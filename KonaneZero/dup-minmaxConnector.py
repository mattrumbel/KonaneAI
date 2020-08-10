from telnetlib import Telnet
from Board import Board
from Konane import Game
import random

# Prints the next received command
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
    uName = "99\n"
    tn.write(bytes(uName.encode('ascii')))
    print("Logging in user: ", uName)
    printNext()
    password = "100\n"
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
        print("I recognized I am the 1 player.")
        return 1
    else:
        print("I recognized I am the 0 player.")
        return 0

# Protocol for the first player to remove a piece
def firstRemove():
    # Make the first move of the game

    game = Game()
    print("Here is the starting board:")
    print(game.board)

    p1_coords = game.generate_legal_moves(0)
    k = random.randint(0, len(p1_coords) - 1)
    game.board.removePiece(p1_coords[k])

    removeMessage = encodeRemove(p1_coords[k])

    # removeMessage = "[9:9]\n"
    tn.write(bytes(removeMessage.encode('ascii')))

    # Receive your color
    read_string = tn.read_until(b'\n')
    myColor = getMyColor(read_string.decode('utf-8'))

    # Receive the piece you just removed and take it out from the board
    read_string = tn.read_until(b'\n')
    newMove = parseRemove(read_string.decode('utf-8'))
    print("Board after your removal:")
    print(game.board)

    # Receive the piece your opponent removed and take it out from the board
    read_string = tn.read_until(b'\n')
    newMove = parseRemove(read_string.decode('utf-8'))
    game.board.removePiece(newMove)
    print("Board after opponent's removal:")
    print(game.board)
    return game, myColor

# Protocol for the second player to remove the second piece
def secondRemove(messages):
    # First message received is your color. Set it
    myColor = getMyColor(messages[0])
    game = Game(player=myColor, ai_player=myColor, opp_player=1-myColor)

    # Third message is what the first player removed. Remove it from the board
    newMove = parseRemove(messages[2])
    game.board.removePiece(newMove)
    print("Board after opponent's removal:")
    print(game.board)

    # Remove your own piece
    p2_coords = game.generate_legal_moves(1) # getting second move
    k = random.randint(0, len(p2_coords) - 1)
    game.board.removePiece(p2_coords[k])
    removeMessage = encodeRemove(p2_coords[k])
    # removeMessage = "[10:9]\n"
    tn.write(bytes(removeMessage.encode('ascii')))
    print("Board after your removal:")
    print(game.board)

    # Receive the move you just made
    read_string = tn.read_until(b'\n')

    # Get the first normal move from your opponent and execute it
    read_string = tn.read_until(b'\n')
    newMove = parseMove(read_string.decode('utf-8'))
    game = makeMove(game, newMove)
    print("Board after opponent's move:")
    print(game.board)
    return game, myColor

# Translates a move from the AI syntax to server syntax
def encodeRemove(move):
    moveCommand = "[" + str(move[0]) + ':' + str(move[1]) + "]\n"
    return moveCommand

# Translates a move from AI syntac to server syntax
def encodeMove(move):
    moveCommand = "[" + str(move[0][0]) + ':' + str(move[0][1]) + "]:[" + str(move[1][0]) + ":" + str(move[1][1]) + "]\n"
    return moveCommand

# Parses a removal message and takes out the coordinates 
def parseRemove(message):
    message = message[8:]
    locations = ""
    for i in message:
        if i != "[" and i != "]":
            locations += i
    locations = locations.split(":")
    return (int(locations[0]), int(locations[1]))

# Parses a move message to get start and end coordinates
def parseMove(message):
    message = message[5:]
    locations = ""
    for i in message:
        if i != "[" and i != "]":
            locations += i
    locations = locations.split(":")
    return ((int(locations[0]), int(locations[1])), (int(locations[2]), int(locations[3])))

# Takes a move and changes the board
def makeMove(game, move):
    game.board.movePiece(move[0],move[1])
    return game

# Generates the next move to be made. Return
def generateMove(game, player):
    game.player_turn = player
    move = game.player_move()
    return game, move

if __name__ == "__main__":
    print("Connecting to server...")
    with Telnet('artemis.engr.uconn.edu', 4705) as tn:
        print("Successfully connected to server!")

        # Run the standard protocol for logging in and connecting to your opponent
        startGame()

        # Wait to be asked to remove a piece and create an array of all commands recieved in this time
        read_string = tn.read_until(b"?Remove:\n")
        read_string = read_string.decode('utf-8')
        rm = read_string.split('\n')

        # Check to see if a player is player 1 or player 2 based on what commands are in L
        if rm[0] == 'Player:1':
            print("You are player 1.\n")
            game, myColor = firstRemove()
        else:
            print("You are player 2.\n")
            game, myColor = secondRemove(rm)

        moves = 0

        # Now each player begins waiting for their turn to make a move and keeping track of their board
        flag = True
        while flag:
            # Check to see if your opponent won or if you need to make a move
            # time.sleep(180)
            read_string = tn.read_until(b'\n')
            read_string = read_string.decode('utf-8')
            print("Remember, you are player: ", myColor)
            print(read_string)
            if read_string == "Opponent wins!" or read_string == "Opponent wins!\n":
                print("Thanks for playing!")
                flag = False

            # Generate your move to make
            game, move = generateMove(game, myColor)
            print("This is what we are getting for move:", move)
            moveMessage = encodeMove(move)
            tn.write(bytes(moveMessage.encode('ascii')))
            
            moves = moves + 1

            # Receive the move you just made and remove the apppropriate pieces from the board
            read_string = tn.read_until(b'\n')
            print("This is the board after your move:")
            print(game.board)

            # Check to see if you won by making that move
            read_string = tn.read_until(b'\n')
            read_string = read_string.decode('utf-8')
            print(read_string)
            if read_string == "You win!" or read_string == "You win!\n":
                print("Thanks for playing!")
                flag = False

            # If your opponent has not won, use the move they sent to again modify the board to its current state
            newMove = parseMove(read_string)
            game = makeMove(game, newMove)
            print("This is the board after your opponent's move:")
            print(game.board)

            moves = moves + 1

            print("This many moves have been made: ", moves)

        #Close game connection
        tn.close()
