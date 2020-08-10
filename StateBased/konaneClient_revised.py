import requests
import time

url = 'http://localhost:5000/'

pID = '0'
pNum = '0'

def getBoard():
    return requests.get(url + 'printBoard')

def getPlayerID():
    return requests.get(url + 'getPlayerID/' + pNum)

def getBoardVal(xLoc,yLoc):
    return requests.get(url + 'getBoardVal/' + xLoc + '/' + yLoc)

def getPlayerColor(pNum):
    return requests.get(url + 'getPlayerColor/' + pNum)

def removeStartPiece(pNum, xLoc,yLoc):
    return requests.get(url + 'removeStartPiece/'  + pNum + '/' + xLoc + '/' + yLoc)

def checkCurrentPlayer():
    return requests.get(url + 'currentPlayer')

def joinServer():
    return requests.get(url + 'join')

def move(startX, startY, endX, endY):
    return requests.get(url + 'move/' + startX + '/' + startY + '/' + endX + '/' + endY)

def isFirstValid(xLoc,yLoc):
    return requests.get(url + 'isFirstValid/' + xLoc + '/' + yLoc)

def isSecondValid(pNum, xLoc,yLoc):
    return requests.get(url + '/' + pNum + '/' + xLoc + '/' + yLoc)

def isMoveValid(pNum, startX, startY, endX, endY):
    return requests.get(url + 'isMoveValid/' + pNum + '/' + startX + '/' + startY + '/' + endX + '/' + endY)


if __name__ == "__main__":
    pNum = joinServer().text
    print("Your player number is: ", pNum)
    pID = getPlayerID().text
    print("Your player ID is: ", pID)

    if pNum=='0':
        print("This is the starting board:")
        currBoard = getBoard().text
        print(currBoard)
        print("You must first remove a piece.")
        isValid = False
        while not isValid:
            xLoc = input("Please enter the X coordinate of the first piece to remove: ")
            yLoc = input("Please enter the Y coordinate of the first piece to remove: ")
            if isFirstValid(xLoc,yLoc).text == 'False':
                print("This is an invalid piece to remove. Please try again.")
            else:
                isValid = True
        print(removeStartPiece(pNum,xLoc,yLoc).text)
        print("Waiting for next player to move...")
        checker = True
        while checker:
            time.sleep(1)
            checker = checkCurrentPlayer().text != pNum
        print("Your opponent has made the first move. This is the current board:")
        currBoard = getBoard().text
        print(currBoard)

    else:
        print("Please wait for player 0 to make the first move")
        checker = True
        while checker:
            time.sleep(1)
            checker = checkCurrentPlayer().text != pNum
        print("Your opponent has made the first move. This is the current board:")
        currBoard = getBoard().text
        print(currBoard)
        print("You must now remove a piece as well.")
        isValid = False
        while not isValid:
            xLoc = input("Please enter the X coordinate of the piece to remove: ")
            yLoc = input("Please enter the Y coordinate of the piece to remove: ")
            if isSecondValid(pNum, xLoc,yLoc).text == 'False':
                print("This is an invalid piece to remove. Please try again.")
            else:
                isValid = True
        # print("the player number is: ", pNum)
        # print("the x location is: ", xLoc)
        # print("the y location is: ", yLoc)
        # boardVal = getBoardVal(xLoc, yLoc).text
        # print("the board at the given location is: ", boardVal)
        # myColor = getPlayerColor(pNum).text
        # print("my piece color is: ", myColor)
        print(removeStartPiece(pNum,xLoc,yLoc).text)
        print("Waiting for next player to move...")
        checker = True
        while checker:
            time.sleep(1)
            checker = checkCurrentPlayer().text != pNum
        print("Your opponent has made the first move. This is the current board:")
        currBoard = getBoard().text
        print(currBoard)

    while True:
        print("Enter Your Next Move")
        isValid = False
        while not isValid:
            startX = input("startX: ")
            startY = input("startY: ")
            endX = input("endX: ")
            endY = input("endY: ")
            if isMoveValid(pNum, startX,startY, endX, endY).text == 'False':
                print("This is an invalid piece to remove. Please try again.")
            else:
                isValid = True
        print(move(startX, startY, endX, endY).text)
        print("Waiting for next player to move...")
        checker = True
        while checker:
            time.sleep(1)
            checker = checkCurrentPlayer().text != pNum
        print("Your opponent has made a move. This is the current board:")
        currBoard = getBoard().text
        print(currBoard)
