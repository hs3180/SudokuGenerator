import time
from typing import List, Dict, Any
from sudoku.generator import SudokuGenerator


def run_backtest(runs_per_setting: int = 3) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    sizes = [4, 6, 9]
    difficulties = ['very_easy', 'easy', 'normal', 'hard', 'very_hard']

    for size in sizes:
        generator = SudokuGenerator(size)
        for difficulty in difficulties:
            timings: List[float] = []
            for _ in range(runs_per_setting):
                start = time.perf_counter()
                puzzle, solution = generator.generate_puzzle(difficulty)
                elapsed = time.perf_counter() - start
                stats = generator.get_puzzle_statistics(puzzle)
                timings.append(elapsed)
            results.append({
                'size': size,
                'difficulty': difficulty,
                'runs': runs_per_setting,
                'avg_seconds': sum(timings) / len(timings),
                'min_seconds': min(timings),
                'max_seconds': max(timings),
                'last_stats': stats,
            })
    return results


def format_results_table(results: List[Dict[str, Any]]) -> str:
    # Simple text table
    headers = [
        'Size', 'Difficulty', 'Runs', 'Avg(s)', 'Min(s)', 'Max(s)', 'Fill%'
    ]
    lines = [' | '.join(headers)]
    for r in results:
        fill_percent = f"{r['last_stats']['fill_percentage']:.1f}%"
        lines.append(
            f"{r['size']} | {r['difficulty']} | {r['runs']} | "
            f"{r['avg_seconds']:.2f} | {r['min_seconds']:.2f} | {r['max_seconds']:.2f} | {fill_percent}"
        )
    return '\n'.join(lines)


def main():
    results = run_backtest(runs_per_setting=2)
    print(format_results_table(results))


if __name__ == '__main__':
    main()