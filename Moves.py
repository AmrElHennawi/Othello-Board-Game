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
        self.board[3][3] = 1
        self.board[3][4] = -1
        self.board[4][3] = -1
        self.board[4][4] = 1
        self.current_player = -1  # Start with black player
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
                button.bind("<Button-1>", lambda event, i=i, j=j: self.Update_Board(i, j))
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
                elif self.board[i][j] == 2:
                    self.buttons[i][j].configure(bg="red")

    def find_Color_below(self, target, i, j):
        rows = 8
        # Iterate over rows starting from i+1
        for row in range(i + 1, rows):
            if self.board[row][j] == target:
                return True
        return False
    def find_Color_up(self, target, i, j):
        rows = 8
        # Iterate over rows starting from i+1
        for row in range(i - 1, rows):
            if self.board[row][j] == target:
                return True
        return False

    def find_Color_left(self, target, i, j):
        cols = 8
        # Iterate over cols starting from j+1
        for col in range(j + 1, cols):
            if self.board[i][col] == target:
                return True
        return False
    def find_Color_right(self, target, i, j):
        cols = 8
        # Iterate over cols starting from j+1
        for col in range(j - 1, cols):
            if self.board[i][col] == target:
                return True
        return False


    def find_sandwich_cells(self, i, j, current_color):
        sandwich_cells = []

        # Check horizontally for sandwich and flip
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up

        for dx, dy in directions:
            x, y = i + dx, j + dy
            temp_sandwich_cells = []

            while 0 <= x < 8 and 0 <= y < 8 and self.board[x][y] == -current_color:
                temp_sandwich_cells.append((x, y))
                x += dx
                y += dy

            if 0 <= x < 8 and 0 <= y < 8 and self.board[x][y] == current_color:
                sandwich_cells.extend(temp_sandwich_cells)

        return sandwich_cells


    def Update_Board(self, i, j):
        if self.board[i][j] == 0:
            neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
            valid_move = any(self.board[x][y] != 0 for x, y in neighbors if 0 <= x < 8 and 0 <= y < 8)

            if not valid_move:
                messagebox.showinfo("Message", "Invalid move! All neighbors are still blank.")
                self.color_board()
                self.current_player *= 1
            else:
                current_color = self.current_player
                self.board[i][j] = current_color
                opponent_color = -current_color

                sandwich_made = False

                sandwich_cells = self.find_sandwich_cells(i, j, current_color)

                if sandwich_cells:
                    for cell in sandwich_cells:
                        self.board[cell[0]][cell[1]] = 2
                        self.color_board()

                if sandwich_cells:
                    sandwich_made = True
                    for cell in sandwich_cells:
                        self.board[cell[0]][cell[1]] = current_color


                if not sandwich_made:
                    messagebox.showinfo("Message", "Invalid move! No sandwich formation.")
                    self.current_player *= 1
                    self.board[i][j] = 0

                self.color_board()
                self.current_player *= -1


def main():
    board = Board()


if __name__ == "__main__":
    main()
