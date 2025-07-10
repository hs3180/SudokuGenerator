# Printable Sudoku Generator

A Python-based sudoku generator that creates printable puzzles in multiple sizes and difficulty levels.

## Features

- **Multiple Grid Sizes**: Support for 4×4, 6×6, and 9×9 sudoku grids
- **Difficulty Levels**: Easy, Normal, and Hard difficulty settings
- **Flexible Layout**: Configurable number of puzzles per page (1-9)
- **Printable Output**: Generates clean HTML files optimized for printing
- **Solutions Included**: Optional solutions page for checking answers
- **Mixed Mode**: Generate puzzles with random sizes and difficulties

## Installation

No additional dependencies required! The generator uses only Python standard library.

```bash
# Clone or download the files
git clone <repository-url>
cd sudoku-generator

# Make the main script executable (optional)
chmod +x main.py
```

## Usage

### Basic Usage

Generate 4 normal 9×9 puzzles with 2 per page:
```bash
python main.py
```

### Common Examples

Generate 6 easy 4×4 puzzles, 4 per page:
```bash
python main.py --size 4 --difficulty easy --count 6 --per-page 4
```

Generate 2 hard 9×9 puzzles, 1 per page:
```bash
python main.py --size 9 --difficulty hard --count 2 --per-page 1
```

Generate mixed puzzles (random sizes and difficulties):
```bash
python main.py --mixed --count 9 --per-page 3
```

Generate puzzles without solutions:
```bash
python main.py --count 6 --no-solutions
```

Custom output filename:
```bash
python main.py --output my_puzzles.html
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--size` | Grid size (4, 6, or 9) | 9 |
| `--difficulty` | Difficulty level (easy, normal, hard) | normal |
| `--count` | Number of puzzles to generate | 4 |
| `--per-page` | Puzzles per page (1-9) | 2 |
| `--output` | Output HTML filename | sudoku_puzzles.html |
| `--no-solutions` | Don't include solutions page | False |
| `--mixed` | Generate mixed size/difficulty puzzles | False |

## Difficulty Levels

The difficulty is determined by how many numbers are removed from the complete grid:

### 4×4 Grids
- **Easy**: 30% of cells removed (~5 cells)
- **Normal**: 40% of cells removed (~6 cells)
- **Hard**: 50% of cells removed (~8 cells)

### 6×6 Grids
- **Easy**: 35% of cells removed (~13 cells)
- **Normal**: 45% of cells removed (~16 cells)
- **Hard**: 55% of cells removed (~20 cells)

### 9×9 Grids
- **Easy**: 40% of cells removed (~32 cells)
- **Normal**: 50% of cells removed (~40 cells)
- **Hard**: 60% of cells removed (~49 cells)

## Printing Instructions

1. Open the generated HTML file in your web browser
2. Press `Ctrl+P` (or `Cmd+P` on Mac) to open print dialog
3. **Important**: Enable "Background graphics" in print settings to see the grid borders
4. Choose your paper size (Letter or A4 work well)
5. Print!

## Grid Types

### 4×4 Sudoku
- Uses numbers 1-4
- 2×2 sub-grids
- Perfect for beginners or kids
- Quick to solve (5-15 minutes)

### 6×6 Sudoku
- Uses numbers 1-6
- 2×3 sub-grids
- Intermediate difficulty
- Moderate solving time (15-30 minutes)

### 9×9 Sudoku
- Uses numbers 1-9
- 3×3 sub-grids
- Traditional sudoku format
- Longer solving time (20-60+ minutes)

## File Structure

```
sudoku-generator/
├── main.py              # Main CLI script
├── sudoku_generator.py  # Core sudoku generation logic
├── sudoku_printer.py    # HTML formatting and printing
└── README.md           # This file
```

## How It Works

1. **Grid Generation**: Creates a complete, valid sudoku grid using backtracking algorithm
2. **Number Removal**: Strategically removes numbers while ensuring unique solution
3. **HTML Formatting**: Converts grids to styled HTML with CSS for clean printing
4. **Layout Management**: Arranges multiple puzzles per page with proper spacing

## Examples Output

The generator creates clean, professional-looking puzzles suitable for:
- Classroom activities
- Puzzle books
- Personal entertainment
- Gifts for puzzle enthusiasts

## Tips for Best Results

- For young children: Use 4×4 grids with easy difficulty
- For casual solvers: Use 6×6 or 9×9 grids with normal difficulty
- For puzzle enthusiasts: Use 9×9 grids with hard difficulty
- For printing: Use 1-2 puzzles per page for 9×9, up to 4 for 4×4
- For bulk generation: Use the mixed mode for variety

## Troubleshooting

**Puzzles taking too long to generate?**
- 9×9 hard puzzles can take 30-60 seconds each
- Try generating fewer puzzles or easier difficulties
- 4×4 and 6×6 puzzles generate much faster

**Print formatting issues?**
- Make sure "Background graphics" is enabled in print settings
- Try different browsers if formatting looks wrong
- Use "Print to PDF" to save a digital copy

**Grid borders not visible?**
- This usually means background graphics are disabled in print settings
- Enable "Print backgrounds" or "Background graphics" option
