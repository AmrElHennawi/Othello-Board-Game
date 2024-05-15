import copy
from tkinter import messagebox
from tkinter import simpledialog
import tkinter as tk

EMPTY = 0
BLACK = 1
WHITE = 2

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class GUI:
    def __init__(self, board, game):
        self.window = tk.Tk()
        self.window.title("Othello Game")
        self.canvas = tk.Canvas(self.window, width=600,
                                height=600, background="green")
        self.window.resizable(width=False, height=False)
        self.createBoard(board)
        self.clicked_row = None
        self.clicked_col = None
        self.game = game

    def createBoard(self, board):
        self.buttons = []
        for i in range(8):
            row = []
            for j in range(8):
                button = tk.Button(self.window, width=10,
                                   height=5, background="green", command=lambda i=i, j=j: self.button_clicked(i, j))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)
        self.colorBoard(board)

    def colorBoard(self, board):
        for i in range(8):
            for j in range(8):
                if board[i][j] == BLACK:
                    self.buttons[i][j].config(background="black")
                elif board[i][j] == WHITE:
                    self.buttons[i][j].config(background="white")

    def clearInputs(self):
        self.clicked_row = None
        self.clicked_col = None

    def button_clicked(self, row, col):
        ValidMoves = self.game.getValidMoves(WHITE)
        if (row, col) in ValidMoves:
            self.clicked_row = row
            self.clicked_col = col
        else:
            messagebox.showinfo("Invalid Move", "Invalid move. Try again.")

    def colorValidMoves(self, ValidMoves):
        for i in range(8):
            for j in range(8):
                if (i, j) in ValidMoves:
                    self.buttons[i][j].config(background="red")

    def clearRed(self):
        for i in range(8):
            for j in range(8):
                self.buttons[i][j].config(background="green")


class Othello:
    def __init__(self):
        self.board = [[EMPTY] * 8 for _ in range(8)]
        self.board[3][3] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[4][4] = WHITE
        self.currentPlayer = BLACK

    def getBoard(self):
        return self.board

    def printBoard(self):
        print("  0 1 2 3 4 5 6 7")
        for i in range(8):
            print(i, end=' ')
            for j in range(8):
                if self.board[i][j] == EMPTY:
                    print('. ', end='')
                elif self.board[i][j] == BLACK:
                    print('B ', end='')
                else:
                    print('W ', end='')
            print()

    def isValidMove(self, row, col, player):
        if self.board[row][col] != EMPTY:
            return False
        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == 3 - player:
                while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == 3 - player:
                    r += dr
                    c += dc
                if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == player:
                    return True
        return False

    def makeMove(self, row, col, player):

        if not self.isValidMove(row, col, player):
            return False
        self.board[row][col] = player

        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == 3 - player:
                while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == 3 - player:
                    r += dr
                    c += dc

                if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == player:
                    while True:
                        r -= dr
                        c -= dc
                        if r == row and c == col:
                            break
                        self.board[r][c] = player
        return True

    def countDiscs(self, player):
        count = 0
        for row in self.board:
            count += row.count(player)
        return count

    def gameOver(self):

        if self.countDiscs(BLACK) >= 32 or self.countDiscs(WHITE) >= 32:
            return True

        return self.countDiscs(BLACK) == 0 or self.countDiscs(WHITE) == 0 or self.countDiscs(EMPTY) == 0

    def getWinner(self):

        blackDiscs = self.countDiscs(BLACK)
        whiteDiscs = self.countDiscs(WHITE)

        if blackDiscs > whiteDiscs:
            return BLACK

        elif blackDiscs < whiteDiscs:
            return WHITE

        else:
            return EMPTY

    def getValidMoves(self, player):
        ValidMoves = []
        for i in range(8):
            for j in range(8):
                if self.isValidMove(i, j, player):
                    ValidMoves.append((i, j))
        return ValidMoves

    def switchPlayer(self):
        self.currentPlayer = 3 - self.currentPlayer

    def evaluate(self):
        currentColor = self.currentPlayer
        score = 0
        nextColor = 3 - currentColor

        for i in self.board:
            for cell in i:
                if cell == currentColor:
                    score += 1
                elif cell == nextColor:
                    score -= 1
        return score

    def alphaBeta(self, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.gameOver():
            return self.evaluate()

        if maximizingPlayer:
            maxEval = -64
            ValidMoves = self.getValidMoves(self.currentPlayer)

            for move in ValidMoves:
                tempBoard = copy.deepcopy(self)
                tempBoard.makeMove(move[0], move[1], self.currentPlayer)
                maxEval = max(maxEval, tempBoard.alphaBeta(
                    depth - 1, alpha, beta, False))
                alpha = max(alpha, maxEval)
                if beta <= alpha:
                    break
            return maxEval
        else:

            minEval = 64
            ValidMoves = self.getValidMoves(3 - self.currentPlayer)

            for move in ValidMoves:
                tempBoard = copy.deepcopy(self)
                tempBoard.makeMove(move[0], move[1], 3 - self.currentPlayer)
                minEval = min(minEval, tempBoard.alphaBeta(
                    depth - 1, alpha, beta, True))
                beta = min(beta, minEval)
                if beta <= alpha:
                    break
            return minEval

    def getBestMove(self, mode):
        depth = 0
        if mode == '3':
            depth = 5
        elif mode == '2':
            depth = 3
        else:
            depth = 1

        bestMove = None
        maxEval = -64
        ValidMoves = self.getValidMoves(self.currentPlayer)

        for move in ValidMoves:
            tempBoard = copy.deepcopy(self)
            tempBoard.makeMove(move[0], move[1], self.currentPlayer)
            eval = tempBoard.alphaBeta(
                depth - 1, -64, 64, False)
            if eval > maxEval:
                maxEval = eval
                bestMove = move
        return bestMove


def main():
    game = Othello()
    board = GUI(game.getBoard(), game)
    game.printBoard()
    countSwitch = 0
    difficulty = simpledialog.askstring(
        "Input", "Choose difficulty (1-easy, 2-medium, 3-hard): ").lower()

    while difficulty not in ['1', '2', '3']:
        print("Invalid difficulty! Please choose again.")
        difficulty = simpledialog.askstring(
            "Input", "Choose difficulty (1-easy, 2-medium, 3-hard): ").lower()

    while not game.gameOver():
        print("Current Player:", "Black" if game.currentPlayer == BLACK else "White")

        if game.currentPlayer == BLACK:
            validMoves = game.getValidMoves(BLACK)
            if len(validMoves) == 0:
                countSwitch += 1
                game.switchPlayer()
                if countSwitch == 2:
                    break
                continue
            countSwitch = 0
            row, col = game.getBestMove(difficulty)
            print("Computer plays at:", row, col)

        else:
            validMoves = game.getValidMoves(WHITE)
            if len(validMoves) == 0:
                countSwitch += 1
                game.switchPlayer()
                if countSwitch == 2:
                    break
                continue
            countSwitch = 0
            board.colorValidMoves(validMoves)
            print("Valid moves:", validMoves)
            while board.clicked_row is None or board.clicked_col is None:
                board.window.update()
            row = board.clicked_row
            col = board.clicked_col
            board.clearInputs()
            board.clearRed()

        if game.makeMove(row, col, game.currentPlayer):
            board.colorBoard(game.getBoard())
            game.printBoard()
            game.switchPlayer()

        else:
            print("Invalid move. Try again.")

    winner = game.getWinner()
    if winner == BLACK:
        print("Black wins , Black discs:", game.countDiscs(
            BLACK), "White discs:", game.countDiscs(WHITE))
        messagebox.showinfo(
            "Message", "Black Wins! black: {} white: {}".format(game.countDiscs(BLACK), game.countDiscs(WHITE)))

    else:
        print("White wins , Black discs:", game.countDiscs(
            BLACK), "White discs:", game.countDiscs(WHITE))
        messagebox.showinfo(
            "Message", "White Wins! black: {} white: {}".format(game.countDiscs(BLACK), game.countDiscs(WHITE)))

    board.window.mainloop()


if __name__ == "__main__":
    main()
