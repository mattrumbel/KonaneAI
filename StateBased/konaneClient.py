import requests

url = 'http://localhost:5000/'

pID = '0'
pNum = '0'

def getBoard():
    return requests.get(url + 'printBoard')

def getPlayerID():
    return requests.get(url + 'getPlayerID/' + pNum)

def removeStartPiece(pID, pieceNum):
    return requests.get(url + 'removeStartPiece/'  + pID + '/' + str(pieceNum))

def checkCurrentPlayer():
    return requests.get(url + 'currentPlayer')

def joinServer():
    return requests.get(url + 'join')

def move(startX, startY, endX, endY):
    return requests.get(url + 'move/' + pID + '/' + startX + '/' + startY + '/' + endX + '/' + endY)


if __name__ == "__main__":
    pNum = joinServer().text
    print(pNum)
    pID = getPlayerID().text
    print(pID)
    print("What start piece would you like to remove?")
    startNum = int(input())
    print(removeStartPiece(pID,startNum).text)
    print(checkCurrentPlayer().text)
    while True:
        print("Enter Your Move")
        startX = input("startX: ")
        startY = input("startY: ")
        endX = input("endX: ")
        endY = input("endY: ")
        print(move(startX, startY, endX, endY).text)
        print(checkCurrentPlayer().text)
