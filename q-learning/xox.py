board = ["-"] * 9
currentPlayer = 'X'
Winner = None 
gameRunning = True

def printGameState(board):
    print(board[0] + " | " + board[1] + " | " + board[2])
    print("-----------")
    print(board[3] + " | " + board[4] + " | " + board[5])
    print("-----------")
    print(board[6] + " | " + board[7] + " | " + board[8])

def get_empty_cells(board):
    return [i for i, cell in enumerate(board) if cell == "-"]

def get_cells_state(board):
    return board

def get_current_game_tuple(board):
    return tuple(board)

def playerInput(board, inp):
    global currentPlayer
    if board[inp] == "-":
        board[inp] = currentPlayer
    else:
        print("This cell is full or out of bound!")
        switchPlayer()

def checkHorizontal(board):
    global Winner
    if board[0] == board[1] == board[2] and board[2] != "-":
        Winner = board[0]
        return True
    if board[3] == board[4] == board[5] and board[5] != "-":
        Winner = board[3]
        return True
    if board[6] == board[7] == board[8] and board[8] != "-":
        Winner = board[6]
        return True

def checkRow(board):
    global Winner
    if board[0] == board[3] == board[6] and board[6] != "-":
        Winner = board[0]
        return True
    if board[1] == board[4] == board[7] and board[7] != "-":
        Winner = board[1]
        return True
    if board[2] == board[5] == board[8] and board[8] != "-":
        Winner = board[2]
        return True

def checkDiagonal(board):
    global Winner
    if (board[0] == board[4] == board[8] and board[4] != "-") or (board[2] == board[4] == board[6] and board[4] != "-"):
        Winner = board[4]
        return True

def checkWin():
    if checkHorizontal(board) or checkRow(board) or checkDiagonal(board):
        return 1 if Winner == "X" else -1
    return 0

def checkforTie(board):
    global gameRunning
    if "-" not in board:
        print("Draw")
        gameRunning = False
        return True
    return False

def switchPlayer():
    global currentPlayer
    currentPlayer = 'O' if currentPlayer == 'X' else 'X'

