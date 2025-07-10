#!/usr/bin/env python3
"""
Sudoku Generator - Generate printable sudoku puzzles

Usage:
    python main.py --size 9 --difficulty normal --count 4 --per-page 2
"""

import argparse
import sys
from typing import List, Tuple
from sudoku_generator import SudokuGenerator
from sudoku_printer import SudokuPrinter

def generate_multiple_puzzles(size: int, difficulty: str, count: int) -> List[Tuple[List[List[int]], List[List[int]], str, int]]:
    """Generate multiple sudoku puzzles."""
    generator = SudokuGenerator(size)
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
        python main.py --size 9 --difficulty normal --count 4 --per-page 2
    
    Generate 6 easy 4×4 puzzles, 4 per page:
        python main.py --size 4 --difficulty easy --count 6 --per-page 4
    
    Generate mixed difficulty puzzles:
        python main.py --mixed --count 9 --per-page 3
        """
    )
    
    parser.add_argument(
        "--size", 
        type=int, 
        choices=[4, 6, 9], 
        default=9,
        help="Sudoku grid size (4, 6, or 9). Default: 9"
    )
    
    parser.add_argument(
        "--difficulty", 
        choices=["easy", "normal", "hard"], 
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
    
    parser.add_argument(
        "--no-solutions", 
        action="store_true",
        help="Don't include solutions page"
    )
    
    parser.add_argument(
        "--output", 
        type=str, 
        default="sudoku_puzzles.html",
        help="Output filename. Default: sudoku_puzzles.html"
    )
    
    parser.add_argument(
        "--mixed", 
        action="store_true",
        help="Generate mixed size and difficulty puzzles"
    )
    
    args = parser.parse_args()
    
    # Validate puzzles per page
    if args.per_page < 1 or args.per_page > 9:
        print("Error: Puzzles per page must be between 1 and 9")
        sys.exit(1)
    
    # Validate count
    if args.count < 1:
        print("Error: Count must be at least 1")
        sys.exit(1)
    
    try:
        if args.mixed:
            # Generate mixed puzzles
            puzzles = []
            sizes = [4, 6, 9]
            difficulties = ["easy", "normal", "hard"]
            
            print(f"Generating {args.count} mixed sudoku puzzles...")
            
            import random
            for i in range(args.count):
                size = random.choice(sizes)
                difficulty = random.choice(difficulties)
                print(f"  Generating puzzle {i+1}/{args.count} ({size}×{size}, {difficulty})...", end=" ", flush=True)
                
                generator = SudokuGenerator(size)
                puzzle, solution = generator.generate_puzzle(difficulty)
                puzzles.append((puzzle, solution, difficulty, size))
                print("✓")
        else:
            # Generate uniform puzzles
            puzzles = generate_multiple_puzzles(args.size, args.difficulty, args.count)
        
        # Generate HTML
        print("\nGenerating HTML...")
        printer = SudokuPrinter()
        html_content = printer.generate_html_document(
            puzzles, 
            args.per_page, 
            include_solutions=not args.no_solutions
        )
        
        # Save to file
        printer.save_to_file(html_content, args.output)
        
        print(f"\nSuccess! Generated {len(puzzles)} puzzles.")
        print(f"Output saved to: {args.output}")
        print(f"Puzzles per page: {args.per_page}")
        if not args.no_solutions:
            print("Solutions included on separate page")
        
        print("\nTo print:")
        print(f"1. Open {args.output} in your web browser")
        print("2. Use Ctrl+P (or Cmd+P on Mac) to print")
        print("3. Make sure to enable 'Background graphics' in print settings")
        
    except KeyboardInterrupt:
        print("\nGeneration cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()