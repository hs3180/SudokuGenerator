from typing import List, Tuple, Dict, Optional
from sudoku_generator import SudokuGenerator

class SudokuPrinter:
    def __init__(self):
        self.default_settings = {
            4: {'cell_size': 35, 'font_size': 18, 'solution_cell_size': 25, 'solution_font_size': 12},
            6: {'cell_size': 32, 'font_size': 14, 'solution_cell_size': 22, 'solution_font_size': 10},
            9: {'cell_size': 28, 'font_size': 14, 'solution_cell_size': 18, 'solution_font_size': 8}
        }

    def generate_css(self, formatting_options: Optional[Dict] = None) -> str:
        """Generate CSS with custom formatting options."""
        options = formatting_options or {}
        
        # Default values
        page_margin = options.get('page_margin', '0.5in')
        puzzle_margin = options.get('puzzle_margin', 20)
        title_font_size = options.get('title_font_size', 14)
        solution_title_font_size = options.get('solution_title_font_size', 12)
        border_width = options.get('border_width', 3)
        cell_border_width = options.get('cell_border_width', 1)
        thick_border_width = options.get('thick_border_width', 3)
        grid_color = options.get('grid_color', '#000000')
        cell_border_color = options.get('cell_border_color', '#666666')
        text_color = options.get('text_color', '#000000')
        background_color = options.get('background_color', '#ffffff')
        
        css = f"""
        <style>
        @media print {{
            @page {{ margin: {page_margin}; }}
            body {{ margin: 0; }}
        }}
        
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: white;
        }}
        
        .page {{
            page-break-after: always;
            width: 100%;
        }}
        
        .page:last-child {{
            page-break-after: avoid;
        }}
        
        .puzzle-container {{
            display: inline-block;
            margin: {puzzle_margin}px;
            text-align: center;
            vertical-align: top;
        }}
        
        .puzzle-title {{
            font-size: {title_font_size}px;
            font-weight: bold;
            margin-bottom: 10px;
            color: {text_color};
        }}
        
        .puzzle-info {{
            font-size: {max(title_font_size - 2, 10)}px;
            color: #666;
            margin-top: 10px;
        }}
        
        .sudoku-grid {{
            border: {border_width}px solid {grid_color};
            display: inline-block;
            background-color: {background_color};
        }}
        
        .sudoku-row {{
            display: flex;
            margin: 0;
            padding: 0;
        }}
        
        .sudoku-cell {{
            border: {cell_border_width}px solid {cell_border_color};
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            background-color: {background_color};
            color: {text_color};
        }}
        """
        
        # Generate size-specific CSS
        for size in [4, 6, 9]:
            defaults = self.default_settings[size]
            cell_size = options.get('cell_size', defaults['cell_size'])
            font_size = options.get('font_size', defaults['font_size'])
            solution_cell_size = options.get('solution_cell_size', defaults['solution_cell_size'])
            solution_font_size = options.get('solution_font_size', defaults['solution_font_size'])
            
            # Determine box separator positions
            if size == 4:
                nth_child_col = "2n"
                nth_child_row = "2n"
            elif size == 6:
                nth_child_col = "3n"
                nth_child_row = "2n"
            else:  # size == 9
                nth_child_col = "3n"
                nth_child_row = "3n"
            
            css += f"""
        /* {size}x{size} grid styling */
        .grid-{size}x{size} .sudoku-cell {{
            width: {cell_size}px;
            height: {cell_size}px;
            font-size: {font_size}px;
        }}
        
        .grid-{size}x{size} .sudoku-cell:nth-child({nth_child_col}) {{
            border-right: {thick_border_width}px solid {grid_color};
        }}
        
        .grid-{size}x{size} .sudoku-row:nth-child({nth_child_row}) .sudoku-cell {{
            border-bottom: {thick_border_width}px solid {grid_color};
        }}
        
        /* Solution grid specific styling */
        .solution-grid.grid-{size}x{size} .sudoku-cell {{
            width: {solution_cell_size}px;
            height: {solution_cell_size}px;
            font-size: {solution_font_size}px;
        }}
        """
        
        css += f"""
        .solutions-page {{
            page-break-before: always;
        }}
        
        .solution-grid {{
            margin: 10px;
            display: inline-block;
        }}
        
        .solution-title {{
            font-size: {solution_title_font_size}px;
            margin-bottom: 5px;
            color: {text_color};
        }}
        
        .solution-grid .sudoku-grid {{
            border: 2px solid {cell_border_color};
        }}
        
        .solution-grid .sudoku-cell {{
            border: 1px solid #ccc;
        }}
        
        h1, h2 {{
            text-align: center;
            color: {text_color};
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        </style>
        """
        
        return css
    
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
                            puzzles_per_page: int, show_puzzle_info: bool = False) -> str:
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
            if show_puzzle_info:
                html += f'  <div class="puzzle-info">Size: {size}×{size} | Difficulty: {difficulty.title()}</div>\n'
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
                             puzzles_per_page: int, include_solutions: bool = True, 
                             formatting_options: Optional[Dict] = None) -> str:
        """Generate complete HTML document with puzzles."""
        options = formatting_options or {}
        show_puzzle_info = options.get('show_puzzle_info', False)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sudoku Puzzles</title>
    {self.generate_css(formatting_options)}
</head>
<body>
"""
        
        # Split puzzles into pages
        for i in range(0, len(all_puzzles), puzzles_per_page):
            page_puzzles = all_puzzles[i:i + puzzles_per_page]
            html += self.generate_puzzles_page(page_puzzles, puzzles_per_page, show_puzzle_info)
        
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