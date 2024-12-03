import tkinter as tk
from tkinter import messagebox


class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        """Create a 9x9 grid of entry boxes for Sudoku."""
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.root, width=2, font=("Arial", 18), justify="center")
                entry.grid(row=row, column=col, padx=5, pady=5)
                if (row // 3 + col // 3) % 2 == 0:  # Color alternating blocks
                    entry.config(bg="#e6f7ff")
                self.entries[row][col] = entry

    def create_buttons(self):
        """Create Solve and Clear buttons."""
        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.grid(row=9, column=0, columnspan=4, pady=10)

        clear_button = tk.Button(self.root, text="Clear", command=self.clear_board)
        clear_button.grid(row=9, column=5, columnspan=4, pady=10)

    def clear_board(self):
        """Clear the Sudoku board."""
        for row in self.entries:
            for entry in row:
                entry.delete(0, tk.END)

    def get_board(self):
        """Extract the Sudoku board from the GUI."""
        board = []
        for row in self.entries:
            board_row = []
            for entry in row:
                val = entry.get()
                board_row.append(int(val) if val.isdigit() else 0)
            board.append(board_row)
        return board

    def display_board(self, board):
        """Update the GUI with the solved board."""
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(board[i][j]))

    def solve(self):
        """Solve the Sudoku and update the GUI."""
        board = self.get_board()
        if solve_sudoku(board):
            self.display_board(board)
        else:
            messagebox.showerror("Error", "No solution exists!")


def solve_sudoku(board):
    """Backtracking algorithm to solve Sudoku."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:  # Empty cell
                for num in range(1, 10):  # Try numbers 1-9
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):  # Recursively solve
                            return True
                        board[row][col] = 0  # Backtrack
                return False  # No valid number found
    return True


def is_valid(board, row, col, num):
    """Check if placing num in board[row][col] is valid."""
    if any(board[row][i] == num for i in range(9)):  # Check row
        return False
    if any(board[i][col] == num for i in range(9)):  # Check column
        return False
    sub_grid_row_start, sub_grid_col_start = (row // 3) * 3, (col // 3) * 3
    for i in range(sub_grid_row_start, sub_grid_row_start + 3):
        for j in range(sub_grid_col_start, sub_grid_col_start + 3):
            if board[i][j] == num:
                return False
    return True


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
