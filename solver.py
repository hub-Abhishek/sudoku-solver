import numpy as np


class SudokuSolver:
    def __init__(self, seed=42):
        self.seed = seed

    @staticmethod
    def get_cell(sudoku, r, c):
        row_start = (r//3)*3
        row_end = row_start + 3
        col_start = (c//3)*3
        col_end = col_start + 3
        return sudoku[row_start:row_end, col_start:col_end]

    @staticmethod
    def get_row_dig(sudoku, n):
        return set(list(sudoku[n]))-{0}

    @staticmethod
    def get_col_dig(sudoku, n):
        return set(list(sudoku[:, n]))-{0}

    def get_cell_dig(self, sudoku, r, c):
        cell = self.get_cell(sudoku, r, c)
        return set(np.unique(cell))-{0}

    def possible_vals(self, sudoku, r, c):
        row_vals = self.get_row_dig(sudoku, r)
        col_vals = self.get_col_dig(sudoku, c)
        cell_vals = self.get_cell_dig(sudoku, r, c)
        return set(range(1, 10)) - cell_vals - row_vals - col_vals

    def check_vals(self, sudoku, r, c):
        if sudoku[r, c] == 0:
            return False
        row_vals = sudoku[r]
        col_vals = sudoku[:, c]
        cell_vals = self.get_cell(sudoku, r, c)
        return self.compare(row_vals) and self.compare(col_vals) and self.compare(cell_vals)

    @staticmethod
    def compare(val):
        val_to_compare = val.flatten()
        non_zeros = val_to_compare[np.flatnonzero(val_to_compare)]
        return len(list(non_zeros)) == len(list(set(non_zeros)))

    @staticmethod
    def get_r_c(num):
        r = int(num // 9)
        c = int(num - 9 * r)
        return r, c

    def solver(self, sudoku_grid, curr_choice=-1):
        np.random.seed = self.seed
        curr_choice += 1
        if curr_choice == 81:
            return sudoku_grid

        r, c = self.get_r_c(curr_choice)

        if sudoku_grid[r, c] != 0:
            return self.solver(sudoku_grid, curr_choice)
        else:
            curr_vals = list(self.possible_vals(sudoku_grid, r, c))
            if len(curr_vals) == 0:
                sudoku_grid[r, c] = 0
                return False
            sudoku_grid[r, c] = np.random.choice(curr_vals)
            curr_vals.pop(curr_vals.index(sudoku_grid[r, c]))
            while self.solver(sudoku_grid, curr_choice) is False:
                if len(curr_vals) == 0:
                    sudoku_grid[r, c] = 0
                    return False
                sudoku_grid[r, c] = np.random.choice(curr_vals)
                curr_vals.pop(curr_vals.index(sudoku_grid[r, c]))
            sudoku_grid = self.solver(sudoku_grid, curr_choice)
        return sudoku_grid
