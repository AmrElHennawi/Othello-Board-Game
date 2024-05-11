import tkinter as tk


class Board:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Othello Game")
        self.canvas = tk.Canvas(self.window, width=600,
                                height=600, background="green")
        self.window.resizable(width=False, height=False)
        self.boardSize = 8
        self.board = [[0 for i in range(self.boardSize)]
                      for j in range(self.boardSize)]
        self.board[3][3] = 1
        self.board[3][4] = -1
        self.board[4][3] = -1
        self.board[4][4] = 1
        self.create_board()
        self.window.mainloop()

    def create_board(self):
        self.buttons = []
        for i in range(8):
            row = []
            for j in range(8):
                button = tk.Button(self.window, width=10,
                                   height=5, background="green")
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)
        self.color_board()

    def color_board(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 1:
                    self.buttons[i][j].configure(bg="white")
                elif self.board[i][j] == -1:
                    self.buttons[i][j].configure(bg="black")


def main():
    board = Board()


if __name__ == "__main__":
    main()
