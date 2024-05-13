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

    def UpdateBoard(self, i, j):
        if self.board[i][j] == 0:
            neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
            valid_move = any(
                self.board[x][y] != 0 for x, y in neighbors if 0 <= x < 8 and 0 <= y < 8)

            if not valid_move:
                messagebox.showinfo(
                    "Message", "Invalid move! All neighbors are still blank.")
                self.colorBoard()
                self.current_player *= 1
            else:
                current_color = self.current_player
                self.board[i][j] = current_color
                opponent_color = -current_color

                sandwich_made = False

                Sandwich_Moves = self.RepresentMoves(i, j, current_color)

                if not Sandwich_Moves:
                    messagebox.showinfo(
                        "Message", "Invalid move! No Sandwich Relationship.")
                    self.colorBoard()
                    self.current_player *= 1
                else:
                    sandwich_cells = self.find_sandwich_cells(
                        i, j, current_color)

                    if sandwich_cells:
                        sandwich_made = True
                        for cell in sandwich_cells:
                            self.board[cell[0]][cell[1]] = current_color

                    self.colorBoard()
                    self.current_player *= -1


def main():
    board = Board()


if __name__ == "__main__":
    main()
