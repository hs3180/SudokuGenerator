import random
import math
from typing import List, Tuple, Optional
from copy import deepcopy

class SudokuGenerator:
    def __init__(self, size: int = 9):
        """
        Initialize Sudoku generator for different grid sizes.
        
        Args:
            size: Grid size (4, 6, or 9)
        """
        if size not in [4, 6, 9]:
            raise ValueError("Size must be 4, 6, or 9")
            
        self.size = size
        self.box_height = int(math.sqrt(size)) if size == 4 or size == 9 else 2
        self.box_width = int(math.sqrt(size)) if size == 4 or size == 9 else 3
        
        # Difficulty settings: percentage of cells to remove
        self.difficulty_settings = {
            4: {'easy': 0.3, 'normal': 0.4, 'hard': 0.5},
            6: {'easy': 0.35, 'normal': 0.45, 'hard': 0.55},
            9: {'easy': 0.4, 'normal': 0.5, 'hard': 0.6}
        }
        
        # Generation settings
        self.max_attempts_multiplier = 10
        self.require_unique_solution = True
    
    def is_valid(self, grid: List[List[int]], row: int, col: int, num: int) -> bool:
        """Check if placing num at (row, col) is valid."""
        # Check row
        for c in range(self.size):
            if grid[row][c] == num:
                return False
        
        # Check column
        for r in range(self.size):
            if grid[r][col] == num:
                return False
        
        # Check box
        box_start_row = (row // self.box_height) * self.box_height
        box_start_col = (col // self.box_width) * self.box_width
        
        for r in range(box_start_row, box_start_row + self.box_height):
            for c in range(box_start_col, box_start_col + self.box_width):
                if grid[r][c] == num:
                    return False
        
        return True
    
    def solve(self, grid: List[List[int]]) -> bool:
        """Solve sudoku using backtracking."""
        for row in range(self.size):
            for col in range(self.size):
                if grid[row][col] == 0:
                    numbers = list(range(1, self.size + 1))
                    random.shuffle(numbers)
                    
                    for num in numbers:
                        if self.is_valid(grid, row, col, num):
                            grid[row][col] = num
                            
                            if self.solve(grid):
                                return True
                            
                            grid[row][col] = 0
                    
                    return False
        return True
    
    def generate_complete_grid(self) -> List[List[int]]:
        """Generate a complete valid sudoku grid."""
        grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        # 只对4x4和9x9预填对角box，6x6直接回溯生成
        if self.size in (4, 9):
            for i in range(0, self.size, max(self.box_height, self.box_width)):
                self.fill_box(grid, i, i)
        self.solve(grid)
        return grid
    
    def fill_box(self, grid: List[List[int]], row: int, col: int):
        """Fill a box with random valid numbers."""
        numbers = list(range(1, self.size + 1))
        random.shuffle(numbers)
        
        idx = 0
        for r in range(row, row + self.box_height):
            for c in range(col, col + self.box_width):
                grid[r][c] = numbers[idx]
                idx += 1
    
    def count_solutions(self, grid: List[List[int]], limit: int = 2) -> int:
        """Count number of solutions (up to limit for efficiency)."""
        def solve_count(g, count):
            if count[0] >= limit:
                return
                
            for row in range(self.size):
                for col in range(self.size):
                    if g[row][col] == 0:
                        for num in range(1, self.size + 1):
                            if self.is_valid(g, row, col, num):
                                g[row][col] = num
                                solve_count(g, count)
                                g[row][col] = 0
                        return
            count[0] += 1
        
        test_grid = deepcopy(grid)
        count = [0]
        solve_count(test_grid, count)
        return count[0]
    
    def remove_numbers(self, grid: List[List[int]], difficulty: str) -> List[List[int]]:
        """Remove numbers from complete grid to create puzzle."""
        puzzle = deepcopy(grid)
        cells_to_remove = int(self.size * self.size * self.difficulty_settings[self.size][difficulty])
        
        attempts = 0
        removed = 0
        max_attempts = cells_to_remove * self.max_attempts_multiplier
        
        while removed < cells_to_remove and attempts < max_attempts:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            
            if puzzle[row][col] != 0:
                backup = puzzle[row][col]
                puzzle[row][col] = 0
                
                # Check if puzzle still has unique solution (if required)
                if not self.require_unique_solution or self.count_solutions(puzzle, 2) == 1:
                    removed += 1
                else:
                    puzzle[row][col] = backup
            
            attempts += 1
        
        return puzzle
    
    def generate_puzzle(self, difficulty: str = 'normal') -> Tuple[List[List[int]], List[List[int]]]:
        """
        Generate a sudoku puzzle with solution.
        
        Args:
            difficulty: 'easy', 'normal', or 'hard'
            
        Returns:
            Tuple of (puzzle, solution)
        """
        if difficulty not in ['easy', 'normal', 'hard']:
            raise ValueError("Difficulty must be 'easy', 'normal', or 'hard'")
        
        solution = self.generate_complete_grid()
        puzzle = self.remove_numbers(solution, difficulty)
        
        return puzzle, solution