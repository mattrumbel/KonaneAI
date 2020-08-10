"""
Author: UCONN AI
Date: Nov 20, 2019.
"""


class Board:

    def __init__(self):
        self.width = 18
        self.height = 18

        self.pieces = list()
        for y in range(self.height):
            self.pieces.append(list())

        for y in range(self.height):
            currRow = self.pieces[y]
            for x in range(self.width):
                if (x + y) % 2 == 0:
                    currRow.append(1)
                else:
                    currRow.append(-1)

    # TODO: Believed to no longer be used
    # def __getitem__(self, index):
    #     print("\n\n__getitem__\n\n")
    #     return self.pieces[index]

    def get_legal_moves(self, color):
        """
        Returns all the legal moves for the given color
        :param color: Color to generates moves for (1 for white, -1 for black)
        :return: 2d array of moves (list of list of coordinates corresponding to moves)
        """
        remPieces = self._isBoardFull()
        if remPieces == 0:
            return self._getFirstMoves()
        if remPieces == 1:
            return self._getSecondMoves()
        else:
            return self._getValidMoves(color)

    def execute_move(self, move, color):
        """
        Executes a move, given the coordinates and color
        TODO Why is this method required?  Seems like just a middle man for _movePiece
        :param move: coordinates of a move
        TODO Shouldn't need color here, assume piece has already been checked for legality
        :param color: color, for verification
        :return: None, updates the board
        """
        x1, y1, x2, y2 = move
        if self._isBoardFull() == 0:
            # print("FIRST MOVE")
            if not self.pieces[x1][y1] == color:
                self._invertBoard()
        self._movePiece(x1, y1, x2, y2)

################## Internal methods ##################
    @staticmethod
    def _getCaptures(x1, y1, x2, y2):
        """
        get captures from within the coordinate spaces
        Assume move is already checked for legality
        :param x1: int x starting pos
        :param y1: int y starting pos
        :param x2: int x ending pos
        :param y2: int y ending pos
        :return: list of captured piece coordinates?
        """
        captures = []
        if x1 == x2:
            for i in range(min(y1, y2), max(y1, y2), 2):
                captures.extend([[x1, i+1]])
        else:
            for i in range(min(x1, x2), max(x1, x2), 2):
                captures.extend([[i+1, y1]])
        return captures

    def _movePiece(self, x1, y1, x2, y2, first=False):
        """
        move a piece for x1, y1 coords to x2, y2 coords
        TODO Make sure not checking for illegality here doesn't break anything
        :param x1: int x starting pos
        :param y1: int y starting pos
        :param x2: int x ending pos
        :param y2: int y ending pos
        :return: number of pieces captured, after the move was completed
        """
        if(x1 == x2 and y1 == y2):
            self.pieces[y1][x1] = 0
            return 1
        self.pieces[y2][x2] = self.pieces[y1][x1]
        self.pieces[y1][x1] = 0  # Set to empty piece
        # _getCaptures shouldn't hit on start plays
        caps = self._getCaptures(x1, y1, x2, y2)
        for c in caps:
            self.pieces[c[1]][c[0]] = 0

        return len(caps)

    def _getValidMoves(self, player):
        """
        Generates all valid moves
        :param player: player whose turn it is (1 for white, -1 for black)
        :return: list of list of move coordinates [[x1, y1, x2, y2], ...]
        """
        legal_moves = []

        for y in range(self.height):
            for x in range(self.width):
                if player == self.pieces[y][x]:
                    # Generate legal Up moves
                    for k in range(2, self.height, 2):
                        if y >= k:
                            if (self.pieces[y - (k - 1)][x] == player * -1) and self.pieces[y - k][x] == 0:
                                legal_moves.append([x, y, x, y - k])
                            else:
                                break
                        else:
                            break
                    # Generate legal Left moves
                    for k in range(2, self.width, 2):
                        if x >= k:
                            if (self.pieces[y][x - (k - 1)] == player * -1) and self.pieces[y][x - k] == 0:
                                legal_moves.append([x, y, x - k, y])
                            else:
                                break
                        else:
                            break
                    # Generate legal Down moves
                    for k in range(2, self.height, 2):
                        if y <= (self.height - 1 - k):
                            if (self.pieces[y + (k - 1)][x] == player * -1) and self.pieces[y + k][x] == 0:
                                legal_moves.append([x, y, x, y + k])
                            else:
                                break
                        else:
                            break
                    # Generate legal Right moves
                    for k in range(2, self.width, 2):
                        if x <= (self.width - 1 - k):
                            if (self.pieces[y][x + (k - 1)] == player * -1) and self.pieces[y][x + k] == 0:
                                legal_moves.append([x, y, x + k, y])
                            else:
                                break
                        else:
                            break

        return legal_moves

    def _invertBoard(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                self.pieces[i][j] *= -1

    def _getFirstMoves(self):
        """
        Get a list of all valid first move coordinates, independent of player turn
        :return: list of list of move coordinates [[x1, y1, x2, y2], ...]
        """
        moves = [
            [0, 0, 0, 0],
            [0, self.width - 1, 0, self.width - 1],
            [self.height - 1, self.width - 1, self.height - 1, self.width - 1],
            [self.height - 1, 0, self.height - 1, 0],
            [self.height//2 - 1, self.width//2 - 1,
                self.height//2 - 1, self.width//2 - 1],
            [self.height//2 - 1, self.width//2, self.height//2 - 1, self.width//2],
            [self.height//2, self.width//2, self.height//2, self.width//2],
            [self.height//2, self.width//2 - 1, self.height//2, self.width//2 - 1]]
        return moves
        # moves = []
        # moves.append((tuple([0]*2)))
        # moves.append((tuple([self.size-1]*2)))
        # moves.append((tuple([self.size//2]*2)))
        # moves.append((tuple([(self.size//2)-1]*2)))
        # return moves

    def _getSecondMoves(self):
        """
        get list of all valid second move coordinates, independent of player turn
        Assumes first piece removal is legal and board state is valid
        :return: list of list of move coordinates [[x1, y1, x2, y2], ...]
        """
        moves = []

        if self.pieces[0][0] == 0:
            # Upper left
            moves.append([0, 1, 0, 1])
            moves.append([1, 0, 1, 0])
        elif self.pieces[0][self.width - 1] == 0:
            # Upper right
            moves.append([self.width - 2, 0, self.width - 2, 0])
            moves.append([self.width - 1, 1, self.width - 1, 1])
        elif self.pieces[self.height - 1][0] == 0:
            # Bottom left
            moves.append([0, self.height - 2, 0, self.height - 2])
            moves.append([1, self.height - 1, 1, self.height - 1])
        elif self.pieces[self.height-1][self.height-1] == 0:
            # Bottom right
            moves.append([self.width - 1, self.height - 2, self.width - 1, self.height - 2])
            moves.append([self.width - 2, self.height - 1, self.width - 2, self.height - 1])
        else:
            # Middle of the board
            to_break = False
            for y in range(self.height // 2 - 1, self.height // 2 + 1):
                for x in range(self.width // 2 - 1, self.width // 2 + 1):
                    if self.pieces[y][x] == 0:
                        moves.append([x, y - 1, x, y - 1])
                        moves.append([x, y + 1, x, y + 1])
                        moves.append([x - 1, y, x - 1, y])
                        moves.append([x + 1, y, x + 1, x])
                        to_break = True
                        break
                if to_break:
                    break

        return moves

        """
        elif self.pieces[(self.height // 2) - 1][(self.width // 2) - 1] == 0:
            # Middle, top left
            moves.append([self.width // 2, self.height // 2 - 1, self.width // 2, self.height // 2 - 1])
            moves.append([self.width // 2, self.height // 2 + 1, self.width // 2, self.height // 2 + 1])

            moves.append([self.height//2, self.width// 2 - 1, self.height//2, self.width// 2 - 1])
            moves.append([self.height//2 - 2, self.width// 2 - 1, self.height//2 - 2, self.width// 2 - 1])
            moves.append([self.height//2 - 1, self.width//2, self.height//2 - 1, self.width//2])
            moves.append([self.height//2 - 1, self.width//2 - 2, self.height//2 - 1, self.width//2 - 2])
        elif self.pieces[(self.height // 2) - 1][self.width // 2] == 0:
            # Middle, top right
            moves.append([self.height//2 - 1, self.width// 2 - 1, self.height//2 - 1, self.width// 2 - 1])
            moves.append([self.height//2 - 1, self.width// 2 + 1, self.height//2 - 1, self.width// 2 + 1])
            moves.append([self.height//2, self.width//2, self.height//2, self.width//2])
            moves.append([self.height//2 - 2, self.width//2, self.height//2 - 2, self.width//2])
        elif self.pieces[self.height // 2][(self.width // 2) - 1] == 0:
            # Middle, bottom left
            moves.append([self.height//2, self.width// 2, self.height//2, self.width// 2])
            moves.append([self.height//2, self.width// 2 - 2, self.height//2, self.width// 2 - 2])
            moves.append([self.height//2 - 1, self.width//2 - 1, self.height//2 - 1, self.width//2 - 1])
            moves.append([self.height//2 + 1, self.width//2 - 1, self.height//2 + 1, self.width//2 - 1])
        else:
            # Middle, bottom right
            moves.append([self.height//2, self.width// 2 - 1, self.height//2, self.width// 2 - 1])
            moves.append([self.height//2, self.width// 2 + 1, self.height//2, self.width// 2 + 1])
            moves.append([self.height//2 - 1, self.width//2, self.height//2 - 1, self.width//2])
            moves.append([self.height//2 + 1, self.width//2, self.height//2 + 1, self.width//2])
        """

        return moves

        # moves = []
        # if self.pieces[0][0] == 0:
        #     moves.append([0,1,0,1])
        #     moves.append([1,0,1,0])
        #     return moves
        # elif self.pieces[self.height-1][self.height-1] == 0:
        #     moves.append([self.height-1,self.height-2,self.height-1,self.height-2])
        #     moves.append([self.height-2,self.height-1,self.height-2,self.height-1])
        #     return moves
        # elif self.pieces[(self.height//2)-1][(self.height//2)-1] == 0:
        #     pos = (self.height//2) -1
        # else:
        #     pos = self.height//2
        # moves.append([pos,pos-1,pos,pos-1])
        # moves.append([pos+1,pos,pos+1,pos])
        # moves.append([pos,pos+1,pos,pos+1])
        # moves.append([pos-1,pos,pos-1,pos])
        # return moves

    def _isBoardFull(self):
        """
        Checks if the board is full
        :return: int # of missing pieces
        """
        missingPieces = 0
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.pieces[i][j] == 0:
                    missingPieces += 1
        return missingPieces
