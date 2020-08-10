from Board import Board
from copy import deepcopy
from time import time, sleep
import random


class Game:

    def __init__(self, board=Board(), size=18, player=0, prev_move=((), ()), ai_player=0, opp_player=1):
        """
        Constructor fucntion for Konane game
        :param board: board object
        :param size: size of game board (18 by default)
        :param player: which player's turn? 0 or 1.
        Assume 0 (computer) goes first by default
        :param prev_move: previous move coordinates
        :param ai_player: is AI player 0 or 1
        :param opp_player: is opponent player 0 or 1
        """
        # The Board object
        self.board = board
        # The actual game board matrix
        self.game_board_mat = board.gameBoard
        self.size = size
        self.player_turn = player
        self.ai_player = ai_player
        self.opponent = opp_player
        self.endgame = False
        self.prev_move = prev_move

    def countSymbol(self, board, symbol):
        """
        Returns the number of instances of the symbol on the board.
        """
        count = 0
        for r in range(self.size):
            for c in range(self.size):
                if board[r][c] == symbol:
                    count += 1
        return count
        
    def openingMove(self, board):
        """
        Based on the number of blanks present on the konane board, determines
        whether the current move is the first or second of the game.
        """
        return self.countSymbol(board, " ") <= 1

    def generateFirstMoves(self, board):
        """
        Returns random first move of the game.
        """
        moves = []
        moves.append((tuple([0]*2)))
        moves.append((tuple([self.size-1]*2)))
        moves.append((tuple([self.size//2]*2)))
        moves.append((tuple([(self.size//2)-1]*2)))
        return moves

    def generateSecondMoves(self, board):
        """
        Returns second move of the game, based on where the first move occurred.
        """
        moves = []
        if board[0][0] == " ":
            moves.append(tuple([0,1]))
            moves.append(tuple([1,0]))
            return moves
        elif board[self.size-1][self.size-1] == " ":
            moves.append(tuple([self.size-1,self.size-2]))
            moves.append(tuple([self.size-2,self.size-1]))
            return moves
        elif board[(self.size//2)-1][(self.size//2)-1] == " ":
            pos = (self.size//2) -1
        else:
            pos = self.size//2
        moves.append((tuple([pos,pos-1])))
        moves.append((tuple([pos+1,pos])))
        moves.append((tuple([pos,pos+1])))
        moves.append((tuple([pos-1,pos])))
        return moves

    

    def generate_legal_moves(self, player):
        """
        Function that will compute and return legal moves from
        current game position, given a player's turn
        :param player: player: 0 or 1
        :return: list() of lists() of legal moves
        """
        board = self.game_board_mat
        if self.openingMove(board): # if it's the first two moves
            if player== 0:
                return self.generateFirstMoves(board)
            else:
                return self.generateSecondMoves(board)

        legal_moves = list()
        

        for y in range(self.size):
            for x in range(self.size):
                if player == self.game_board_mat[y][x]:

                    # Check up move
                    for k in range(2, self.size, 2):
                        if y >= k:
                            if (self.game_board_mat[y - (k - 1)][x] == 1 - player) and self.game_board_mat[y - k][x] == " ":
                                legal_moves.append(((x, y), (x, y - k)))
                            else:
                                break
                        else:
                            break
                    # Check left
                    for k in range(2, self.size, 2):
                        if x >= k:
                            if (self.game_board_mat[y][x - (k - 1)] == 1 - player) and self.game_board_mat[y][x - k] == " ":
                                legal_moves.append(((x, y), (x - k, y)))
                            else:
                                break
                        else:
                            break
                    # Check down move
                    for k in range(2, self.size, 2):
                        if y <= (self.size - 1 - k):
                            if (self.game_board_mat[y + (k - 1)][x] == 1 - player) and self.game_board_mat[y + k][x] == " ":
                                legal_moves.append(((x, y), (x, y + k)))
                            else:
                                break
                        else:
                            break
                    # Check right move
                    for k in range(2, self.size, 2):
                        if x <= (self.size - 1 - k):
                            if (self.game_board_mat[y][x + (k - 1)] == 1 - player) and self.game_board_mat[y][x + k] == " ":
                                legal_moves.append(((x, y), (x + k, y)))
                            else:
                                break
                        else:
                            break

        return legal_moves

    def generate_successor_states(self):
        """
        Generate successor board, based on legal moves
        :return: list() of successor Board() instances
        """
        # TODO Make sure game instances are correctly generated
        successors = list()
        for move in self.generate_legal_moves(self.player_turn):
            board_copy = deepcopy(self.board)
            board_copy.movePiece(move[0], move[1])
            nextPlayer = 1 - self.player_turn
            successors.append(Game(board_copy, self.size, nextPlayer, move, self.ai_player, self.opponent))

        return successors

    def player_move(self):
        # Simulate a random move for the player
        legal_moves = self.generate_legal_moves(self.player_turn)
        if len(legal_moves) == 0:
            self.endgame = True
            print("Player", self.player_turn, "loses!")
        else:
            k = random.randint(0, len(legal_moves) - 1)
            self.board.movePiece(legal_moves[k][0], legal_moves[k][1])
            self.prev_move = legal_moves[k]
            self.player_turn = 1 - self.player_turn

        """
        try:
            legal_moves = self.generate_legal_moves(self.player_turn)
            # print(legal_moves)
            if len(legal_moves) != 0:
                flag = False
                while not flag:
                    # TODO Will need to modify depending on how moves are received from server
                    for move in legal_moves:
                        print(move)
                    print("Enter x y coordinates of piece to move")
                    start = tuple([int(x) for x in input("Format: x y: ").split()])
                    print("Enter x y coordinates of ending position:")
                    end = tuple([int(x) for x in input("Format: x y: ").split()])
                    move = (start, end)
                    if move in legal_moves:
                        flag = True
                    else:
                        print("Invalid Move!  You lose!")
                        self.endgame = True
                        return
                self.board.movePiece(move[0], move[1])
                self.prev_move = move
                self.player_turn = 1 - self.player_turn
            else:
                self.endgame = True
                print("Player " + self.player_turn + " loses")
        except KeyboardInterrupt:
            raise
        """

    def computer_move(self):
        # TODO Not fully tested
        global minimax_calls
        start = None
        end = None
        if len(self.generate_legal_moves(self.player_turn)) != 0:
            # There are moves available
            minimax_calls += 1
            alpha, move = minimax(float("-inf"), float("inf"), 0, self)
            # print(alpha, move)
            if not(move is None):
                self.board.movePiece(move[0], move[1])
                self.prev_move = move
                self.player_turn = 1 - self.player_turn
                start = (self.board.cols[move[0][0]], move[0][1] + 1)
                end = (self.board.cols[move[1][0]], move[1][1] + 1)
            # May need redundant no-moves-available check here via else:
            else:
                # TODO Under what circumstances is minimax returning None move?
                for move in self.generate_legal_moves(self.player_turn):
                    print(move)
                # Computer lost
                self.endgame = True
                print("Computer (Player %d) loses, darn" % self.player_turn)

        else:
            # Computer can't make any moves, lose
            self.endgame = True
            print("Computer (Player %d) loses, darn" % self.player_turn)

        # TODO May need to modify depending on how we send moves to server
        # Format move to a-r for x coord, 1-18 for y
        return start, end

    def naive_evaluation(self):
        # TODO Add better naive_evaluation (i.e., account for more properties)
        global static_eval_count
        static_eval_count += 1
        my_moves = len(self.generate_legal_moves(self.player_turn))
        opponent_moves = len(self.generate_legal_moves(1 - self.player_turn))

        if my_moves == 0:
            # Current player can't make any moves, lose
            return float("-inf")
        elif opponent_moves == 0:
            # Other player can't make any moves, win
            return float("inf")
        else:
            return my_moves - opponent_moves

    def q_eval(self):
        # Based off static board evaluation q
        global static_eval_count
        static_eval_count += 1

        m = self.board.piece_count[self.player_turn]
        n = self.board.piece_count[1 - self.player_turn]
        if n == 0:
            # return float("inf")
            return 999
        elif m == 0:
            # return float("-inf")
            return 999
        else:
            return m / n

    def r_eval(self):
        # Based off static board evaluation r
        global static_eval_count
        static_eval_count += 1

        m = self.board.piece_count[self.player_turn]
        n = self.board.piece_count[1 - self.player_turn]
        if n == 0:
            return float("inf")
        elif m == 0:
            return float("-inf")
        else:
            return m / (n * 3)


# Some minimax statistics for later use
static_eval_count = 0
minimax_calls = 0
total_branches = 0
cutoffs = 0


def minimax(alpha=float("-inf"), beta=float("inf"), depth_bound=0, game=Game()):
    """
    Player vs AI for minimax algorithm, assume 0 is AI, 1 is Player
    :param alpha: int
    :param beta: int
    :param depth_bound: int (current depth)
    :param game: Game() state
    :return: (alpha, bestmove)
    """
    global static_eval_count
    global minimax_calls
    global total_branches
    global cutoffs

    # TODO Not fully tested
    eval_fs = {'naive': game.naive_evaluation,
               'q': game.q_eval,
               'r': game.r_eval}
    if depth_bound == 2:
        static_eval_count += 1
        # Second slot doesn't matter when at depth cap
        return eval_fs['q'](), None
    else:
        opt_move = None
        minimax_calls += 1
        if game.player_turn == game.ai_player:
            # Assume AI, max
            for successor in game.generate_successor_states():
                total_branches += 1
                board_eval = minimax(alpha, beta, depth_bound + 1, successor)[0]
                if board_eval > alpha:
                    alpha = board_eval
                    opt_move = successor.prev_move
                if alpha >= beta:
                    cutoffs += 1
                    return beta, opt_move
            # print(alpha, opt_move)
            return alpha, opt_move
        else:
            for successor in game.generate_successor_states():
                total_branches += 1
                board_eval = minimax(alpha, beta, depth_bound + 1, successor)[0]
                if board_eval < beta:
                    beta = board_eval
                    opt_move = successor.prev_move
                if beta <= alpha:
                    cutoffs += 1
                    return alpha, opt_move
            # print(beta, opt_move)
            return beta, opt_move


def receive_move():
    pass


def send_move(coord):
    pass


def play():
    # Simulate random (ai vs player) begin, random choice for piece selection
    a = random.randint(0, 1)
    b = random.randint(0, 1)
    game = Game(player=random.randint(0, 1), ai_player=a, opp_player=b)
    # Computer v Player, at the moment
    print(game.board)
    # Player 1 initial removal

    # print("Enter x y coordinates of piece to move (player 1 initial move")
    # p1_coords = input("Format: x y: ").split()
    # p1_coords = [int(x) for x in p1_coords]
    p1_coords = game.generate_legal_moves(0) # getting first move
    k = random.randint(0, len(p1_coords) - 1)
    game.board.removePiece(p1_coords[k])
    print(p1_coords[0][0])

    # print("Enter x y coordinates of piece to move (player 2 initial move")
    # p2_coords = input("Format: x y: ").split()
    # p2_coords = [int(x) for x in p2_coords]

    p2_coords = game.generate_legal_moves(1) # getting second move
    k = random.randint(0, len(p2_coords) - 1)
    print(p2_coords[0][1])
    game.board.removePiece(p2_coords[k])
    print("Initial Board Configuration:")
    print(game.board)

    while not(game.endgame):
        if game.player_turn == 0:
            # TODO will modify later to send move to server
            game.computer_move()
        else:
            # TODO will modify later to receive move from server
            game.computer_move()
        print(game.board)


if __name__ == "__main__":

    start_time = time()
    play()
    end_time = time()
    print("Total Game Time:", end_time - start_time, "seconds")
    print("Number of CPU Board Evaluations:", static_eval_count)
    print("Average Branching Factor:", total_branches / (minimax_calls + 0.0))
    print("Number of Branches Pruned:", cutoffs)
    """
    g = Game()
    g.board.removePiece((17, 0))
    g.board.removePiece((16, 0))
    g.board.removePiece((14, 0))
    print(g.board)
    for move in g.generate_legal_moves(0):
        print(move)
    """