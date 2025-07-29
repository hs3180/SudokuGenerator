import os
from typing import List, Tuple, Optional
from sudoku.generator import SudokuGenerator

class SudokuParser:
    """Parser for reading sudoku puzzles from text files."""
    
    def __init__(self):
        pass
    
    def parse_file(self, filepath: str) -> Tuple[List[List[int]], int]:
        """
        Parse a sudoku puzzle from a text file.
        
        Args:
            filepath: Path to the text file containing the sudoku puzzle
            
        Returns:
            Tuple of (puzzle_grid, size) where puzzle_grid is a 2D list of integers
            and size is the grid size (4, 6, or 9)
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file format is invalid
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Remove empty lines and strip whitespace
        lines = [line.strip() for line in lines if line.strip()]
        
        if not lines:
            raise ValueError(f"File {filepath} is empty")
        
        # Determine grid size from first line
        first_line = lines[0]
        size = len(first_line)
        
        if size not in [4, 6, 9]:
            raise ValueError(f"Invalid grid size: {size}. Must be 4, 6, or 9")
        
        if len(lines) != size:
            raise ValueError(f"Expected {size} lines, got {len(lines)}")
        
        # Parse the grid
        grid = []
        for i, line in enumerate(lines):
            if len(line) != size:
                raise ValueError(f"Line {i+1} has {len(line)} characters, expected {size}")
            
            row = []
            for j, char in enumerate(line):
                if char == '.':
                    row.append(0)  # Empty cell
                elif char.isdigit():
                    num = int(char)
                    if num < 0 or num > size:
                        raise ValueError(f"Invalid number {num} at position ({i+1}, {j+1})")
                    row.append(num)
                else:
                    raise ValueError(f"Invalid character '{char}' at position ({i+1}, {j+1})")
            
            grid.append(row)
        
        return grid, size
    
    def validate_puzzle(self, grid: List[List[int]], size: int) -> bool:
        """
        Validate that a parsed puzzle is a valid sudoku puzzle.
        
        Args:
            grid: The puzzle grid
            size: The grid size
            
        Returns:
            True if the puzzle is valid, False otherwise
        """
        if len(grid) != size:
            return False
        
        for row in grid:
            if len(row) != size:
                return False
        
        # Check for duplicate numbers in rows, columns, and boxes
        box_height = int(size ** 0.5) if size in [4, 9] else 2
        box_width = int(size ** 0.5) if size in [4, 9] else 3
        
        # Check rows
        for row in grid:
            numbers = [num for num in row if num != 0]
            if len(numbers) != len(set(numbers)):
                return False
        
        # Check columns
        for col in range(size):
            numbers = [grid[row][col] for row in range(size) if grid[row][col] != 0]
            if len(numbers) != len(set(numbers)):
                return False
        
        # Check boxes
        for box_row in range(0, size, box_height):
            for box_col in range(0, size, box_width):
                numbers = []
                for r in range(box_row, box_row + box_height):
                    for c in range(box_col, box_col + box_width):
                        if grid[r][c] != 0:
                            numbers.append(grid[r][c])
                if len(numbers) != len(set(numbers)):
                    return False
        
        return True
    
    def solve_puzzle(self, grid: List[List[int]], size: int) -> Optional[List[List[int]]]:
        """
        Solve a sudoku puzzle and return the solution.
        
        Args:
            grid: The puzzle grid
            size: The grid size
            
        Returns:
            The solution grid, or None if no solution exists
        """
        generator = SudokuGenerator(size)
        solution = [row[:] for row in grid]  # Deep copy
        
        if generator.solve(solution):
            return solution
        else:
            return None
    
    def parse_multiple_files(self, filepaths: List[str]) -> List[Tuple[List[List[int]], List[List[int]], str, int]]:
        """
        Parse multiple sudoku files and return puzzles with solutions.
        
        Args:
            filepaths: List of file paths to parse
            
        Returns:
            List of tuples (puzzle, solution, filename, size)
        """
        puzzles = []
        
        for filepath in filepaths:
            try:
                puzzle, size = self.parse_file(filepath)
                
                if not self.validate_puzzle(puzzle, size):
                    print(f"Warning: Invalid puzzle in {filepath}, skipping...")
                    continue
                
                solution = self.solve_puzzle(puzzle, size)
                if solution is None:
                    print(f"Warning: No solution found for {filepath}, skipping...")
                    continue
                
                filename = os.path.basename(filepath)
                puzzles.append((puzzle, solution, filename, size))
                print(f"✓ Parsed {filename} ({size}×{size})")
                
            except Exception as e:
                print(f"Error parsing {filepath}: {e}")
                continue
        
        return puzzles 