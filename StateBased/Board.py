class Board:

    def __init__(self, size = 18, p0_piece = 18, p1_piece = 18):
        """
        Initialize the board
        :param size: size of board
        """
        self.size = size
        # Columns labeled as letters, a-r, create dictionary to indicate numerical value
        self.cols = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h',
                     8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o',
                     15: 'p', 16: 'q', 17: 'r'}

        # keep track of the number of pieces each player has, useful for some
        # static board evaluations
        self.piece_count = {0 : p0_piece,
                            1 : p1_piece}

        # Set up the board (2d list matrix)
        self.gameBoard = list()
        for i in range(self.size):
            self.gameBoard.append(list())

        # int 0 = black, int 1 = white, str " " = Blank/Open Space
        # Fill the board
        for i in range(self.size):
            # Max cache performance?
            currRow = self.gameBoard[i]
            if i % 2 == 0:
                for k in range(self.size):
                    currRow.append(k % 2)
            else:
                for k in range(1, self.size + 1):
                    currRow.append(k % 2)

    def movePiece(self, start, end):
        """
        Move the pieces around
        :param self:
        :param start: starting position (x_position, y_position)
        :param end: ending position     (x_position, y_position)
        :return: None
        """
        # May need to switch up depending on how server interaction works
        piece = self.gameBoard[start[1]][start[0]]
        # Remove pieces between [start and ending positions
        if start[1] == end[1]:
            # Horizontal Move, clear spaces
            currRow = self.gameBoard[start[1]]
            # Find section to clear out
            if start[0] < end[0]:
                a = start[0]
                b = end[0] + 1
            else:
                a = end[0]
                b = start[0] + 1
            for i in range(a, b):
                to_rm = currRow[i]
                if to_rm == 0:
                    self.piece_count[0] -= 1
                elif to_rm == 1:
                    self.piece_count[1] -= 1
                currRow[i] = " "
        elif start[0] == end[0]:
            # Vertical Move, clear spaces between [start and end positions
            if start[1] < end[1]:
                a = start[1]
                b = end[1] + 1
            else:
                a = end[1]
                b = start[1] + 1
            x_pos = start[0]
            for i in range(a, b):
                to_rm = self.gameBoard[i][x_pos]
                if to_rm == 0:
                    self.piece_count[0] -= 1
                elif to_rm == 1:
                    self.piece_count[1] -= 1
                self.gameBoard[i][x_pos] = " "
        else:
            raise AttributeError("Invalid Move")
        # Set the correct ending piece
        self.piece_count[piece] += 1
        self.gameBoard[end[1]][end[0]] = piece

    def removePiece(self, loc):
        """
        Remove a piece at a certain location
        :param loc: piece coordinate    (x_coordinate, y_coordinate)
        :return:
        """

        self.piece_count[self.gameBoard[loc[1]][loc[0]]] -= 1
        self.gameBoard[loc[1]][loc[0]] = " "

    def __str__(self):
        """
        Print the game board
        :return: None
        """
        # TODO __str__ should return printable string?, not print the desired string
        print("-" * (self.size * 2 + 1))
        for row in self.gameBoard:
            print("|", end = "")
            for i in range(len(row)):
                print(row[i], end = "|")
            print("\n", end = "")
        print("-" * (self.size * 2 + 1))

        return ""


if __name__ == "__main__":
    b = Board()
    b.removePiece((0, 0))
    b.removePiece((0, 1))
    print(b)
    print(b.piece_count)
    b.movePiece((2, 1), (0, 1))
    print(b)
    print(b.piece_count)
    b.movePiece((0, 2), (0, 0))
    print(b)
    print(b.piece_count)
