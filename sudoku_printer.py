from typing import List, Tuple, Dict, Optional
from sudoku_generator import SudokuGenerator
from fpdf import FPDF

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
            solution_cell_size = options.get('solution_cell_size') or defaults['solution_cell_size']
            solution_font_size = options.get('solution_font_size') or defaults['solution_font_size']
            
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

    def grid_to_pdf(self, pdf: FPDF, grid: List[List[int]], size: int, x: float, y: float, cell_size: float, font_size: int, is_solution: bool = False):
        """Draw a sudoku grid on the PDF at position (x, y)."""
        n = size
        
        # Draw all cell borders first
        for row_idx, row in enumerate(grid):
            for col_idx, cell in enumerate(row):
                xpos = x + col_idx * cell_size
                ypos = y + row_idx * cell_size
                pdf.set_draw_color(0, 0, 0)
                pdf.set_line_width(0.5)
                pdf.rect(xpos, ypos, cell_size, cell_size)
        
        # Fill in the numbers
        for row_idx, row in enumerate(grid):
            for col_idx, cell in enumerate(row):
                if cell != 0:
                    xpos = x + col_idx * cell_size
                    ypos = y + row_idx * cell_size
                    pdf.set_font("Arial", style="B" if not is_solution else "", size=font_size)
                    pdf.set_text_color(0, 0, 0)
                    # Center the text in the cell
                    text_width = pdf.get_string_width(str(cell))
                    text_x = xpos + (cell_size - text_width) / 2
                    text_y = ypos + (cell_size - font_size) / 2
                    pdf.set_xy(text_x, text_y)
                    pdf.cell(text_width, font_size, str(cell), align="L")
        
        # Draw thick borders for boxes
        thick = 1.5
        if n == 4:
            box = 2
        elif n == 6:
            box = 3  # 6x6 should have 3x2 boxes
        else:
            box = 3
        
        for i in range(n + 1):
            lw = thick if i % box == 0 else 0.5
            # Horizontal lines
            pdf.set_line_width(lw)
            pdf.line(x, y + i * cell_size, x + n * cell_size, y + i * cell_size)
            # Vertical lines
            pdf.line(x + i * cell_size, y, x + i * cell_size, y + n * cell_size)

    def generate_pdf_document(self, all_puzzles: List[Tuple[List[List[int]], List[List[int]], str, int]],
                             puzzles_per_page: int, include_solutions: bool = True,
                             formatting_options: Optional[Dict] = None, filename: str = "sudoku_puzzles.pdf"):
        """Generate a PDF document with puzzles only (no solutions)."""
        options = formatting_options or {}
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.set_auto_page_break(auto=True, margin=15)
        show_puzzle_info = options.get('show_puzzle_info', False)
        
        # Get size-appropriate defaults for the first puzzle
        first_size = all_puzzles[0][3] if all_puzzles else 9
        default_cell_size = self.default_settings[first_size]['cell_size']
        default_font_size = self.default_settings[first_size]['font_size']
        
        cell_size = options.get('cell_size') or default_cell_size
        font_size = options.get('font_size') or default_font_size
        title_font_size = options.get('title_font_size', 14)
        puzzle_margin = options.get('puzzle_margin', 20)
        
        # Get page dimensions
        page_width = pdf.w
        page_height = pdf.h
        
        # Puzzles per page layout
        for i in range(0, len(all_puzzles), puzzles_per_page):
            page_puzzles = all_puzzles[i:i + puzzles_per_page]
            pdf.add_page()
            
            # Add page title
            pdf.set_font("Arial", "B", title_font_size)
            pdf.cell(0, 15, "Sudoku Puzzles", ln=True, align="C")
            
            # Calculate starting position
            x0, y0 = 20, 35
            x, y = x0, y0
            
            # Calculate layout for this page
            max_row, max_col = self.calculate_puzzles_per_row(first_size, puzzles_per_page)
            
            for idx, (puzzle, solution, difficulty, size) in enumerate(page_puzzles):
                # Check if we need to move to next row
                if idx > 0 and idx % max_col == 0:
                    x = x0
                    y += (cell_size * size) + puzzle_margin + 15
                
                # Check if we need a new page
                puzzle_height = (cell_size * size) + 20  # Include title space
                if y + puzzle_height > page_height - 20:  # Leave margin at bottom
                    pdf.add_page()
                    pdf.set_font("Arial", "B", title_font_size)
                    pdf.cell(0, 15, "Sudoku Puzzles", ln=True, align="C")
                    x, y = x0, 35
                
                # Add puzzle title
                pdf.set_xy(x, y)
                pdf.set_font("Arial", "B", title_font_size)
                title_text = f"Puzzle #{i+idx+1} - {size}×{size} ({difficulty.title()})"
                pdf.cell(cell_size * size, 8, title_text, ln=2, align="C")
                
                # Draw the grid
                self.grid_to_pdf(pdf, puzzle, size, x, y + 10, cell_size, font_size)
                
                # Add puzzle info if requested
                if show_puzzle_info:
                    pdf.set_xy(x, y + 10 + cell_size * size + 5)
                    pdf.set_font("Arial", size=10)
                    info_text = f"Size: {size}×{size} | Difficulty: {difficulty.title()}"
                    pdf.cell(cell_size * size, 6, info_text, ln=2, align="C")
                
                # Move to next column
                x += (cell_size * size) + puzzle_margin
                
                # Check if next puzzle would exceed page width
                if x + (cell_size * size) > page_width - 20:
                    x = x0
                    y += (cell_size * size) + puzzle_margin + 15
        
        pdf.output(filename)
        print(f"Sudoku puzzles saved to {filename}")
        print(f"Open this file to print or share the puzzles as a PDF.")