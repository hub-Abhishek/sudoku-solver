import numpy as np


def get_cell(sudoku, r, c):
    row_start = (r//3)*3
    row_end = row_start + 3
    col_start = (c//3)*3
    col_end = col_start + 3
    return sudoku[row_start:row_end, col_start:col_end]


def get_row_dig(sudoku, n):
    return set(list(sudoku[n]))-{0}


def get_col_dig(sudoku, n):
    return set(list(sudoku[:, n]))-{0}


def get_cell_dig(sudoku, r, c):
    cell = get_cell(sudoku, r, c)
    return set(np.unique(cell))-{0}


def possible_vals(sudoku, r, c):
    row_vals = get_row_dig(sudoku, r)
    col_vals = get_col_dig(sudoku, c)
    cell_vals = get_cell_dig(sudoku, r, c)
    return set(range(1, 10)) - cell_vals - row_vals - col_vals


def check_vals(sudoku, r, c):
    if sudoku[r, c] == 0:
        return False
    row_vals = sudoku[r]
    col_vals = sudoku[:, c]
    cell_vals = get_cell(sudoku, r, c)
    return compare(row_vals) and compare(col_vals) and compare(cell_vals)


def compare(val):
    val_to_compare = val.flatten()
    non_zeros = val_to_compare[np.flatnonzero(val_to_compare)]
    return len(list(non_zeros)) == len(list(set(non_zeros)))


def get_r_c(num):
    r = int(num // 9)
    c = int(num - 9 * r)
    return r, c


def solver(sudoku_grid, curr_choice=-1, seed=42):
    np.random.seed = seed
    curr_choice += 1
    if curr_choice == 81:
        return sudoku_grid

    r, c = get_r_c(curr_choice)

    if sudoku_grid[r, c] != 0:
        return solver(sudoku_grid, curr_choice, seed)
    else:
        curr_vals = list(possible_vals(sudoku_grid, r, c))
        if len(curr_vals) == 0:
            sudoku_grid[r, c] = 0
            return False
        sudoku_grid[r, c] = np.random.choice(curr_vals)
        curr_vals.pop(curr_vals.index(sudoku_grid[r, c]))
        while solver(sudoku_grid, curr_choice, seed) is False:
            if len(curr_vals) == 0:
                sudoku_grid[r, c] = 0
                return False
            sudoku_grid[r, c] = np.random.choice(curr_vals)
            curr_vals.pop(curr_vals.index(sudoku_grid[r, c]))
        sudoku_grid = solver(sudoku_grid, curr_choice, seed)
    return sudoku_grid


def generator(difficulty, seed=42):
    np.random.seed = seed
    difficulty = int(difficulty)
    if difficulty > 5:
        difficulty = 5
    if difficulty < 1:
        difficulty = 1
    difficulty = [.1 * i for i in range(3, 8)][difficulty-1]

    sudoku_solved_grid = solver(np.zeros([9, 9], dtype=np.int), seed=23)
    sudoku_unsolved_grid = sudoku_solved_grid.copy()

    idx = np.flatnonzero(sudoku_unsolved_grid)
    N = np.count_nonzero(sudoku_unsolved_grid != 0) - int(round(difficulty * sudoku_unsolved_grid.size ))
    np.put(sudoku_unsolved_grid, np.random.choice(idx, size=N, replace=False), 0)

    return sudoku_unsolved_grid, sudoku_solved_grid

