from __future__ import annotations

import os
import tempfile
from typing import List, Tuple, Optional, Dict

from flask import Flask, render_template, request, send_file, Response

from sudoku.generator import SudokuGenerator
from sudoku.printer import SudokuPrinter


def generate_puzzles(size: int, difficulty: str, count: int, seed: Optional[int] = None,
                     custom_difficulty: Optional[float] = None,
                     max_attempts_multiplier: Optional[int] = None,
                     allow_multiple_solutions: bool = False) -> List[Tuple[List[List[int]], List[List[int]], str, int]]:
    if seed is not None:
        import random
        random.seed(seed)

    generator = SudokuGenerator(size)

    if custom_difficulty is not None:
        generator.difficulty_settings[size][difficulty] = custom_difficulty

    if max_attempts_multiplier is not None:
        generator.max_attempts_multiplier = max_attempts_multiplier

    if allow_multiple_solutions:
        generator.require_unique_solution = False

    puzzles: List[Tuple[List[List[int]], List[List[int]], str, int]] = []
    for _ in range(count):
        puzzle, solution = generator.generate_puzzle(difficulty)
        puzzles.append((puzzle, solution, difficulty, size))
    return puzzles


def build_formatting_options(form: Dict[str, str]) -> Dict:
    def parse_int(name: str) -> Optional[int]:
        val = form.get(name)
        if val is None or val == "":
            return None
        try:
            return int(val)
        except ValueError:
            return None

    options = {
        'cell_size': parse_int('cell_size'),
        'font_size': parse_int('font_size'),
        'solution_cell_size': parse_int('solution_cell_size'),
        'solution_font_size': parse_int('solution_font_size'),
        'border_width': parse_int('border_width') or 3,
        'cell_border_width': parse_int('cell_border_width') or 1,
        'thick_border_width': parse_int('thick_border_width') or 3,
        'grid_color': form.get('grid_color') or '#000000',
        'cell_border_color': form.get('cell_border_color') or '#666666',
        'text_color': form.get('text_color') or '#000000',
        'background_color': form.get('background_color') or '#ffffff',
        'page_margin': form.get('page_margin') or '0.5in',
        'puzzle_margin': parse_int('puzzle_margin') or 20,
        'title_font_size': parse_int('title_font_size') or 14,
        'solution_title_font_size': parse_int('solution_title_font_size') or 12,
        'show_puzzle_info': (form.get('print_info') == 'on')
    }
    return options


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get('/')
    def index():
        return render_template('index.html')

    @app.post('/generate')
    def generate():
        # Required fields with defaults
        size = int(request.form.get('size', 9))
        difficulty = request.form.get('difficulty', 'normal')
        count = int(request.form.get('count', 4))
        per_page = int(request.form.get('per_page', 2))
        seed_val = request.form.get('seed')
        seed = int(seed_val) if seed_val else None
        custom_diff_val = request.form.get('custom_difficulty')
        custom_difficulty = float(custom_diff_val) if custom_diff_val else None
        allow_multiple_solutions = request.form.get('allow_multiple_solutions') == 'on'
        no_solutions = request.form.get('no_solutions') == 'on'
        output_format = request.form.get('output_format', 'pdf')  # 'pdf' or 'html'

        formatting_options = build_formatting_options(request.form)

        puzzles = generate_puzzles(
            size=size,
            difficulty=difficulty,
            count=count,
            seed=seed,
            custom_difficulty=custom_difficulty,
            allow_multiple_solutions=allow_multiple_solutions,
        )

        printer = SudokuPrinter()
        include_solutions = not no_solutions

        if output_format == 'html':
            html_content = printer.generate_html_document(
                puzzles,
                puzzles_per_page=per_page,
                include_solutions=include_solutions,
                formatting_options=formatting_options,
                from_files=False,
            )
            # Return inline for easy preview/print on mobile/desktop
            return Response(html_content, mimetype='text/html')
        else:
            # Generate PDF to temp file and send
            tmp_fd, tmp_path = tempfile.mkstemp(suffix='.pdf')
            os.close(tmp_fd)
            try:
                printer.generate_pdf_document(
                    puzzles,
                    puzzles_per_page=per_page,
                    include_solutions=include_solutions,
                    formatting_options=formatting_options,
                    filename=tmp_path,
                    from_files=False,
                )
                filename = f"sudoku_{size}x{size}_{difficulty}.pdf"
                return send_file(tmp_path, as_attachment=True, download_name=filename, mimetype='application/pdf')
            finally:
                # File will be removed after response is sent; safe to attempt cleanup
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

    return app


app = create_app()

if __name__ == '__main__':
    # Development server - enables reloader and debug
    app.run(host='0.0.0.0', port=5000, debug=True)
