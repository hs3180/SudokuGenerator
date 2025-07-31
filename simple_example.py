#!/usr/bin/env python3
"""
数独生成器简单使用示例
快速生成和显示数独谜题
"""

from sudoku.generator import SudokuGenerator

def print_simple_grid(grid, title=""):
    """简单打印数独网格"""
    if title:
        print(f"\n{title}")
        print("-" * 30)
    
    size = len(grid)
    for i, row in enumerate(grid):
        if i % 3 == 0 and i != 0 and size == 9:
            print("-" * (size * 2 + 1))
        elif i % 2 == 0 and i != 0 and size == 6:
            print("-" * (size * 2 + 1))
        elif i % 2 == 0 and i != 0 and size == 4:
            print("-" * (size * 2 + 1))
        
        row_str = " ".join(str(x) if x != 0 else "." for x in row)
        print(row_str)

def main():
    """主函数 - 演示数独生成"""
    print("数独生成器简单示例")
    print("=" * 40)
    
    # 示例1: 生成9×9数独
    print("\n示例1: 生成9×9数独谜题")
    generator_9x9 = SudokuGenerator(9)
    
    # 生成easy难度的谜题
    puzzle, solution = generator_9x9.generate_puzzle('easy')
    
    print_simple_grid(puzzle, "Easy难度数独谜题")
    print_simple_grid(solution, "完整解答")
    
    # 验证解的唯一性
    solution_count = generator_9x9.count_solutions(puzzle, 3)
    print(f"\n解的数量: {solution_count}")
    print(f"是否唯一解: {'是' if solution_count == 1 else '否'}")
    
    # 示例2: 生成4×4数独
    print("\n\n示例2: 生成4×4数独谜题")
    generator_4x4 = SudokuGenerator(4)
    
    puzzle_4x4, solution_4x4 = generator_4x4.generate_puzzle('normal')
    
    print_simple_grid(puzzle_4x4, "4×4数独谜题")
    print_simple_grid(solution_4x4, "完整解答")
    
    # 示例3: 生成6×6数独
    print("\n\n示例3: 生成6×6数独谜题")
    generator_6x6 = SudokuGenerator(6)
    
    puzzle_6x6, solution_6x6 = generator_6x6.generate_puzzle('hard')
    
    print_simple_grid(puzzle_6x6, "6×6数独谜题 (Hard难度)")
    print_simple_grid(solution_6x6, "完整解答")
    
    # 示例4: 批量生成
    print("\n\n示例4: 批量生成数独谜题")
    print("生成5个不同难度的9×9数独:")
    
    difficulties = ['easy', 'normal', 'hard']
    for i, difficulty in enumerate(difficulties, 1):
        puzzle, solution = generator_9x9.generate_puzzle(difficulty)
        empty_cells = sum(1 for row in puzzle for cell in row if cell == 0)
        print(f"\n{i}. {difficulty}难度 (挖空{empty_cells}个):")
        print_simple_grid(puzzle)
    
    print("\n\n使用说明:")
    print("1. 创建生成器: generator = SudokuGenerator(size)")
    print("2. 生成谜题: puzzle, solution = generator.generate_puzzle(difficulty)")
    print("3. 验证唯一性: count = generator.count_solutions(puzzle, limit)")
    print("4. 支持的size: 4, 6, 9")
    print("5. 支持的difficulty: 'easy', 'normal', 'hard'")

if __name__ == "__main__":
    main()