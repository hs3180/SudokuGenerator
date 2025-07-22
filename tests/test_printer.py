import unittest
from sudoku.printer import SudokuPrinter

class TestSudokuPrinter(unittest.TestCase):
    def test_generate_css(self):
        printer = SudokuPrinter()
        css = printer.generate_css()
        self.assertIn('<style>', css)

if __name__ == '__main__':
    unittest.main() 