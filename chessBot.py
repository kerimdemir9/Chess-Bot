import chess
import chess.engine
import helper


def minimax(board, depth, alpha, beta, maximizing):
    """ Minimax algorithm with alpha-beta pruning. """
    if depth == 0 or board.is_game_over():
        return helper.evaluate_board(board)

    legal_moves = list(board.legal_moves)

    if maximizing:
        best_value = float("-inf")
        for move in legal_moves:
            board.push(move)
            value = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            best_value = max(best_value, value)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return best_value
    else:
        best_value = float("inf")
        for move in legal_moves:
            board.push(move)
            value = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            best_value = min(best_value, value)
            beta = min(beta, value)
            if beta <= alpha:
                break
        return best_value


def find_best_move(board, depth):
    """ Finds the best move using Minimax with Alpha-Beta Pruning. """
    best_move = None
    best_value = float("-inf") if board.turn == chess.WHITE else float("inf")
    original_turn = board.turn

    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, float("-inf"), float("inf"), board.turn == original_turn)
        board.pop()

        if board.turn == chess.WHITE and board_value > best_value:
            best_value = board_value
            best_move = move
        elif board.turn == chess.BLACK and board_value < best_value:
            best_value = board_value
            best_move = move

    # ✅ If no valid move was found, return a random legal move
    if best_move is None:
        best_move = next(iter(board.legal_moves), None)  # Get first legal move if exists

    return best_move


def play_chess():
    """Runs a game between a human and the bot, allowing the user to pick a side."""
    board = chess.Board()

    # Get bot difficulty level
    while True:
        depth = int(input("Enter bot difficulty level: "))
        if depth > 0:
            break
        else:
            print("Invalid input! Enter a valid number.")

    # Get player color choice
    while True:
        player_color = input("Do you want to play as White or Black? (W/B): ").strip().upper()
        if player_color in ["W", "B"]:
            player_is_white = player_color == "W"
            break
        else:
            print("Invalid choice! Enter 'W' for White or 'B' for Black.")

    print("\nGame Started!\n")
    helper.print_pretty_board(board)


    while not board.is_game_over():
        if board.turn == chess.WHITE and player_is_white or board.turn == chess.BLACK and not player_is_white:
            # Human's turn
            while True:
                try:
                    move_uci = input("Your move (in UCI format, e.g., e2e4): ").strip()
                    if move_uci == "exit":
                        print("Game exited.")
                        return

                    move = chess.Move.from_uci(move_uci)
                    if move in board.legal_moves:
                        board.push(move)
                        break
                    else:
                        print("Invalid move! Try again.")
                except ValueError:
                    print("Invalid input! Enter a move in UCI format (e.g., e2e4).")
        else:
            # Bot's turn
            print("\nBot is thinking...\n")
            bot_move = find_best_move(board, depth)
            board.push(bot_move)
            print(f"Bot played: {bot_move}")

        helper.print_pretty_board(board)

    print("Game Over!", board.result())


play_chess()