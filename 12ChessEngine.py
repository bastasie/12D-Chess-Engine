self.color =import random
import chess
import chess.engine
import sys
import time
import argparse
import os

# Define the 12D Chess Board and Piece Classes
class Board12D:
    def __init__(self):
        self.board = {}
        self.king_moved = {'White': False, 'Black': False}
        self.rook_moved = {'White': [False, False], 'Black': [False, False]}
        self.turn = 'White'
        self.game_over = False

    def place_piece(self, piece, position):
        self.board[position] = piece

    def move_piece(self, from_position, to_position):
        if self.game_over:
            raise ValueError("The game is over")
        piece = self.get_piece(from_position)
        if not piece:
            raise ValueError("No piece at the from_position.")
        if piece.color != self.turn:
            raise ValueError("It's not your turn")
        if to_position not in piece.valid_moves(from_position, self):
            raise ValueError("Invalid move")

        self.board[to_position] = self.board.pop(from_position)
        if isinstance(piece, Pawn):
            piece.promote(to_position, self, Queen(piece.color))

        self.turn = 'Black' if self.turn == 'White' else 'White'
        self.check_for_checkmate()

    def get_piece(self, position):
        return self.board.get(position, None)

    def is_in_check(self, color):
        king_position = None
        for pos, piece in self.board.items():
            if isinstance(piece, King) and piece.color == color:
                king_position = pos
                break
        if not king_position:
            return False
        for pos, piece in self.board.items():
            if piece.color != color:
                if king_position in piece.valid_moves(pos, self):
                    return True
        return False

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False
        for pos, piece in self.board.items():
            if piece.color == color:
                for move in piece.valid_moves(pos, self):
                    original_position = pos
                    original_piece = self.get_piece(move)
                    self.board[move] = self.board.pop(pos)
                    if not self.is_in_check(color):
                        self.board[original_position] = self.board.pop(move)
                        if original_piece:
                            self.board[move] = original_piece
                        return False
                    self.board[original_position] = self.board.pop(move)
                    if original_piece:
                        self.board[move] = original_piece
        return True

    def check_for_checkmate(self):
        if self.is_checkmate('White'):
            print("Checkmate! Black wins!")
            self.game_over = True
        elif self.is_checkmate('Black'):
            print("Checkmate! White wins!")
            self.game_over = True

    def can_castle(self, color, rook_side):
        if self.game_over:
            return False

        king_position = None
        rook_position = None
        for pos, piece in self.board.items():
            if isinstance(piece, King) and piece.color == color:
                king_position = pos
            elif isinstance(piece, Rook) and piece.color == color:
                if rook_side == 'kingside' and pos[0] == 7:
                    rook_position = pos
                elif rook_side == 'queenside' and pos[0] == 0:
                    rook_position = pos

        if not king_position or not rook_position:
            return False

        if self.king_moved[color]:
            return False

        if rook_side == 'kingside' and self.rook_moved[color][1]:
            return False
        elif rook_side == 'queenside' and self.rook_moved[color][0]:
            return False

        if self.is_in_check(color):
            return False

        if rook_side == 'kingside':
            positions_between = [(i, king_position[1], *king_position[2:]) for i in range(king_position[0] + 1, 7)]
        else:
            positions_between = [(i, king_position[1], *king_position[2:]) for i in range(1, king_position[0])]

        for pos in positions_between:
            if self.get_piece(pos) or self.is_in_check_at_position(color, pos):
                return False

        return True

    def castle(self, color, rook_side):
        if not self.can_castle(color, rook_side):
            raise ValueError("Castling conditions not met")

        king_position = None
        rook_position = None
        for pos, piece in self.board.items():
            if isinstance(piece, King) and piece.color == color:
                king_position = pos
            elif isinstance(piece, Rook) and piece.color == color:
                if rook_side == 'kingside' and pos[0] == 7:
                    rook_position = pos
                elif rook_side == 'queenside' and pos[0] == 0:
                    rook_position = pos

        if rook_side == 'kingside':
            new_king_position = (6, king_position[1], *king_position[2:])
            new_rook_position = (5, rook_position[1], *rook_position[2:])
        else:
            new_king_position = (2, king_position[1], *king_position[2:])
            new_rook_position = (3, rook_position[1], *rook_position[2:])

        self.board[new_king_position] = self.board.pop(king_position)
        self.board[new_rook_position] = self.board.pop(rook_position)

    def is_in_check_at_position(self, color, position):
        for pos, piece in self.board.items():
            if piece.color != color:
                if position in piece.valid_moves(pos, self):
                    return True
        return False

    def print_board(self):
        board_2d = [['.' for _ in range(8)] for _ in range(8)]
        for pos, piece in self.board.items():
            x, y = pos[0], pos[1]
            board_2d[y][x] = piece.symbol()
        print("  a b c d e f g h")
        for i, row in enumerate(board_2d):
            print(f"{8 - i} {' '.join(row)} {8 - i}")
        print("  a b c d e f g h\n")

# Define piece classes with the previous logic
class King:
    def __init__(self, color):
        self.color = color

    def valid_moves(self, position, board):
        valid_moves = []
        for i in range(12):
            for sign in [-1, 1]:
                new_position = list(position)
                new_position[i] += sign
                new_position = tuple(new_position)
                if self.is_valid_position(new_position) and not board.get_piece(new_position):
                    valid_moves.append(new_position)
        return valid_moves

    @staticmethod
    def is_valid_position(position):
        return all(0 <= x < 8 for x in position[:2])

    def symbol(self):
        return 'K' if self.color == 'White' else 'k'

class Rook:
    def __init__(self, color):
        self.color = color

    def valid_moves(self, position, board):
        valid_moves = []
        for i in range(12):
            for delta in range(1, 8):
                for sign in [-1, 1]:
                    new_position = list(position)
                    new_position[i] += sign * delta
                    new_position = tuple(new_position)
                    if self.is_valid_position(new_position) and not board.get_piece(new_position):
                        valid_moves.append(new_position)
                    else:
                        break
        return valid_moves

    @staticmethod
    def is_valid_position(position):
        return all(0 <= x < 8 for x in position[:2])

    def symbol(self):
        return 'R' if self.color == 'White' else 'r'

class Bishop:
    def __init__(self, color):
        self.color = color

    def valid_moves(self, position, board):
        valid_moves = []
        for i in range(12):
            for j in range(i + 1, 12):
                for delta in range(1, 8):
                    for sign1 in [-1, 1]:
                        for sign2 in [-1, 1]:
                            new_position = list(position)
                            new_position[i] += sign1 * delta
                            new_position[j] += sign2 * delta
                            new_position = tuple(new_position)
                            if self.is_valid_position(new_position) and not board.get_piece(new_position):
                                valid_moves.append(new_position)
                            else:
                                break
        return valid_moves

    @staticmethod
    def is_valid_position(position):
        return all(0 <= x < 8 for x in position[:2])

    def symbol(self):
        return 'B' if self.color == 'White' else 'b'

class Queen:
    def __init__(self, color):
        self.color = color
        self.rook = Rook(color)
        self.bishop = Bishop(color)

    def valid_moves(self, position, board):
        return self.rook.valid_moves(position, board) + self.bishop.valid_moves(position, board)

    def symbol(self):
        return 'Q' if = 'White' else 'q'

class Knight:
    def __init__(self, color):
        self.color = color
        self.moves = self.generate_knight_moves()

    def generate_knight_moves(self):
        moves = []
        for i in range(12):
            for j in range(i + 1, 12):
                moves.extend([
                    self.create_move(i, j, 2, 1),
                    self.create_move(i, j, 2, -1),
                    self.create_move(i, j, -2, 1),
                    self.create_move(i, j, -2, -1),
                    self.create_move(i, j, 1, 2),
                    self.create_move(i, j, 1, -2),
                    self.create_move(i, j, -1, 2),
                    self.create_move(i, j, -1, -2)
                ])
        return moves

    def create_move(self, i, j, a, b):
        move = [0] * 12
        move[i] = a
        move[j] = b
        return tuple(move)

    def valid_moves(self, position, board):
        valid_moves = []
        for move in self.moves:
            new_position = tuple(pos + delta for pos, delta in zip(position, move))
            if self.is_valid_position(new_position) and not board.get_piece(new_position):
                valid_moves.append(new_position)
        return valid_moves

    @staticmethod
    def is_valid_position(position):
        return all(0 <= x < 8 for x in position[:2])

    def symbol(self):
        return 'N' if self.color == 'White' else 'n'

class Pawn:
    def __init__(self, color):
        self.color = color

    def valid_moves(self, position, board):
        valid_moves = []
        direction = 1 if self.color == 'White' else -1

        # Forward move
        forward_one = list(position)
        forward_one[0] += direction
        forward_one = tuple(forward_one)
        if self.is_valid_position(forward_one) and not board.get_piece(forward_one):
            valid_moves.append(forward_one)

            # Forward two if it's the first move
            if (self.color == 'White' and position[0] == 1) or (self.color == 'Black' and position[0] == 6):
                forward_two = list(position)
                forward_two[0] += 2 * direction
                forward_two = tuple(forward_two)
                if self.is_valid_position(forward_two) and not board.get_piece(forward_two):
                    valid_moves.append(forward_two)

        # Captures
        for i in range(1, 12):
            capture = list(position)
            capture[0] += direction
            capture[i] += 1
            capture = tuple(capture)
            if self.is_valid_position(capture) and board.get_piece(capture) and board.get_piece(capture).color != self.color:
                valid_moves.append(capture)

            capture = list(position)
            capture[0] += direction
            capture[i] -= 1
            capture = tuple(capture)
            if self.is_valid_position(capture) and board.get_piece(capture) and board.get_piece(capture).color != self.color:
                valid_moves.append(capture)

        return valid_moves

    def promote(self, position, board, new_piece):
        if (self.color == 'White' and position[0] == 7) or (self.color == 'Black' and position[0] == 0):
            board.board[position] = new_piece

    @staticmethod
    def is_valid_position(position):
        return all(0 <= x < 8 for x in position[:2])

    def symbol(self):
        return 'P' if self.color == 'White' else 'p'

# AI Player class for the 12D AI system
class AIPlayer:
    def __init__(self, color, depth=3):
        self.color = color
        self.depth = depth

    def get_best_move(self, board):
        best_move = None
        best_value = -float('inf') if self.color == chess.WHITE else float('inf')
        
        for move in board.legal_moves:
            board.push(move)
            board_value = self.minimax(board, self.depth - 1, -float('inf'), float('inf'), board.turn != self.color)
            board.pop()
            
            if self.color == chess.WHITE and board_value > best_value:
                best_value = board_value
                best_move = move
            elif self.color == chess.BLACK and board_value < best_value:
                best_value = board_value
                best_move = move
        
        return best_move

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)
        
        if is_maximizing:
            max_eval = -float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_board(self, board):
        material_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        evaluation = 0
        for piece_type in material_values:
            evaluation += len(board.pieces(piece_type, chess.WHITE)) * material_values[piece_type]
            evaluation -= len(board.pieces(piece_type, chess.BLACK)) * material_values[piece_type]
        return evaluation

def randomize_opening_moves(board, num_moves=2):
    openings = [
        ["e2e4", "e7e5", "g1f3", "b8c6"],  # King's Pawn Opening
        ["d2d4", "d7d5", "c2c4", "e7e6"],  # Queen's Gambit
        ["c2c4", "e7e5", "g1f3", "b8c6"],  # English Opening
        ["g1f3", "d7d5", "g2g3", "c8f5"],  # Reti Opening
        ["e2e4", "c7c5", "g1f3", "d7d6"],  # Sicilian Defense
        ["e2e4", "e7e6", "d2d4", "d7d5"],  # French Defense
        ["e2e4", "c7c6", "d2d4", "d7d5"],  # Caro-Kann Defense
        ["e2e4", "e7e5", "f2f4", "e5f4"],  # King's Gambit
        ["d2d4", "g8f6", "c2c4", "e7e6"],  # Nimzo-Indian Defense
        ["d2d4", "d7d5", "c2c4", "c7c6"],  # Slav Defense
        ["e2e4", "e7e5", "g1f3", "f8c5"],  # Italian Game
        ["e2e4", "e7e5", "g1f3", "f8b4"],  # Ruy Lopez
        ["e2e4", "c7c5", "f1b5", "a7a6"],  # Sicilian Defense, Rossolimo
        ["d2d4", "d7d5", "c2c4", "c7c6"],  # Semi-Slav Defense
        ["d2d4", "d7d5", "g1f3", "g8f6"],  # Queen's Gambit Declined
        ["d2d4", "d7d5", "c2c4", "e7e5"],  # Albin Countergambit
        ["e2e4", "e7e5", "g1f3", "g8f6"],  # Petrov's Defense
        ["d2d4", "d7d5", "c2c4", "d5c4"],  # Queen's Gambit Accepted
        ["e2e4", "d7d6", "d2d4", "g8f6"],  # Pirc Defense
        ["e2e4", "g8f6", "e4e5", "f6d5"],  # Alekhine's Defense
        ["e2e4", "c7c5", "d2d4", "c5d4"],  # Sicilian Defense, Open
        ["e2e4", "e7e5", "g1f3", "g8c6"],  # Four Knights Game
        ["e2e4", "e7e5", "d2d4", "e5d4"],  # Scotch Game
        ["c2c4", "e7e5", "g1f3", "e5e4"],  # English Opening, Reversed Sicilian
        ["d2d4", "f7f5", "g1f3", "g8f6"],  # Dutch Defense
        ["e2e4", "c7c6", "d2d4", "d7d5"],  # Caro-Kann Defense
        ["e2e4", "e7e5", "f2f4", "e5f4"],  # King's Gambit Accepted
        ["e2e4", "e7e5", "f2f4", "e5e4"],  # King's Gambit Declined
        ["d2d4", "g8f6", "c2c4", "e7e5"],  # Budapest Gambit
        ["d2d4", "d7d5", "c2c4", "c7c6"],  # Slav Defense, Exchange Variation
        ["e2e4", "e7e5", "g1f3", "g8f6"],  # Russian Game
        ["e2e4", "c7c5", "g1f3", "d7d6"],  # Sicilian Defense, Najdorf Variation
        ["d2d4", "d7d5", "c2c4", "e7e6"],  # Queen's Gambit Declined, Orthodox Defense
        ["d2d4", "g8f6", "c2c4", "d7d6"],  # King's Indian Defense
        ["e2e4", "e7e5", "f1c4", "g8f6"],  # Italian Game, Two Knights Defense
        ["e2e4", "e7e6", "d2d4", "d7d5"],  # French Defense, Tarrasch Variation
        ["e2e4", "e7e6", "d2d4", "d7d5"],  # French Defense, Advance Variation
        ["e2e4", "e7e6", "d2d4", "d7d5"],  # French Defense, Winawer Variation
        ["d2d4", "d7d5", "c2c4", "c7c6"],  # Slav Defense, Czech Variation
        ["e2e4", "c7c5", "d2d4", "c5d4"],  # Sicilian Defense, Smith-Morra Gambit
        ["d2d4", "d7d5", "g1f3", "g8f6"],  # Queen's Gambit Declined, Exchange Variation
        ["e2e4", "c7c5", "g1f3", "e7e6"],  # Sicilian Defense, French Variation
        ["d2d4", "d7d5", "c2c4", "d5c4"],  # Queen's Gambit Accepted
        ["e2e4", "c7c5", "f1b5", "a7a6"],  # Sicilian Defense, Canal Attack
        ["d2d4", "g8f6", "c2c4", "e7e5"],  # Budapest Gambit
        ["d2d4", "g8f6", "c2c4", "g7g6"],  # King's Indian Defense, Fianchetto
        ["d2d4", "d7d5", "g1f3", "g8f6"],  # Queen's Gambit Declined, Tartakower
        ["e2e4", "e7e5", "g1f3", "d7d6"],  # Philidor Defense
        ["e2e4", "e7e5", "g1f3", "d7d6"],  # Modern Defense
        ["e2e4", "c7c5", "f1b5", "a7a6"],  # Sicilian Defense, Moscow Variation
        ["d2d4", "g8f6", "c2c4", "e7e5"],  # Budapest Gambit
        ["d2d4", "g8f6", "c2c4", "g7g6"],  # King's Indian Defense, Fianchetto
        ["d2d4", "d7d5", "g1f3", "g8f6"],  # Queen's Gambit Declined, Tartakower
        ["e2e4", "c7c5", "f1b5", "a7a6"],  # Sicilian Defense, Rossolimo
        ["e2e4", "c7c5", "f1b5", "a7a6"],  # Sicilian Defense, Moscow
        ["e2e4", "e7e5", "f1b5", "a7a6"],  # Ruy Lopez, Morphy Defense
        ["e2e4", "e7e5", "g1f3", "b8c6"],  # Four Knights Game, Scotch Variation
        ["e2e4", "c7c5", "f1b5", "a7a6"],  # Sicilian Defense, Moscow
        ["d2d4", "g8f6", "c2c4", "e7e5"],  # Budapest Gambit
        ["d2d4", "g8f6", "c2c4", "g7g6"],  # King's Indian Defense, Fianchetto
        ["d2d4", "d7d5", "g1f3", "g8f6"],  # Queen's Gambit Declined, Tartakower
        ["e2e4", "c7c5", "f1b5", "a7a6"],  # Sicilian Defense, Rossolimo
        ["e2e4", "e7e5", "f1b5", "a7a6"],  # Ruy Lopez, Morphy Defense
        ["e2e4", "e7e5", "g1f3", "b8c6"],  # Four Knights Game, Scotch Variation
    ]
    
    opening = random.choice(openings)
    for move in opening[:num_moves * 2]:  # Apply first 'num_moves' moves for both players
        board.push_san(move)

def watch_12d_vs_stockfish(thinking_time, num_games, stockfish_depth=None):
    for i in range(num_games):
        print(f"Game {i + 1} of {num_games}")
        seed = int(time.time()) + i  # Generate a unique seed for each game
        play_game(thinking_time, watch=True, seed=seed, stockfish_depth=stockfish_depth)

def play_game(thinking_time=10.0, watch=False, seed=None, stockfish_depth=None):
    if seed is not None:
        random.seed(seed)
    
    # Initialize the python-chess board and engine
    board = chess.Board()

    # If watching 12D AI vs Stockfish, randomize the opening moves
    if watch:
        randomize_opening_moves(board)

    # If playing against 12D AI, initialize the board with only one move by 12D AI
    else:
        white_ai = AIPlayer(chess.WHITE, depth=3)
        move = white_ai.get_best_move(board)
        board.push(move)

    # Determine the correct path for the Stockfish executable
    stockfish_path = os.path.join(os.path.dirname(sys.executable), "C:/Users/NEC/Documents/Chess12/stockfish/stockfish-windows-x86-64-avx2.exe")

    try:
        engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    except PermissionError as e:
        print(f"Failed to open Stockfish engine: {e}")
        return
    except FileNotFoundError as e:
        print(f"Stockfish executable not found: {e}")
        return

    black_ai = AIPlayer(chess.BLACK, depth=3)

    while not board.is_game_over():
        if board.turn == chess.WHITE:
            if watch:
                move = white_ai.get_best_move(board)
            else:
                print(board)
                move = input("Enter your move (e.g., e2e4): ")
                try:
                    move = chess.Move.from_uci(move)
                    if move not in board.legal_moves:
                        raise ValueError
                except ValueError:
                    print("Invalid move, try again.")
                    continue
            board.push(move)
        else:
            if watch:
                if stockfish_depth:
                    result = engine.play(board, chess.engine.Limit(depth=stockfish_depth))
                else:
                    result = engine.play(board, chess.engine.Limit(time=thinking_time))
                board.push(result.move)
            else:
                move = black_ai.get_best_move(board)
                board.push(move)

        print(board)

    engine.quit()

    # Determine the game outcome
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            print("Checkmate! Black (12D AI) wins!")
else:
            print("Checkmate! White (Stockfish) wins!" if watch else "Checkmate! White (Player) wins!")
    elif board.is_stalemate():
        print("Stalemate!")
    elif board.is_insufficient_material():
        print("Draw due to insufficient material!")
    elif board.is_seventyfive_moves():
        print("Draw due to the seventy-five move rule!")
    elif board.is_fivefold_repetition():
        print("Draw due to fivefold repetition!")
    elif board.is_variant_draw():
        print("Draw (variant-specific rules)!")
    else:
        print("Game over (other reason)!")

def main(args):
    if args.watch:
        watch_12d_vs_stockfish(args.thinking_time, args.num_games, args.stockfish_depth)
    else:
        play_game(thinking_time=args.thinking_time, watch=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="12D Chess AI")
    parser.add_argument('--watch', action='store_true', help="Watch 12D AI play against Stockfish")
    parser.add_argument('--thinking_time', type=float, default=1.0, help="Thinking time for Stockfish (in seconds)")
    parser.add_argument('--num_games', type=int, default=1, help="Number of games to play")
    parser.add_argument('--stockfish_depth', type=int, default=None, help="Depth for Stockfish engine")
    args = parser.parse_args()

    main(args)
