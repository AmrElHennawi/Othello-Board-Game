import tkinter as tk
from tkinter import messagebox


class Board:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Othello Game")
        self.canvas = tk.Canvas(self.window, width=600,
                                height=600, background="green")
        self.window.resizable(width=True, height=True)
        self.boardSize = 8
        self.board = [[0 for i in range(self.boardSize)]
                      for j in range(self.boardSize)]
        self.sandwichCells = []
        self.current_player = -1  # Start with black player
        self.startBoard()
        self.createBoard()
        self.window.mainloop()

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
                            self.sandwichCells.append(
                                (("r"), (i, right+1)))

                    for left in range(j-1, 0, -1):
                        if self.board[i][left] == 0:
                            break
                        if self.board[i][left] == current_color:
                            break
                        if self.board[i][left] == -current_color and self.board[i][left-1] == 0:
                            self.sandwichCells.append(
                                (("l"), (i, left-1)))

                    for down in range(i+1, self.boardSize - 1):
                        if self.board[down][j] == 0:
                            break
                        if self.board[down][j] == current_color:
                            break
                        if self.board[down][j] == -current_color and self.board[down+1][j] == 0:
                            self.sandwichCells.append(
                                (("d"), (down+1, j)))

                    for up in range(i-1, 0, -1):
                        if self.board[up][j] == 0:
                            break
                        if self.board[up][j] == current_color:
                            break
                        if self.board[up][j] == -current_color and self.board[up-1][j] == 0:
                            self.sandwichCells.append(
                                (("u"), (up-1, j)))

    def RepresentPossibleMoves(self, current_color):
        self.findSandwichCells(current_color)
        if self.sandwichCells:
            for cell in self.sandwichCells:
                self.board[cell[1][0]][cell[1][1]] = 2
                self.colorBoard()
            return True
        return False

    def colorInBetween(self, i, j, currentColor):
        for cell in self.sandwichCells:
            if cell[0][0] == "r":
                for right in range(j+1, cell[1][1]):
                    if self.board[i][right] == -currentColor:
                        self.board[i][right] = currentColor
            if cell[0][0] == "l":
                for left in range(j-1, cell[1][1], -1):
                    if self.board[i][left] == -currentColor:
                        self.board[i][left] = currentColor
            if cell[0][0] == "d":
                for down in range(i+1, cell[1][0]):
                    if self.board[down][j] == -currentColor:
                        self.board[down][j] = currentColor
            if cell[0][0] == "u":
                for up in range(i-1, cell[1][0], -1):
                    if self.board[up][j] == -currentColor:
                        self.board[up][j] = currentColor
        self.colorBoard()

    def UpdateBoard(self, i, j):
        currentColor = self.current_player
        if self.RepresentPossibleMoves(currentColor):
            if self.board[i][j] == 2:
                self.board[i][j] = currentColor
                self.current_player *= -1
                self.colorInBetween(i, j, currentColor)
                self.clearRed()
            else:
                messagebox.showinfo(
                    "Message", "Invalid move! No Sandwich Relationship.")
                self.colorBoard()
                self.current_player *= 1

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


def main():
    board = Board()


if __name__ == "__main__":
    main()
