import unittest
from sudoku.generator import SudokuGenerator

class TestSudokuGenerator(unittest.TestCase):
    def test_generate_complete_grid(self):
        gen = SudokuGenerator(9)
        grid = gen.generate_complete_grid()
        self.assertEqual(len(grid), 9)
        self.assertTrue(all(len(row) == 9 for row in grid))

if __name__ == '__main__':
    unittest.main() 