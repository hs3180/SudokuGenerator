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
        
        # 改进的难度设置：更精确的挖空比例
        self.difficulty_settings = {
            4: {
                'very_easy': 0.25,    # 25% 挖空
                'easy': 0.35,         # 35% 挖空
                'normal': 0.45,       # 45% 挖空
                'hard': 0.55,         # 55% 挖空
                'very_hard': 0.65     # 65% 挖空
            },
            6: {
                'very_easy': 0.30,    # 30% 挖空
                'easy': 0.40,         # 40% 挖空
                'normal': 0.50,       # 50% 挖空
                'hard': 0.60,         # 60% 挖空
                'very_hard': 0.70     # 70% 挖空
            },
            9: {
                'very_easy': 0.35,    # 35% 挖空
                'easy': 0.45,         # 45% 挖空
                'normal': 0.55,       # 55% 挖空
                'hard': 0.65,         # 65% 挖空
                'very_hard': 0.75     # 75% 挖空
            }
        }
        
        # 生成设置
        self.max_attempts_multiplier = 15  # 增加尝试次数
        self.require_unique_solution = True
        self.max_solution_check_limit = 3  # 检查最多3个解
    
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
                    # Don't shuffle for solving - use deterministic order
                    
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
        
        # 对于4x4数独，直接使用回溯算法生成，不预填充
        # 对于6x6数独，直接使用回溯算法生成
        # 对于9x9数独，预填充对角box然后回溯
        if self.size == 9:
            for i in range(0, self.size, max(self.box_height, self.box_width)):
                self.fill_box(grid, i, i)
        
        if not self.solve(grid):
            raise RuntimeError("Failed to generate a complete valid sudoku grid")
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
    
    def count_solutions(self, grid: List[List[int]], limit: int = 3) -> int:
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
    
    def remove_numbers_improved(self, grid: List[List[int]], difficulty: str) -> List[List[int]]:
        """
        改进的挖空算法：更智能的挖空策略
        
        1. 先生成完整解
        2. 按难度比例挖空
        3. 确保挖空后仍有唯一解
        4. 使用更高效的挖空策略
        """
        puzzle = deepcopy(grid)
        cells_to_remove = int(self.size * self.size * self.difficulty_settings[self.size][difficulty])
        
        # 创建所有位置的列表，用于随机挖空
        all_positions = [(row, col) for row in range(self.size) for col in range(self.size)]
        random.shuffle(all_positions)
        
        removed = 0
        attempts = 0
        max_attempts = cells_to_remove * self.max_attempts_multiplier
        
        # 第一轮：尝试挖空所有目标位置
        for row, col in all_positions:
            if removed >= cells_to_remove:
                break
                
            if puzzle[row][col] != 0:
                backup = puzzle[row][col]
                puzzle[row][col] = 0
                
                # 检查是否仍有唯一解
                if self.count_solutions(puzzle, self.max_solution_check_limit) == 1:
                    removed += 1
                else:
                    # 如果没有唯一解，恢复数字
                    puzzle[row][col] = backup
                
                attempts += 1
                if attempts >= max_attempts:
                    break
        
        # 如果第一轮没有挖空足够的数字，进行第二轮尝试
        if removed < cells_to_remove and attempts < max_attempts:
            remaining_positions = [(row, col) for row in range(self.size) for col in range(self.size) 
                                 if puzzle[row][col] != 0]
            random.shuffle(remaining_positions)
            
            for row, col in remaining_positions:
                if removed >= cells_to_remove or attempts >= max_attempts:
                    break
                    
                backup = puzzle[row][col]
                puzzle[row][col] = 0
                
                # 更严格的唯一解检查
                if self.count_solutions(puzzle, self.max_solution_check_limit) == 1:
                    removed += 1
                else:
                    puzzle[row][col] = backup
                
                attempts += 1
        
        return puzzle
    
    def remove_numbers(self, grid: List[List[int]], difficulty: str) -> List[List[int]]:
        """Remove numbers from complete grid to create puzzle."""
        return self.remove_numbers_improved(grid, difficulty)
    
    def generate_puzzle(self, difficulty: str = 'normal') -> Tuple[List[List[int]], List[List[int]]]:
        """
        Generate a sudoku puzzle with solution.
        
        Args:
            difficulty: 'very_easy', 'easy', 'normal', 'hard', or 'very_hard'
            
        Returns:
            Tuple of (puzzle, solution)
        """
        valid_difficulties = ['very_easy', 'easy', 'normal', 'hard', 'very_hard']
        if difficulty not in valid_difficulties:
            raise ValueError(f"Difficulty must be one of {valid_difficulties}")
        
        # 第一步：生成完整的合法数独解
        print(f"  Generating complete solution...", end=" ", flush=True)
        solution = self.generate_complete_grid()
        print("✓")
        
        # 第二步：根据难度挖空数字
        print(f"  Creating puzzle with {difficulty} difficulty...", end=" ", flush=True)
        puzzle = self.remove_numbers(solution, difficulty)
        print("✓")
        
        # 第三步：验证挖空后的谜题
        print(f"  Verifying puzzle uniqueness...", end=" ", flush=True)
        solution_count = self.count_solutions(puzzle, self.max_solution_check_limit)
        if solution_count != 1:
            raise RuntimeError(f"Generated puzzle has {solution_count} solutions, expected 1")
        print("✓")
        
        return puzzle, solution
    
    def get_puzzle_statistics(self, puzzle: List[List[int]]) -> dict:
        """获取谜题的统计信息"""
        filled_cells = sum(1 for row in puzzle for cell in row if cell != 0)
        empty_cells = self.size * self.size - filled_cells
        fill_percentage = filled_cells / (self.size * self.size) * 100
        
        return {
            'size': self.size,
            'filled_cells': filled_cells,
            'empty_cells': empty_cells,
            'fill_percentage': fill_percentage,
            'empty_percentage': 100 - fill_percentage
        }