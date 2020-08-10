# NOTES ON ARTEMIS AND ARTEMIS CONNECTOR

## General

* We only need to respond when a message beginning with a question mark is received

* All messages must be sent with "\n" at the end for the server to recognize it as a final message.

* writing a message must be encoded to ascii and decoding must be done to utf-8

* If we want to just get the next line of code, we can do a read_until(b"\n") and this will print the newest line received

* a piece removal must have the form [x:y]

* a piece move must have the form [startX:startY]:[endX:endY]

* Since the game does not give us the board, we will have to maintain our own board at all times and execute every move ourselves. 

## How Commands Are Sent and How to Recieve Them

* When both players have properly requested each other, they will both recieve a message about what game number they are playing (e.g. "Game:1")

* After both players have received a message about what game it is, the server will assign one of them as Player 1 and the other as Player 2.

* Player 1 will be told right away that they are "Player:1" and asked to remove a piece. Once a removal instruction has been sent, Player 1 will be told which color they are (the color of the piece they removed) and the removed piece move will be recieved.

* While Player 1 is starting the game, Player 2 does not receive any information, including that they are Player 2. Only after the first player has removed a piece will the second player be told what color they are, what player number they are, and what the first player's move was (in that order). 

* After both players have removed pieces, their receival of information becomes identical in formatting.

* The server will now send "?Move commands whenever we need to do something. When we recieve this, the AI can make a move.

* We will need to periodically check if the game has ended when move commands have been sent to the server. If we do not recieve a game over message, we will know to modify our board using the move that was just sent.

## How to Sequence Playing the Game

* Since Player 1 and Player 2 will recieve information in different orders, we will have to add in code which accounts for this and will adapt accordingly.

* Player 1 will begin by making a removal move, receiivng their remove from the server and modifying the board with it, and finally wiating to receive the opponents removal command and modifying the board once again

* Player 2 will not know to do anything until player one has finished sending its removal command. At this time Player 2 will remove Player 1's chosen piece and make their own removal. After this they will wait for the first player to send back the first "noraml" move of the game and modify their board accordingly.

* When players get their color, one of them will need to invert their board in order to plahy properly. If a player is White, this corresponds to the -1 on our board representation. We will therefore multiply the entire board by -1 which effectively changes the color of every piece on the board. This allows each object to properly find moves on their own without modifying any of the existing code.

* Once both players have followed these set of protocol steps, they will both be in a position in which the next command they are going to receive will be asking them to make a move. This leads us into the next part of the code

* A while loop with a flag parameter will now run continuously no matter which player the AI is. Since we have set it up such that we know the first received command will be a "?Move" one, we will start with this. First, we check to see if the opponent has won on their previous move by looking at the received message. If they have not, we will make our own move. We then receive this move from the server and modify our board using it. Now we will look for the next message from the server. If this string says "You won!" we know that our last move won the game and we can finish. Otherwise we know this command was another move from the opponent and we will once again have to modify the board. At this point the loop will start again looking to see if the opponent had won or if we need to move again. The loop continues until it received a message that either us or the opponent has won.

## How Information Is transferred

This section is for keeping track of how information is transferred at certain points

* _int2move takes a hashed value and returns an array with the startX, startY, endX, endY in that order

* getActionProb returns a list of best moves in hashed value forms 

* np.random.choice will return the position in the hash table which has the highest valued move