from solver import SudokuSolver
import numpy as np


class SudokuGenerator(SudokuSolver):
    def __init__(self, difficulty=4, seed=42):
        super().__init__(seed)
        self.difficulty = difficulty
        self.unsolved_board, self.solved_board = self.generator(self.difficulty)
        self.unsolved_board_copy = [self.unsolved_board.copy(), self.unsolved_board.copy()]

    def copy(self):
        self.unsolved_board_copy.append(self.unsolved_board_copy[-1].copy())
        if len(self.unsolved_board_copy) > 2:
            self.unsolved_board_copy.pop(0)

    def generator(self, difficulty):
        np.random.seed = self.seed
        difficulty = int(difficulty)
        if difficulty > 5:
            difficulty = 5
        if difficulty < 1:
            difficulty = 1
        difficulty = [.1 * i for i in range(3, 8)][difficulty-1]

        sudoku_solved_grid = self.solver(np.zeros([9, 9], dtype=np.int))
        sudoku_unsolved_grid = sudoku_solved_grid.copy()

        idx = np.flatnonzero(sudoku_unsolved_grid)
        N = np.count_nonzero(sudoku_unsolved_grid != 0) - int(round(difficulty * sudoku_unsolved_grid.size ))
        np.put(sudoku_unsolved_grid, np.random.choice(idx, size=N, replace=False), 0)

        return sudoku_unsolved_grid, sudoku_solved_grid

    def print_grid(self):
        print('\n'+ '~'*11, 'Lets play Sudoku!', '~'*11, '\n')
        print('*' + '-' * 39 + '*')
        for row in range(9):
            print('||',
                  ' | '.join(str(i).replace('0',' ') for i in self.unsolved_board_copy[-1][row][:3]), "||",
                  ' | '.join(str(i).replace('0', ' ') for i in self.unsolved_board_copy[-1][row][3:6]),"||",
                  ' | '.join(str(i).replace('0', ' ') for i in self.unsolved_board_copy[-1][row][6:]),
                  '||')
            if row in [2, 5]:
                print('*' + '-' * 12 + '||'+ '-' * 11 + '||'+ '-' * 12 + '*')
        print('*' + '-' * 39 + '*')


sudoku = SudokuGenerator()
sudoku.print_grid()
