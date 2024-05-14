from copy import copy
from random import random
from time import sleep
import tkinter as tk
from tkinter import messagebox

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0),
              (1, 1), (-1, -1), (1, -1), (-1, 1)]


class Board:
    def __init__(self, difficulty):
        self.window = tk.Tk()
        self.window.title("Othello Game")
        self.canvas = tk.Canvas(self.window, width=600,
                                height=600, background="green")
        self.window.resizable(width=False, height=False)
        self.boardSize = 8
        self.board = [[0 for i in range(self.boardSize)]
                      for j in range(self.boardSize)]
        self.sandwichCells = []
        self.current_player = -1  # Start with black player
        self.difficulty = difficulty
        self.startBoard()
        self.createBoard()

    def startBoard(self):
        self.board[3][3] = 1
        self.board[3][4] = -1
        self.board[4][3] = -1
        self.board[4][4] = 1

    def createBoard(self):
        self.buttons = []
        for i in range(8):
            row = []
            for j in range(8):
                button = tk.Button(self.window, width=10,
                                   height=5, background="green", command=lambda i=i, j=j: self.button_clicked(i, j))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)
        self.RepresentPossibleMoves(self.current_player)
        self.colorBoard()

    def colorBoard(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 1:
                    self.buttons[i][j].configure(bg="white")
                elif self.board[i][j] == -1:
                    self.buttons[i][j].configure(bg="black")
                elif self.board[i][j] == 0:
                    self.buttons[i][j].configure(bg="green")
                elif self.board[i][j] == 2:
                    self.buttons[i][j].configure(bg="red")

    def findSandwichCells(self, current_color):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.board[i][j] == current_color:
                    for right in range(j+1, self.boardSize - 1):
                        if self.board[i][right] == 0:
                            break
                        if self.board[i][right] == current_color:
                            break
                        if self.board[i][right] == -current_color and self.board[i][right+1] == 0:
                            self.sandwichCells.append((i, right+1))

                    for left in range(j-1, 0, -1):
                        if self.board[i][left] == 0:
                            break
                        if self.board[i][left] == current_color:
                            break
                        if self.board[i][left] == -current_color and self.board[i][left-1] == 0:
                            self.sandwichCells.append((i, left-1))

                    for down in range(i+1, self.boardSize - 1):
                        if self.board[down][j] == 0:
                            break
                        if self.board[down][j] == current_color:
                            break
                        if self.board[down][j] == -current_color and self.board[down+1][j] == 0:
                            self.sandwichCells.append((down+1, j))

                    for up in range(i-1, 0, -1):
                        if self.board[up][j] == 0:
                            break
                        if self.board[up][j] == current_color:
                            break
                        if self.board[up][j] == -current_color and self.board[up-1][j] == 0:
                            self.sandwichCells.append((up-1, j))

    def RepresentPossibleMoves(self, current_color):
        self.findSandwichCells(current_color)
        if self.sandwichCells:
            for cell in self.sandwichCells:
                self.board[cell[0]][cell[1]] = 2
                self.colorBoard()
            return True
        return False

    def colorInBetween(self, i, j, currentColor):
        for right in range(j+1, self.boardSize - 1):
            if self.board[i][right] == 0:
                break
            if self.board[i][right] == currentColor:
                break
            if self.board[i][right] == -currentColor:
                self.board[i][right] = currentColor

        for left in range(j-1, 0, -1):
            if self.board[i][left] == 0:
                break
            if self.board[i][left] == currentColor:
                break
            if self.board[i][left] == -currentColor:
                self.board[i][left] = currentColor

        for down in range(i+1, self.boardSize - 1):
            if self.board[down][j] == 0:
                break
            if self.board[down][j] == currentColor:
                break
            if self.board[down][j] == -currentColor:
                self.board[down][j] = currentColor

        for up in range(i-1, 0, -1):
            if self.board[up][j] == 0:
                break
            if self.board[up][j] == currentColor:
                break
            if self.board[up][j] == -currentColor:
                self.board[up][j] = currentColor

        self.colorBoard()

    def checkWinning(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 0 or self.board[i][j] == 2:
                    return False
        return True

    def winner(self):
        black = 0
        white = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 1:
                    white += 1
                if self.board[i][j] == -1:
                    black += 1
        if black > white:
            messagebox.showinfo(
                "Message", "Black Wins! black: {} white: {}".format(black, white))
        elif white > black:
            messagebox.showinfo(
                "Message", "White Wins!" "black: {} white: {}".format(black, white))
        else:
            messagebox.showinfo("Message", "It's a tie!")

    def UpdateBoard(self, i, j):
        currentColor = self.current_player
        if self.RepresentPossibleMoves(currentColor):
            if self.board[i][j] == 2:
                self.board[i][j] = currentColor
                self.colorInBetween(i, j, currentColor)
                self.current_player *= -1
                self.clearRed()
                if self.RepresentPossibleMoves(self.current_player) == False:
                    self.current_player *= -1
                    if self.RepresentPossibleMoves(self.current_player) == False:
                        self.winner()

            else:
                messagebox.showinfo(
                    "Message", "Invalid move! No Sandwich Relationship.")
                self.colorBoard()
                self.current_player *= 1

        elif self.checkWinning():
            self.winner()

    def clearRed(self):
        self.sandwichCells.clear()
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 2:
                    self.board[i][j] = 0
        self.colorBoard()

    def button_clicked(self, row, col):
        self.UpdateBoard(row, col)
        self.RepresentPossibleMoves(self.current_player)
        # if not self.checkWinning():
        #     self.computerMove()

    def utility(self):
        currentColor = self.current_player
        score = 0
        nextColor = -currentColor

        for i in self.board:
            for cell in i:
                if cell == currentColor:
                    score += 1
                elif cell == nextColor:
                    score -= 1
        return score

# Inside the Board class

    def computerMove(self):
        sleep(1)
        bestMove = self.getBestMove()
        if bestMove is not None:
            self.makeMove(bestMove[0], bestMove[1])
        else:
            print("No valid move found for the computer.")

    def alphaBeta(self, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.gameOver():
            return self.evaluate()

        if maximizingPlayer:
            maxEval = float('-inf')
            ValidMoves = self.getValidMoves()

            for move in ValidMoves:
                tempBoard = copy.deepcopy(self)
                tempBoard.makeMove(move[0], move[1])
                maxEval = max(maxEval, tempBoard.alphaBeta(
                    depth - 1, alpha, beta, False))
                alpha = max(alpha, maxEval)
                if beta <= alpha:
                    break
            return maxEval
        else:

            minEval = float('inf')
            ValidMoves = self.getValidMoves(-self.current_player)

            for move in ValidMoves:
                tempBoard = copy.deepcopy(self)
                tempBoard.makeMove(move[0], move[1])
                minEval = min(minEval, tempBoard.alphaBeta(
                    depth - 1, alpha, beta, True))
                beta = min(beta, minEval)
                if beta <= alpha:
                    break
            return minEval

    def isValidMove(self, row, col):
        if self.board[row][col] != 0:
            return False
        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == -self.current_player:
                while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == -self.current_player:
                    r += dr
                    c += dc
                if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                    return True
        return False

    def makeMove(self, row, col):
        if not self.isValidMove(row, col):
            return False
        self.board[row][col] = self.current_player

        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == -self.current_player:
                while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == -self.current_player:
                    r += dr
                    c += dc

                if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                    while True:
                        r -= dr
                        c -= dc
                        if r == row and c == col:
                            break
                        self.board[r][c] = self.current_player
        return True

    def getValidMoves(self):
        ValidMoves = []
        for i in range(8):
            for j in range(8):
                if self.isValidMove(i, j):
                    ValidMoves.append((i, j))
        return ValidMoves

    def getBestMove(self):
        print("Computer's turn")
        if self.difficulty == 1:
            depth = 1
        elif self.difficulty == 2:
            depth = 3
        elif self.difficulty == 3:
            depth = 5
        bestMove = None
        maxEval = float('-inf')
        ValidMoves = self.getValidMoves()
        for move in ValidMoves:
            tempBoard = copy.deepcopy(self)
            tempBoard.makeMove(move[0], move[1])
            eval = tempBoard.alphaBeta(
                depth, float('-inf'), float('inf'), False)
            if eval > maxEval:
                maxEval = eval
                bestMove = move
        return bestMove


def main():
    difficulty = int(
        input("Enter the difficulty level: 1-Easy, 2-Medium, 3-Hard: "))
    board = Board(difficulty)
    while not board.checkWinning():
        if board.current_player == -1:
            board.computerMove()
        elif board.current_player == 1:
            board.window.update()

        if board.checkWinning():
            break

    board.window.mainloop()


if __name__ == "__main__":
    main()
