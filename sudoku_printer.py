from typing import List, Tuple
from sudoku_generator import SudokuGenerator

class SudokuPrinter:
    def __init__(self):
        self.base_css = """
        <style>
        @media print {
            @page { margin: 0.5in; }
            body { margin: 0; }
        }
        
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: white;
        }
        
        .page {
            page-break-after: always;
            width: 100%;
        }
        
        .page:last-child {
            page-break-after: avoid;
        }
        
        .puzzle-container {
            display: inline-block;
            margin: 20px;
            text-align: center;
            vertical-align: top;
        }
        
        .puzzle-title {
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .sudoku-grid {
            border: 3px solid #000;
            display: inline-block;
            background-color: white;
        }
        
        .sudoku-row {
            display: flex;
            margin: 0;
            padding: 0;
        }
        
        .sudoku-cell {
            width: 30px;
            height: 30px;
            border: 1px solid #666;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            font-weight: bold;
            background-color: white;
        }
        
        /* 4x4 grid styling */
        .grid-4x4 .sudoku-cell {
            width: 35px;
            height: 35px;
            font-size: 18px;
        }
        
        .grid-4x4 .sudoku-cell:nth-child(2n) {
            border-right: 3px solid #000;
        }
        
        .grid-4x4 .sudoku-row:nth-child(2n) .sudoku-cell {
            border-bottom: 3px solid #000;
        }
        
        /* 6x6 grid styling */
        .grid-6x6 .sudoku-cell {
            width: 32px;
            height: 32px;
            font-size: 14px;
        }
        
        .grid-6x6 .sudoku-cell:nth-child(3n) {
            border-right: 3px solid #000;
        }
        
        .grid-6x6 .sudoku-row:nth-child(2n) .sudoku-cell {
            border-bottom: 3px solid #000;
        }
        
        /* 9x9 grid styling */
        .grid-9x9 .sudoku-cell {
            width: 28px;
            height: 28px;
            font-size: 14px;
        }
        
        .grid-9x9 .sudoku-cell:nth-child(3n) {
            border-right: 3px solid #000;
        }
        
        .grid-9x9 .sudoku-row:nth-child(3n) .sudoku-cell {
            border-bottom: 3px solid #000;
        }
        
        .puzzle-info {
            font-size: 12px;
            color: #666;
            margin-top: 10px;
        }
        
        .solutions-page {
            page-break-before: always;
        }
        
        .solution-grid {
            margin: 10px;
            display: inline-block;
        }
        
        .solution-title {
            font-size: 12px;
            margin-bottom: 5px;
        }
        
        .solution-grid .sudoku-grid {
            border: 2px solid #666;
        }
        
        .solution-grid .sudoku-cell {
            font-size: 10px;
            width: 20px;
            height: 20px;
            border: 1px solid #ccc;
        }
        
        /* Solution grid specific styling */
        .solution-grid.grid-4x4 .sudoku-cell {
            width: 25px;
            height: 25px;
            font-size: 12px;
        }
        
        .solution-grid.grid-6x6 .sudoku-cell {
            width: 22px;
            height: 22px;
            font-size: 10px;
        }
        
        .solution-grid.grid-9x9 .sudoku-cell {
            width: 18px;
            height: 18px;
            font-size: 8px;
        }
        
        h1, h2 {
            text-align: center;
            color: #333;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        </style>
        """
    
    def grid_to_html(self, grid: List[List[int]], size: int, is_solution: bool = False) -> str:
        """Convert a sudoku grid to HTML table."""
        grid_class = f"grid-{size}x{size}"
        if is_solution:
            grid_class += " solution-grid"
            
        html = f'<div class="sudoku-grid {grid_class}">\n'
        
        for row in grid:
            html += '  <div class="sudoku-row">\n'
            for cell in row:
                value = str(cell) if cell != 0 else ''
                html += f'    <div class="sudoku-cell">{value}</div>\n'
            html += '  </div>\n'
        
        html += '</div>\n'
        return html
    
    def calculate_puzzles_per_row(self, size: int, puzzles_per_page: int) -> Tuple[int, int]:
        """Calculate optimal layout for puzzles on page."""
        if puzzles_per_page == 1:
            return 1, 1
        elif puzzles_per_page <= 2:
            return 2, 1
        elif puzzles_per_page <= 4:
            return 2, 2
        elif puzzles_per_page <= 6:
            return 3, 2
        else:
            return 3, 3  # Max 9 puzzles per page
    
    def generate_puzzles_page(self, puzzles: List[Tuple[List[List[int]], List[List[int]], str, int]], 
                            puzzles_per_page: int) -> str:
        """Generate HTML for a page of puzzles."""
        html = '<div class="page">\n'
        html += '<div class="header">\n'
        html += '<h1>Sudoku Puzzles</h1>\n'
        html += '</div>\n'
        
        puzzle_num = 1
        for puzzle, solution, difficulty, size in puzzles:
            html += '<div class="puzzle-container">\n'
            html += f'  <div class="puzzle-title">Puzzle #{puzzle_num} - {size}×{size} ({difficulty.title()})</div>\n'
            html += self.grid_to_html(puzzle, size)
            html += '</div>\n'
            puzzle_num += 1
        
        html += '</div>\n'
        return html
    
    def generate_solutions_page(self, puzzles: List[Tuple[List[List[int]], List[List[int]], str, int]]) -> str:
        """Generate HTML for solutions page."""
        html = '<div class="solutions-page">\n'
        html += '<h2>Solutions</h2>\n'
        
        puzzle_num = 1
        for puzzle, solution, difficulty, size in puzzles:
            html += '<div class="solution-grid">\n'
            html += f'  <div class="solution-title">Solution #{puzzle_num} - {size}×{size}</div>\n'
            html += self.grid_to_html(solution, size, is_solution=True)
            html += '</div>\n'
            puzzle_num += 1
        
        html += '</div>\n'
        return html
    
    def generate_html_document(self, all_puzzles: List[Tuple[List[List[int]], List[List[int]], str, int]], 
                             puzzles_per_page: int, include_solutions: bool = True) -> str:
        """Generate complete HTML document with puzzles."""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sudoku Puzzles</title>
    {self.base_css}
</head>
<body>
"""
        
        # Split puzzles into pages
        for i in range(0, len(all_puzzles), puzzles_per_page):
            page_puzzles = all_puzzles[i:i + puzzles_per_page]
            html += self.generate_puzzles_page(page_puzzles, puzzles_per_page)
        
        # Add solutions if requested
        if include_solutions:
            html += self.generate_solutions_page(all_puzzles)
        
        html += """
</body>
</html>
"""
        return html
    
    def save_to_file(self, html_content: str, filename: str = "sudoku_puzzles.html"):
        """Save HTML content to file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Sudoku puzzles saved to {filename}")
        print(f"Open this file in your web browser and print to get physical copies.")