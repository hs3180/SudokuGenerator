# Sudoku Generator CLI Arguments Guide

This document outlines all the CLI arguments available for customizing puzzle generation and formatting.

## Basic Puzzle Settings

- `--size {4,6,9}` - Sudoku grid size (default: 9)
- `--difficulty {easy,normal,hard}` - Puzzle difficulty level (default: normal)
- `--count COUNT` - Number of puzzles to generate (default: 4)
- `--per-page PER_PAGE` - Number of puzzles per page, 1-9 (default: 2)

## Generation Settings

- `--seed SEED` - Random seed for reproducible puzzle generation
- `--custom-difficulty PERCENT` - Custom difficulty as percentage of cells to remove (0.1-0.9). Overrides --difficulty setting
- `--max-attempts-multiplier N` - Multiplier for maximum generation attempts (default: 10). Higher values = more thorough but slower generation
- `--allow-multiple-solutions` - Allow puzzles with multiple solutions (faster generation)

## Cell and Font Formatting

- `--cell-size PIXELS` - Cell size in pixels. Uses size-appropriate defaults if not specified:
  - 4×4: 35px
  - 6×6: 32px  
  - 9×9: 28px
- `--font-size PIXELS` - Font size in pixels. Uses size-appropriate defaults if not specified:
  - 4×4: 18px
  - 6×6: 14px
  - 9×9: 14px
- `--solution-cell-size PIXELS` - Solution cell size in pixels (smaller than main puzzles)
- `--solution-font-size PIXELS` - Solution font size in pixels (smaller than main puzzles)

## Border and Grid Styling

- `--border-width PIXELS` - Grid border width (default: 3)
- `--cell-border-width PIXELS` - Individual cell border width (default: 1)
- `--thick-border-width PIXELS` - Thick border width for box separators (default: 3)

## Color Customization

- `--grid-color COLOR` - Grid border color as hex code (default: #000000)
- `--cell-border-color COLOR` - Cell border color as hex code (default: #666666)
- `--text-color COLOR` - Text color as hex code (default: #000000)
- `--background-color COLOR` - Cell background color as hex code (default: #ffffff)

## Page Layout

- `--page-margin SIZE` - Page margin size in CSS format, e.g., '0.5in', '20px' (default: 0.5in)
- `--puzzle-margin PIXELS` - Margin around each puzzle (default: 20)
- `--title-font-size PIXELS` - Puzzle title font size (default: 14)
- `--solution-title-font-size PIXELS` - Solution title font size (default: 12)

## Output Options

- `--no-solutions` - Don't include solutions page
- `--output OUTPUT` - Output filename (default: sudoku_puzzles.html)
- `--mixed` - Generate mixed size and difficulty puzzles
- `--print-info` - Include puzzle information (difficulty, size) below each puzzle

## Examples

### Basic Usage
```bash
python3 main.py --size 9 --difficulty normal --count 4 --per-page 2
```

### Custom Difficulty
```bash
python3 main.py --size 9 --custom-difficulty 0.7 --count 2
```

### Reproducible Generation
```bash
python3 main.py --seed 12345 --count 4
```

### Custom Formatting
```bash
python3 main.py --cell-size 35 --font-size 18 --grid-color "#ff0000" --background-color "#f0f0f0"
```

### Large Format Puzzles
```bash
python3 main.py --size 9 --cell-size 40 --font-size 20 --per-page 1 --page-margin "1in"
```

### Colorful Puzzles with Info
```bash
python3 main.py --grid-color "#0066cc" --text-color "#003366" --print-info --count 6 --per-page 3
```

### Mixed Difficulty Set
```bash
python3 main.py --mixed --count 9 --per-page 3 --seed 54321
```

### Fast Generation (Multiple Solutions Allowed)
```bash
python3 main.py --allow-multiple-solutions --max-attempts-multiplier 5 --count 10
```

## Tips

1. **Custom Difficulty**: Use values between 0.1 (very easy) and 0.9 (extremely hard). Standard difficulties are approximately:
   - Easy: 0.3-0.4
   - Normal: 0.4-0.5  
   - Hard: 0.5-0.6

2. **Performance**: Higher `--max-attempts-multiplier` values create higher quality puzzles but take longer. Use `--allow-multiple-solutions` for faster generation.

3. **Colors**: Use hex color codes like #ff0000 (red), #0066cc (blue), etc. Make sure text and background colors have enough contrast.

4. **Printing**: Generated HTML files are optimized for printing. Enable "Background graphics" in your browser's print settings to see colors and borders.

5. **Reproducibility**: Use `--seed` with the same value to generate identical puzzles across runs.