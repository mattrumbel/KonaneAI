from telnetlib import Telnet
from konane.KonaneGame import KonaneGame as Game
from konane.KonaneGame import display
from konane.KonaneLogic import Board
import numpy as np
from MCTS import MCTS
from konane.pytorch.NNet import NNetWrapper as nn
from utils import *
from Coach import Coach
import time

# Function that will print out the next line of information received
def printNext():
    read_string = tn.read_until(b'\n')
    print(read_string.decode('utf-8'))

# Function does the basic protocol for starting up a game. Ends when opponents are connected
def startGame():

    # Get connecting to the server message
    printNext()
    
    # Get username question
    printNext()
    
    # Log in to the server using username and password
    uName = "12\\n"
    tn.write(bytes(uName.encode('ascii')))
    print("Logging in user: ", uName)
    printNext()
    password = "111\n"
    tn.write(bytes(password.encode('ascii')))
    print("User password received, successful login.\n")

    # Wait for server to ask for opponent
    printNext()

    # Give the opponents username to connect to and print out the game number
    opponent = str(input("Please input your opponent's username: "))
    opponent = opponent + "\n"
    tn.write(bytes(opponent.encode('ascii')))

    # Recieve what game number is being played
    printNext()

# Get which color you are
def getMyColor(message):
    print("This is what is received by getMyColor: ", message)

    # if message == "Color:WHITE" or message == "Color:BLACK":
    #     print("Option 1")
    # elif message == "Color:WHITE\n" or message == "Color:BLACK\n":
    #     print("Option 2")

    if message == "Color:WHITE\n" or message == "Color:WHITE":
        print("I recognized I am the O (-1) player.")
        return -1
    else:
        print("I recognized I am the X (1) player.")
        return 1

# Protocol for the first player to remove a piece
def firstRemove(myCoach, board):
    # Make the first move of the game
    move = generateMove(myCoach, board)
    removeMessage = encodeRemove(move)
    # removeMessage = "[9:9]\n"
    tn.write(bytes(removeMessage.encode('ascii')))

    # Receive your color
    read_string = tn.read_until(b'\n')
    myColor = getMyColor(read_string.decode('utf-8'))

    # Receive the piece you just removed and take it out from the board
    read_string = tn.read_until(b'\n')
    x, y = parseRemove(read_string.decode('utf-8'))
    board = makeMove(board, x, y, x, y)
    print("Board after your removal:")
    print(display(board))

    # Receive the piece your opponent removed and take it out from the board
    read_string = tn.read_until(b'\n')
    x, y = parseRemove(read_string.decode('utf-8'))
    board = makeMove(board, x, y, x, y)
    print("Board after opponent's removal:")
    print(display(board))
    return board, myColor

# Protocol for the second player to remove the second piece
def secondRemove(myCoach, board, messages):
    # First message received is your color. Set it
    myColor = getMyColor(messages[0])

    # Third message is what the first player removed. Remove it from the board
    x, y = parseRemove(messages[2])
    board = makeMove(board, x, y, x, y)
    print("Board after opponent's removal:")
    print(display(board))

    # Remove your own piece
    move = generateMove(myCoach, board)
    removeMessage = encodeRemove(move)
    # removeMessage = "[10:9]\n"
    tn.write(bytes(removeMessage.encode('ascii')))

    # Receive the move you just made and remove it
    read_string = tn.read_until(b'\n')
    x, y = parseRemove(read_string.decode('utf-8'))
    board = makeMove(board, x, y, x, y)
    print("Board after your removal:")
    print(display(board))

    # Get the first normal move from your opponent and execute it
    read_string = tn.read_until(b'\n')
    startX, startY, endX, endY = parseMove(read_string.decode('utf-8'))
    board = makeMove(board, startX, startY, endX, endY)
    print("Board after opponent's move:")
    print(display(board))
    return board, myColor

# Translates a move from the AI syntax to server syntax
def encodeRemove(move):
    moveCommand = "[" + str(move[0]) + ':' + str(move[1]) + "]\n"
    return moveCommand

# Translates a move from AI syntac to server syntax
def encodeMove(move):
    moveCommand = "[" + str(move[0]) + ':' + str(move[1]) + "]:[" + str(move[2]) + ":" + str(move[3]) + "]\n"
    return moveCommand

# Parses a removal message and takes out the coordinates 
def parseRemove(message):
    message = message[8:]
    locations = ""
    for i in message:
        if i != "[" and i != "]":
            locations += i
    locations = locations.split(":")
    return int(locations[0]), int(locations[1])

# Parses a move message to get start and end coordinates
def parseMove(message):
    message = message[5:]
    locations = ""
    for i in message:
        if i != "[" and i != "]":
            locations += i
    locations = locations.split(":")
    return int(locations[0]), int(locations[1]), int(locations[2]), int(locations[3])

# Creates a Coach and Board object for the rest of usage. Args is duplicated from main.py
def generateObjects():
    args = dotdict({
        'numIters': 100,
        'numEps': 10,
        'tempThreshold': 5,
        'updateThreshold': 0.6,
        'maxlenOfQueue': 200000,
        'numMCTSSims': 4,
        'arenaCompare': 40,
        'cpuct': 1,

        'checkpoint': './temp/',
        'load_model': False,
        'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
        'numItersForTrainExamplesHistory': 20,})
    game = Game()
    nnet = nn(game)
    if args.load_model:
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
    myCoach = Coach(game, nnet, args)
    board = myCoach.game.getInitBoard()
    return myCoach, board

# Takes a move and changes the board
def makeMove(board, x1, y1, x2, y2):
    b = Board()
    if(x1 == x2 and y1 == y2):
        board[y1][x1] = 0
    board[y2][x2] = board[y1][x1]
    board[y1][x1] = 0
    caps = b._getCaptures(x1, y1, x2, y2)
    for c in caps:
        board[c[1]][c[0]] = 0
    return board

# Generates the next move to be made. Return
def generateMove(myCoach, board, color=1):
    b = Board()
    canonicalBoard = myCoach.game.getCanonicalForm(board, color)
    pi = myCoach.mcts.getActionProb(canonicalBoard)
    action = np.random.choice(len(pi), p=pi)
    move = myCoach.game._int2move(action, b.width, 4)
    print("This is your chosen move: ", move)
    return move

if __name__ == "__main__":
    print("Connecting to server...")
    with Telnet('artemis.engr.uconn.edu', 4705) as tn:
        print("Successfully connected to server!")

        # Return a coach object and a board object. The coach object contains the Game, nnet, and mcts
        myCoach, board = generateObjects()
        print("Here is the starting board:")
        print(display(board))

        # Run the standard protocol for logging in and connecting to your opponent
        startGame()

        # Wait to be asked to remove a piece and create an array of all commands recieved in this time
        read_string = tn.read_until(b"?Remove:\n")
        read_string = read_string.decode('utf-8')
        rm = read_string.split('\n')

        # Check to see if a player is player 1 or player 2 based on what commands are in L
        if rm[0] == 'Player:1':
            print("You are player 1.\n")
            board, playerColor = firstRemove(myCoach, board)
        else:
            print("You are player 2.\n")
            board, playerColor = secondRemove(myCoach, board, rm)

        if playerColor == -1:
            playerPiece = "O"
        else:
            playerPiece = "X"

        moves = 0

        # Now each player begins waiting for their turn to make a move and keeping track of their board
        flag = True
        while flag:
            # Check to see if your opponent won or if you need to make a move
            # time.sleep(180)
            read_string = tn.read_until(b'\n')
            read_string = read_string.decode('utf-8')
            print("Remember, you are player: ", playerPiece)
            print(read_string)
            if read_string == "Opponent wins!" or read_string == "Opponent wins!\n":
                print("Thanks for playing!")
                flag = False

            # Generate your move to make
            move = generateMove(myCoach, board, playerColor)
            moveMessage = encodeMove(move)
            tn.write(bytes(moveMessage.encode('ascii')))
            
            moves = moves + 1

            # Receive the move you just made and remove the apppropriate pieces from the board
            read_string = tn.read_until(b'\n')
            startX, startY, endX, endY = parseMove(read_string.decode('utf-8'))
            board = makeMove(board, startX, startY, endX, endY)
            print("This is the board after your move:")
            print(display(board))

            # Check to see if you won by making that move
            read_string = tn.read_until(b'\n')
            read_string = read_string.decode('utf-8')
            print(read_string)
            if read_string == "You win!" or read_string == "You win!\n":
                print("Thanks for playing!")
                flag = False

            # If your opponent has not won, use the move they sent to again modify the board to its current state
            startX, startY, endX, endY = parseMove(read_string)
            board = makeMove(board, startX, startY, endX, endY)
            print("This is the board after your opponent's move:")
            print(display(board))

            moves = moves + 1

            print("This many moves have been made: ", moves)


        #Close game connection
        tn.close()