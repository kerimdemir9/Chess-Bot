import chess


UNICODE_PIECES = {
    chess.PAWN: "♙", chess.KNIGHT: "♘", chess.BISHOP: "♗",
    chess.ROOK: "♖", chess.QUEEN: "♕", chess.KING: "♔",
    chess.PAWN + 8: "♟", chess.KNIGHT + 8: "♞", chess.BISHOP + 8: "♝",
    chess.ROOK + 8: "♜", chess.QUEEN + 8: "♛", chess.KING + 8: "♚"
}


def print_pretty_board(board):
    """ Prints the chessboard with Unicode pieces and ranks/files. """
    print("\n    a  b  c  d  e  f  g  h ")
    print("   ------------------------")

    for rank in range(7, -1, -1):
        row = f"{rank + 1} | "
        for file in range(8):
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            row += (UNICODE_PIECES.get(piece.piece_type + (8 if piece.color == chess.BLACK else 0),
                                       "·") + "  ") if piece else "·  "
        print(row + f"| {rank + 1}")

    print("   ------------------------")
    print("    a  b  c  d  e  f  g  h \n")



PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 300,
    chess.ROOK: 500,
    chess.QUEEN: 1100,
    chess.KING: 2000
}

PAWN_TABLE = [
    0, 5,  10, 15, 15, 10, 5,  0,
    5, 10, 15, 25, 25, 15, 10, 5,
    0, 5,  10, 20, 20, 10,  5, 0,
    0, 0,   0, 15, 15,  0,  0, 0,
    0, 0,   0,-15,-15,  0,  0, 0,
    0,-5, -10,-20,-20,-10, -5, 0,
    5,-10,-10,-20,-20,-10,-10, 5,
    0,  0,  0,  0,  0,  0,  0, 0
]

CENTER_SQUARES = {chess.D4, chess.D5, chess.E4, chess.E5}


def piece_value(piece):
    return PIECE_VALUES.get(piece.piece_type, 0) * (1 if piece.color == chess.WHITE else -1)


def get_piece_square_bonus(piece, square):
    """ Returns positional bonus from piece-square tables. """
    if piece.piece_type == chess.PAWN:
        table = PAWN_TABLE
        index = square if piece.color == chess.WHITE else chess.square_mirror(square)
        return table[index] * (1 if piece.color == chess.WHITE else -1)
    return 0


def evaluate_mobility(board):
    """ Evaluates piece mobility (number of legal moves). """
    return (len(list(board.legal_moves)) * 0.1) * (1 if board.turn == chess.WHITE else -1)


def evaluate_king_safety(board):
    """ Penalizes exposed kings. """
    king_square = board.king(board.turn)
    safety_score = 0
    if not board.has_castling_rights(board.turn):
        safety_score -= 0.5
    return safety_score * (1 if board.turn == chess.WHITE else -1)


def evaluate_pawn_structure(board):
    """ Evaluates pawn structure for weaknesses. """
    score = 0
    for color in [chess.WHITE, chess.BLACK]:
        pawns = board.pieces(chess.PAWN, color)
        for square in pawns:
            file = chess.square_file(square)

            # Doubled pawns penalty
            if sum(1 for sq in pawns if chess.square_file(sq) == file) > 1:
                score -= 0.5

            # Isolated pawn penalty
            left_file = file - 1 if file > 0 else None
            right_file = file + 1 if file < 7 else None
            has_adjacent_pawns = any(
                chess.square_file(sq) in [left_file, right_file] for sq in pawns
            )
            if not has_adjacent_pawns:
                score -= 0.5

    return score * (1 if board.turn == chess.WHITE else -1)


def evaluate_center_control(board):
    """ Rewards control of central squares. """
    control_score = 0
    for square in CENTER_SQUARES:
        piece = board.piece_at(square)
        if piece:
            control_score += 0.2 if piece.color == chess.WHITE else -0.2
    return control_score


def evaluate_board(board):
    """ Evaluates the board position based on multiple factors. """
    if board.is_checkmate():
        return float("-inf") if board.turn else float("inf")
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    material_score = sum(piece_value(piece) for piece in board.piece_map().values())
    mobility_score = evaluate_mobility(board)
    king_safety_score = evaluate_king_safety(board)
    pawn_structure_score = evaluate_pawn_structure(board)
    center_control_score = evaluate_center_control(board)

    return material_score + mobility_score + king_safety_score + pawn_structure_score + center_control_score
