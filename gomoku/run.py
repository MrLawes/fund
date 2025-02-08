import tkinter as tk
from tkinter import messagebox


class Gomoku:
    def __init__(self, root):
        self.root = root
        self.root.title("五子棋")
        self.board_size = 15
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'X'
        self.canvas = tk.Canvas(root, width=600, height=600)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board()
        root.mainloop()

    def draw_board(self):
        for i in range(self.board_size):
            self.canvas.create_line(40, 40 + i * 40, 40 + (self.board_size - 1) * 40, 40 + i * 40)
            self.canvas.create_line(40 + i * 40, 40, 40 + i * 40, 40 + (self.board_size - 1) * 40)

    def on_click(self, event):
        col = (event.x - 20) // 40
        row = (event.y - 20) // 40
        if 0 <= row < self.board_size and 0 <= col < self.board_size and self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.draw_piece(row, col)
            if self.check_winner(row, col):
                messagebox.showinfo("游戏结束", f"玩家 {self.current_player} 获胜！")
                self.root.quit()
            elif self.is_full():
                messagebox.showinfo("游戏结束", "平局！")
                self.root.quit()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'

    def draw_piece(self, row, col):
        x = 40 + col * 40
        y = 40 + row * 40
        if self.current_player == 'X':
            self.canvas.create_oval(x - 18, y - 18, x + 18, y + 18, fill='black')
        else:
            self.canvas.create_oval(x - 18, y - 18, x + 18, y + 18, fill='white')

    def check_winner(self, row, col):
        player = self.board[row][col]
        # Check rows
        for i in range(max(0, col - 4), min(col + 5, self.board_size)):
            if all(self.board[row][j] == player for j in range(i, min(i + 5, self.board_size))):
                return True
        # Check columns
        for i in range(max(0, row - 4), min(row + 5, self.board_size)):
            if all(self.board[j][col] == player for j in range(i, min(i + 5, self.board_size))):
                return True
        # Check diagonals
        for i in range(max(0, row - 4), min(row + 5, self.board_size)):
            for j in range(max(0, col - 4), min(col + 5, self.board_size)):
                if all(self.board[i + k][j + k] == player for k in range(5) if 0 <= i + k < self.board_size and 0 <= j + k < self.board_size):
                    return True
                if all(self.board[i + k][j - k] == player for k in range(5) if 0 <= i + k < self.board_size and 0 <= j - k < self.board_size):
                    return True
        return False

    def is_full(self):
        return all(cell != ' ' for row in self.board for cell in row)


if __name__ == "__main__":
    root = tk.Tk()
    game = Gomoku(root)

    # [10101, 20102, 10103, 20104, ]
