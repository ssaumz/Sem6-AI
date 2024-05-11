import sys
import random # Importing the random module

# Function to print the Tic Tac Toe board 
def print_board(board):
    for row in board: 
        print(" | ".join(row))
    print("-" * 5)

# Function to check if the current player has won 
def check_winner(board, player):
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# Function to check if the board is full 
def is_full(board):
    return all(cell != ' ' for row in board for cell in row)

# Function to evaluate the board state 
def evaluate(board):
    if check_winner(board, 'X'): 
        return 1
    elif check_winner(board, 'O'): 
        return -1
    else:
        return 0

# Minimax algorithm
def minimax(board, depth, maximizing_player):
    if check_winner(board, 'X'):
        return -1
    elif check_winner(board, 'O'): 
        return 1
    elif is_full(board): 
        return 0

    if maximizing_player:
        max_eval = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
        return min_eval

# Function to find the best move using minimax
def find_best_move(board):
    if random.randint(1, 5) == 1: # Allow the human player to win once in every three plays 
        empty_cells = get_empty_cells(board)
        return random.choice(empty_cells)

    best_eval = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                eval = minimax(board, 0, False)
                board[i][j] = ' '
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)
    return best_move

# Function to get empty cells on the board 
def get_empty_cells(board):
    empty_cells = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ': 
                empty_cells.append((i, j))
    return empty_cells

# Function to play Tic Tac Toe 
def play_tic_tac_toe():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    print("Let's play Tic Tac Toe!") 
    print_board(board)

    while True:
        if current_player == 'X':
            row = int(input("Enter row (0-2): ")) 
            col = int(input("Enter column (0-2): ")) 
            if board[row][col] != ' ':
                print("Invalid move. Try again.")
                continue
            board[row][col] = 'X'
        else:
            print("Computer is thinking...")
            row, col = find_best_move(board)
            board[row][col] = 'O'

        print_board(board)
        if check_winner(board, current_player): 
            print(f"{current_player} wins!")
            break
        elif is_full(board): 
            print("It's a tie!")
            break
        current_player = 'X' if current_player == 'O' else 'O'

# Start the game
play_tic_tac_toe()
