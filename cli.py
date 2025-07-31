#!/usr/bin/env python3
"""
Sudoku Generator - Generate printable sudoku puzzles

Usage:
    python main.py --size 9 --difficulty normal --count 4 --per-page 2
"""

import argparse
import sys
import random
import glob
from typing import List, Tuple, Optional
from sudoku.generator import SudokuGenerator
from sudoku.parser import SudokuParser

def generate_multiple_puzzles(size: int, difficulty: str, count: int, seed: Optional[int] = None, 
                            custom_difficulty: Optional[float] = None, max_attempts_multiplier: Optional[int] = None) -> List[Tuple[List[List[int]], List[List[int]], str, int]]:
    """Generate multiple sudoku puzzles."""
    if seed is not None:
        random.seed(seed)
        
    generator = SudokuGenerator(size)
    
    # Override difficulty if custom percentage provided
    if custom_difficulty is not None:
        generator.difficulty_settings[size][difficulty] = custom_difficulty
    
    # Override max attempts multiplier if provided
    if max_attempts_multiplier is not None:
        generator.max_attempts_multiplier = max_attempts_multiplier
    
    puzzles = []
    
    print(f"Generating {count} {size}×{size} sudoku puzzles ({difficulty} difficulty)...")
    
    for i in range(count):
        print(f"  Generating puzzle {i+1}/{count}...", end=" ", flush=True)
        puzzle, solution = generator.generate_puzzle(difficulty)
        puzzles.append((puzzle, solution, difficulty, size))
        print("✓")
    
    return puzzles

def main():
    parser = argparse.ArgumentParser(
        description="Generate printable sudoku puzzles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    Generate 4 normal 9×9 puzzles, 2 per page:
        python cli.py --size 9 --difficulty normal --count 4 --per-page 2
    
    Generate 6 easy 4×4 puzzles, 4 per page:
        python cli.py --size 4 --difficulty easy --count 6 --per-page 4
    
    Generate mixed difficulty puzzles:
        python cli.py --mixed --count 9 --per-page 3
    
    Read puzzles from specific files:
        python cli.py --files Easy1.txt Easy2.txt Easy3.txt --per-page 2
    
    Read puzzles using file pattern:
        python cli.py --file-pattern "Easy*.txt" --per-page 2
    
    Custom difficulty and formatting:
        python cli.py --size 9 --difficulty normal --custom-difficulty 0.7 --cell-size 35 --font-size 18
        """
    )
    
    # Basic puzzle settings
    parser.add_argument(
        "--size", 
        type=int, 
        choices=[4, 6, 9], 
        default=9,
        help="Sudoku grid size (4, 6, or 9). Default: 9"
    )
    
    parser.add_argument(
        "--difficulty", 
        choices=["very_easy", "easy", "normal", "hard", "very_hard"], 
        default="normal",
        help="Puzzle difficulty level. Default: normal"
    )
    
    parser.add_argument(
        "--count", 
        type=int, 
        default=4,
        help="Number of puzzles to generate. Default: 4"
    )
    
    parser.add_argument(
        "--per-page", 
        type=int, 
        default=2,
        help="Number of puzzles per page (1-9). Default: 2"
    )
    
    # Generation settings
    parser.add_argument(
        "--seed",
        type=int,
        help="Random seed for reproducible puzzle generation"
    )
    
    parser.add_argument(
        "--custom-difficulty",
        type=float,
        metavar="PERCENT",
        help="Custom difficulty as percentage of cells to remove (0.1-0.9). Overrides --difficulty setting"
    )
    
    parser.add_argument(
        "--max-attempts-multiplier",
        type=int,
        default=10,
        metavar="N",
        help="Multiplier for maximum generation attempts (higher = more thorough but slower). Default: 10"
    )
    
    parser.add_argument(
        "--allow-multiple-solutions",
        action="store_true",
        help="Allow puzzles with multiple solutions (faster generation)"
    )
    
    # Formatting settings
    parser.add_argument(
        "--cell-size",
        type=int,
        metavar="PIXELS",
        help="Cell size in pixels. If not specified, uses size-appropriate defaults"
    )
    
    parser.add_argument(
        "--font-size",
        type=int,
        metavar="PIXELS", 
        help="Font size in pixels. If not specified, uses size-appropriate defaults"
    )
    
    parser.add_argument(
        "--solution-cell-size",
        type=int,
        metavar="PIXELS",
        help="Solution cell size in pixels. If not specified, uses size-appropriate defaults"
    )
    
    parser.add_argument(
        "--solution-font-size",
        type=int,
        metavar="PIXELS",
        help="Solution font size in pixels. If not specified, uses size-appropriate defaults"
    )
    
    parser.add_argument(
        "--border-width",
        type=int,
        default=3,
        metavar="PIXELS",
        help="Grid border width in pixels. Default: 3"
    )
    
    parser.add_argument(
        "--cell-border-width",
        type=int,
        default=1,
        metavar="PIXELS", 
        help="Cell border width in pixels. Default: 1"
    )
    
    parser.add_argument(
        "--thick-border-width",
        type=int,
        default=3,
        metavar="PIXELS",
        help="Thick border width for box separators in pixels. Default: 3"
    )
    
    # Color settings
    parser.add_argument(
        "--grid-color",
        default="#000000",
        metavar="COLOR",
        help="Grid border color (hex code). Default: #000000 (black)"
    )
    
    parser.add_argument(
        "--cell-border-color",
        default="#666666", 
        metavar="COLOR",
        help="Cell border color (hex code). Default: #666666 (gray)"
    )
    
    parser.add_argument(
        "--text-color",
        default="#000000",
        metavar="COLOR",
        help="Text color (hex code). Default: #000000 (black)"
    )
    
    parser.add_argument(
        "--background-color",
        default="#ffffff",
        metavar="COLOR",
        help="Cell background color (hex code). Default: #ffffff (white)"
    )
    
    # Page layout settings
    parser.add_argument(
        "--page-margin",
        default="0.5in",
        metavar="SIZE",
        help="Page margin size (CSS format, e.g., '0.5in', '20px'). Default: 0.5in"
    )
    
    parser.add_argument(
        "--puzzle-margin",
        type=int,
        default=20,
        metavar="PIXELS",
        help="Margin around each puzzle in pixels. Default: 20"
    )
    
    parser.add_argument(
        "--title-font-size",
        type=int,
        default=14,
        metavar="PIXELS",
        help="Puzzle title font size in pixels. Default: 14"
    )
    
    parser.add_argument(
        "--solution-title-font-size",
        type=int,
        default=12,
        metavar="PIXELS",
        help="Solution title font size in pixels. Default: 12"
    )
    
    # Output settings
    parser.add_argument(
        "--no-solutions", 
        action="store_true",
        help="Don't include solutions page"
    )
    
    parser.add_argument(
        "--output", 
        type=str, 
        default="sudoku_puzzles.pdf",
        help="Output filename. Default: sudoku_puzzles.pdf"
    )
    
    parser.add_argument(
        "--mixed", 
        action="store_true",
        help="Generate mixed size and difficulty puzzles"
    )
    
    parser.add_argument(
        "--files",
        nargs='+',
        metavar="FILE",
        help="Read sudoku puzzles from text files instead of generating new ones"
    )
    
    parser.add_argument(
        "--file-pattern",
        metavar="PATTERN",
        help="Read sudoku puzzles from files matching pattern (e.g., 'Easy*.txt')"
    )
    
    parser.add_argument(
        "--print-info",
        action="store_true",
        help="Include puzzle information (difficulty, size) below each puzzle"
    )
    
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Output as PDF instead of HTML (or use .pdf extension in --output)"
    )
    
    parser.add_argument(
        "--console",
        action="store_true",
        help="Output to console instead of file (no PDF/HTML generation)"
    )
    
    args = parser.parse_args()
    
    # Validation
    if args.per_page < 1 or args.per_page > 9:
        print("Error: Puzzles per page must be between 1 and 9")
        sys.exit(1)
    
    # Check if reading from files
    reading_from_files = args.files is not None or args.file_pattern is not None
    
    if not reading_from_files:
        if args.count < 1:
            print("Error: Count must be at least 1")
            sys.exit(1)
    else:
        # Validate file arguments
        if args.files is not None and args.file_pattern is not None:
            print("Error: Cannot use both --files and --file-pattern")
            sys.exit(1)
        
        if args.files is not None and len(args.files) == 0:
            print("Error: No files specified")
            sys.exit(1)
        
        if args.file_pattern is not None and not args.file_pattern.strip():
            print("Error: File pattern cannot be empty")
            sys.exit(1)
        
    if args.custom_difficulty is not None and not (0.1 <= args.custom_difficulty <= 0.9):
        print("Error: Custom difficulty must be between 0.1 and 0.9")
        sys.exit(1)
        
    if args.max_attempts_multiplier < 1:
        print("Error: Max attempts multiplier must be at least 1")
        sys.exit(1)

    try:
        if reading_from_files:
            # Read puzzles from files
            parser = SudokuParser()
            
            if args.files is not None:
                filepaths = args.files
            else:  # args.file_pattern is not None
                filepaths = glob.glob(args.file_pattern)
                if not filepaths:
                    print(f"Error: No files found matching pattern '{args.file_pattern}'")
                    sys.exit(1)
            
            print(f"Reading {len(filepaths)} sudoku puzzle files...")
            puzzles = parser.parse_multiple_files(filepaths)
            
            if not puzzles:
                print("Error: No valid puzzles found in the specified files")
                sys.exit(1)
            
            print(f"Successfully parsed {len(puzzles)} puzzles")
            
        elif args.mixed:
            # Generate mixed puzzles
            puzzles = []
            sizes = [4, 6, 9]
            difficulties = ["easy", "normal", "hard"]
            
            if args.seed is not None:
                random.seed(args.seed)
            
            print(f"Generating {args.count} mixed sudoku puzzles...")
            
            for i in range(args.count):
                size = random.choice(sizes)
                difficulty = random.choice(difficulties)
                print(f"  Generating puzzle {i+1}/{args.count} ({size}×{size}, {difficulty})...", end=" ", flush=True)
                
                generator = SudokuGenerator(size)
                
                # Apply custom settings
                if args.custom_difficulty is not None:
                    generator.difficulty_settings[size][difficulty] = args.custom_difficulty
                if args.max_attempts_multiplier is not None:
                    generator.max_attempts_multiplier = args.max_attempts_multiplier
                if args.allow_multiple_solutions:
                    generator.require_unique_solution = False
                
                puzzle, solution = generator.generate_puzzle(difficulty)
                puzzles.append((puzzle, solution, difficulty, size))
                print("✓")
        else:
            # Generate uniform puzzles
            puzzles = generate_multiple_puzzles(
                args.size, 
                args.difficulty, 
                args.count, 
                args.seed,
                args.custom_difficulty,
                args.max_attempts_multiplier
            )
        
        # Handle output
        if args.console:
            # Console output - no file generation
            print("\n生成的数独谜题:")
            for i, (puzzle, solution, difficulty, size) in enumerate(puzzles, 1):
                print(f"\n谜题 {i} ({size}×{size} {difficulty}):")
                print("谜题:")
                for row in puzzle:
                    print(' '.join(str(cell) if cell != 0 else '.' for cell in row))
                if not args.no_solutions:
                    print("解答:")
                    for row in solution:
                        print(' '.join(str(cell) for cell in row))
                print()
            
            if reading_from_files:
                print(f"成功解析了 {len(puzzles)} 个谜题")
            else:
                print(f"成功生成了 {len(puzzles)} 个谜题")
        else:
            # File output - import printer only when needed
            try:
                from sudoku.printer import SudokuPrinter
                printer = SudokuPrinter()
                formatting_options = {
                    'cell_size': args.cell_size,
                    'font_size': args.font_size,
                    'solution_cell_size': args.solution_cell_size,
                    'solution_font_size': args.solution_font_size,
                    'border_width': args.border_width,
                    'cell_border_width': args.cell_border_width,
                    'thick_border_width': args.thick_border_width,
                    'grid_color': args.grid_color,
                    'cell_border_color': args.cell_border_color,
                    'text_color': args.text_color,
                    'background_color': args.background_color,
                    'page_margin': args.page_margin,
                    'puzzle_margin': args.puzzle_margin,
                    'title_font_size': args.title_font_size,
                    'solution_title_font_size': args.solution_title_font_size,
                    'show_puzzle_info': args.print_info
                }
                # 默认输出PDF：只要--output未指定或为.pdf结尾，或未指定--pdf参数时，默认输出PDF
                output_is_pdf = True if (not args.output or args.output.lower().endswith('.pdf')) else False
                if args.pdf:
                    output_is_pdf = True
                if output_is_pdf:
                    print("\nGenerating PDF...")
                    printer.generate_pdf_document(
                        puzzles,
                        args.per_page,
                        formatting_options=formatting_options,
                        filename=args.output,
                        from_files=reading_from_files
                    )
                else:
                    print("\nGenerating HTML...")
                    html_content = printer.generate_html_document(
                        puzzles, 
                        args.per_page, 
                        formatting_options=formatting_options,
                        from_files=reading_from_files
                    )
                    printer.save_to_file(html_content, args.output)
                
                if reading_from_files:
                    print(f"\nSuccess! Parsed {len(puzzles)} puzzles from files.")
                else:
                    print(f"\nSuccess! Generated {len(puzzles)} puzzles.")
                print(f"Output saved to: {args.output}")
                print(f"Puzzles per page: {args.per_page}")
                if not reading_from_files and args.seed is not None:
                    print(f"Random seed used: {args.seed}")
                if not args.no_solutions:
                    print("Solutions included on separate page")
                if output_is_pdf:
                    print("\nTo print:")
                    print(f"1. Open {args.output} in your PDF viewer")
                    print("2. Use the print function to print the puzzles")
                else:
                    print("\nTo print:")
                    print(f"1. Open {args.output} in your web browser")
                    print("2. Use Ctrl+P (or Cmd+P on Mac) to print")
                    print("3. Make sure to enable 'Background graphics' in print settings")
            except ImportError as e:
                print(f"Error: {e}")
                print("Please install required dependencies for file output:")
                print("pip install fpdf")
                sys.exit(1)
        
    except KeyboardInterrupt:
        print("\nGeneration cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()