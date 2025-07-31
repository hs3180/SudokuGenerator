import unittest
from sudoku.generator import SudokuGenerator

class TestSudokuGenerator(unittest.TestCase):
    def test_generate_complete_grid(self):
        gen = SudokuGenerator(9)
        grid = gen.generate_complete_grid()
        self.assertEqual(len(grid), 9)
        self.assertTrue(all(len(row) == 9 for row in grid))

    def test_6x6_blocks(self):
        gen = SudokuGenerator(6)
        grid = gen.generate_complete_grid()
        self.assertEqual(len(grid), 6)
        self.assertTrue(all(len(row) == 6 for row in grid))
        # 检查每个3x2 block
        for box_row in range(0, 6, 2):
            for box_col in range(0, 6, 3):
                nums = set()
                for r in range(box_row, box_row + 2):
                    for c in range(box_col, box_col + 3):
                        nums.add(grid[r][c])
                self.assertEqual(nums, set(range(1, 7)), f"Block at ({box_row},{box_col}) invalid: {nums}")
        # 检查每行唯一
        for row in grid:
            self.assertEqual(set(row), set(range(1, 7)), f"Row invalid: {row}")
        # 检查每列唯一
        for col in range(6):
            col_vals = set(grid[row][col] for row in range(6))
            self.assertEqual(col_vals, set(range(1, 7)), f"Col {col} invalid: {col_vals}")

    def test_6x6_puzzle_validity(self):
        gen = SudokuGenerator(6)
        solution = gen.generate_complete_grid()
        puzzle = gen.remove_numbers(solution, 'normal')
        # 检查每个3x2 block非零数字无重复
        for box_row in range(0, 6, 2):
            for box_col in range(0, 6, 3):
                nums = [puzzle[r][c] for r in range(box_row, box_row + 2) for c in range(box_col, box_col + 3) if puzzle[r][c] != 0]
                self.assertEqual(len(nums), len(set(nums)), f"Block at ({box_row},{box_col}) has duplicates: {nums}")
        # 检查每行非零数字无重复
        for row in puzzle:
            nums = [n for n in row if n != 0]
            self.assertEqual(len(nums), len(set(nums)), f"Row has duplicates: {row}")
        # 检查每列非零数字无重复
        for col in range(6):
            col_vals = [puzzle[row][col] for row in range(6) if puzzle[row][col] != 0]
            self.assertEqual(len(col_vals), len(set(col_vals)), f"Col {col} has duplicates: {col_vals}")

    def test_puzzle_solvability(self):
        """Test that generated puzzles are solvable."""
        for size in [4, 6, 9]:
            gen = SudokuGenerator(size)
            for difficulty in ['easy', 'normal', 'hard']:
                # 添加重试机制，因为生成可能偶尔失败
                max_attempts = 5
                for attempt in range(max_attempts):
                    try:
                        puzzle, solution = gen.generate_puzzle(difficulty)
                        break
                    except RuntimeError as e:
                        if attempt == max_attempts - 1:
                            self.fail(f"Failed to generate puzzle after {max_attempts} attempts for size {size}, difficulty {difficulty}: {e}")
                        continue
                
                # 验证谜题有解
                test_puzzle = [row[:] for row in puzzle]  # 深拷贝
                self.assertTrue(gen.solve(test_puzzle), 
                               f"Puzzle for size {size}, difficulty {difficulty} is not solvable")
                
                # 验证解是正确的
                for row in range(size):
                    for col in range(size):
                        if puzzle[row][col] != 0:
                            self.assertEqual(test_puzzle[row][col], puzzle[row][col],
                                           f"Solution doesn't preserve given numbers at ({row}, {col})")

    def test_unique_solution(self):
        """Test that puzzles have unique solutions when required."""
        gen = SudokuGenerator(9)
        gen.require_unique_solution = True
        
        puzzle, solution = gen.generate_puzzle('normal')
        solution_count = gen.count_solutions(puzzle, 3)
        self.assertEqual(solution_count, 1, 
                        f"Puzzle should have exactly 1 solution, but found {solution_count}")

if __name__ == '__main__':
    unittest.main() 