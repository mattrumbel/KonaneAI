# KonaneAI

**Valid Paths:**  
**/** -> "Hello World"  
**/join** -> Adds player and returns player number    
**/getPlayerID** -- playerNum -> Returns player ID  
**/getCurrentPlayer** -> Returns player number of competitor who can go  
**/printBoard** -> Returns a string representation of the board  
**/removeStartPiece** -- playerID, pieceNum -> Removes piece if valid and returns string representation of the board

## Important Numbering
Each player can remove one of four pieces. The corner pieces are labelled as follows:

**TL:** 1  
**TR:** 2  
**BR:** 3  
**BL:** 4  

The center pieces are labelled sequentially:

**Center:**  
5,6  
8,7

After the first player picks a piece, the second player enters a piece number between 1 and 4. These represent the pieces surrounding the initial selection in this order:  
.. 1 ..  
4 X 2  
.. 3 ..

## Board Representation

## Heuristic