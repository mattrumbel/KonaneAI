from flask import Flask
from datetime import datetime
from random import seed, randint
import sys
import math

app = Flask(__name__)

boardWidth = 18
boardHeight = 18
playerPiece = ('X','O')
emptyPiece = '.'

startingPieces = {
    1: (0,0),
    2: (0, boardWidth - 1),
    3: (boardHeight - 1, boardWidth - 1),
    4: (boardHeight - 1, 0),
    5: (boardHeight//2 - 1, boardWidth//2 - 1),
    6: (boardHeight//2 - 1, boardWidth//2),
    7: (boardHeight//2, boardWidth//2),
    8: (boardHeight//2, boardWidth//2 - 1)
}

startSurround = {
    1: (-1,0),
    2: (0, 1),
    3: (1, 0),
    4: (0, -1)
}

board = [[playerPiece[(i+j) % 2] for j in range(0, boardWidth)] for i in range(0, boardHeight)]

seed(datetime.now())
playerID = (randint(0, 2000), randint(0,2000))
while playerID[0] == playerID[1]:
        playerID = (randint(0, 2000), randint(0,2000))

print(playerID)
joined = [False, False]
gotID = [False, False]
currentPlayer = 0  
startPiece = (0,0)

def nextPlayer():
    global currentPlayer
    currentPlayer = (currentPlayer + 1) % 2

@app.route("/")
def helloWorld():
    return "Hello World"

@app.route("/join")
def join():
    if not (joined[0] and joined[1]):
        if not joined[0] and not joined[1]:
            rand = randint(0,1)
            joined[rand] = True
            return str(rand)
        else:
            print("LETS START THE GAME!!!")
            if not joined[0]:
                joined[0] = True
                return str(0)
            else:
                joined[1] = True
                return str(1)
    else:
        return "Two players are already playing"

@app.route("/getPlayerID/<pNum>")
def getPlayerID(pNum):
    pNum = int(pNum)
    if not gotID[pNum]:
        gotID[pNum] = True
        return str(playerID[pNum])
    else:
        return "ID already taken"

@app.route("/currentPlayer")
def getCurrentPlayer():
    return str(currentPlayer)

@app.route("/printBoard")
def printBoard():
    boardToStr = '  '
    for i in range(0, boardWidth):
        boardToStr += (str(i%10) + ' ')
    boardToStr += '\n'
    inc = 0
    for row in board:
        rowToStr = ' '.join(map(str, row)) + "\n"
        boardToStr += (str(inc%10) + ' ' + rowToStr)
        inc += 1
    return boardToStr

@app.route("/removeStartPiece/<pID>/<pieceNum>")
def removeStartPiece(pID, pieceNum):
    pID = int(pID)
    pieceNum = int(pieceNum)
    global playerPiece
    global startPiece

    if(pID == playerID[currentPlayer]):
        if(currentPlayer == 0):
            if pieceNum in startingPieces:
                if(pieceNum % 2 == 0):
                    playerPiece = ('0','X')
                else:
                    playerPiece = ('X', 'O')
                startPiece = startingPieces[pieceNum]
                board[startPiece[0]][startPiece[1]] = emptyPiece
                nextPlayer()
                return printBoard()
            else:
                return "Invalid Starting Piece"
        else:
            if pieceNum in startSurround:
                y = startPiece[0] + startSurround[pieceNum][0]
                x = startPiece[1] + startSurround[pieceNum][1]
                if x < boardWidth and y < boardHeight and x >= 0 and y >= 0:
                    board[y][x] = emptyPiece
                    nextPlayer()
                    return printBoard()
                else:
                    return "Invalid Starting Place"
            else:
                return "Invalid Starting Piece"
    else:
        return "Invalid Turn Order"

@app.route("/move/<pID>/<startX>/<startY>/<endX>/<endY>")
def move(pID, startX, startY, endX, endY):
    print(playerPiece)
    pID = int(pID)
    startX = int(startX)
    startY = int(startY)
    endX = int(endX)
    endY = int(endY)

    dirX = 0
    dirY = 0
    if endX - startX > 0:
        dirX = 1
    elif endX - startX < 0:
        dirX = -1
    if endY - startY > 0:
        dirY = 1
    elif endY - startY < 0:
        dirY = -1
    

    if pID == playerID[currentPlayer]:
        if startX < boardWidth and startY < boardHeight and endX < boardWidth and endY < boardHeight and startX >= 0 and startY >= 0 and endX >= 0 and endY >= 0:
            if (startX == endX and not startY == endY) or (not startX == endX and startY == endY):
                if board[startY][startX] == playerPiece[currentPlayer]:
                    if board[endY][endX] == emptyPiece and endY % 2 == startY % 2 and endX % 2 == startX % 2:
                        if startX == endX:
                            for i in range(min(startY, endY), max(startY, endY), 2):
                                if board[i + dirY][startX] == playerPiece[currentPlayer] or board[i + dirY][startX] == emptyPiece:
                                    return "Invalid Jump"
                            board[startY][startX] = emptyPiece
                            for i in range(min(startY, endY), max(startY, endY), 2):
                                board[i + dirY][startX] = emptyPiece
                            board[endY][endX] = playerPiece[currentPlayer]
                            nextPlayer()
                            return printBoard()
                        else:
                            for i in range(min(startX, endX), max(startX, endX), 2):
                                if board[startY][i + dirX] == playerPiece[currentPlayer] or board[startY][i + dirX] == emptyPiece:
                                    return "Invalid Jump"
                            board[startY][startX] = emptyPiece
                            for i in range(min(startX, endX), max(startX, endX), 2):
                                board[startY][i + dirX] = emptyPiece
                            board[endY][endX] = playerPiece[currentPlayer]
                            nextPlayer()
                            return printBoard()
                    else:
                        return "Invalid Final Position"
                else:
                    return "Invalid Piece Moved"
            else:
                return "Invalid Direction Moved"
        else:
            return "Invalid Location Bounds"
    else:
        return "Invalid Turn Order"

if __name__ == "__main__":
    print("Running Main")
    app.run(host="0.0.0.0")
