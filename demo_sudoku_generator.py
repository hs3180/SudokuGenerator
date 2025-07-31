#!/usr/bin/env python3
"""
数独生成器演示脚本
展示先生成完整解，再挖空，并确保解唯一性的完整流程
"""

import random
from sudoku.generator import SudokuGenerator

def print_grid(grid, title=""):
    """打印数独网格"""
    if title:
        print(f"\n{title}")
        print("=" * 50)
    
    size = len(grid)
    for i, row in enumerate(grid):
        if i % 3 == 0 and i != 0:
            print("-" * (size * 3 + 2))
        print(" ".join(str(x) if x != 0 else "." for x in row))

def demo_sudoku_generation():
    """演示数独生成过程"""
    print("数独生成器演示")
    print("=" * 60)
    
    # 设置随机种子以确保可重现的结果
    random.seed(42)
    
    # 创建9x9数独生成器
    generator = SudokuGenerator(9)
    
    print(f"生成器配置:")
    print(f"- 网格大小: {generator.size}x{generator.size}")
    print(f"- 难度设置: {generator.difficulty_settings[9]}")
    print(f"- 要求唯一解: {generator.require_unique_solution}")
    
    # 步骤1: 生成完整解
    print("\n步骤1: 生成完整的数独解")
    print("-" * 40)
    
    complete_solution = generator.generate_complete_grid()
    print_grid(complete_solution, "完整的数独解")
    
    # 验证完整解的有效性
    print(f"\n验证完整解:")
    print(f"- 行数: {len(complete_solution)}")
    print(f"- 列数: {len(complete_solution[0])}")
    print(f"- 所有数字都在1-9范围内: {all(1 <= x <= 9 for row in complete_solution for x in row)}")
    
    # 步骤2: 不同难度的挖空演示
    difficulties = ['easy', 'normal', 'hard']
    
    for difficulty in difficulties:
        print(f"\n步骤2: 生成{difficulty}难度的数独谜题")
        print("-" * 50)
        
        # 生成谜题
        puzzle, solution = generator.generate_puzzle(difficulty)
        
        # 计算挖空数量
        empty_cells = sum(1 for row in puzzle for cell in row if cell == 0)
        total_cells = generator.size * generator.size
        empty_percentage = empty_cells / total_cells * 100
        
        print(f"难度: {difficulty}")
        print(f"挖空比例: {empty_percentage:.1f}% ({empty_cells}/{total_cells} 个空位)")
        print(f"目标挖空比例: {generator.difficulty_settings[9][difficulty] * 100:.1f}%")
        
        # 显示谜题
        print_grid(puzzle, f"{difficulty}难度的数独谜题")
        
        # 验证解的唯一性
        print(f"\n验证解的唯一性:")
        solution_count = generator.count_solutions(puzzle, 3)
        print(f"- 解的数量: {solution_count}")
        print(f"- 是否唯一解: {'是' if solution_count == 1 else '否'}")
        
        # 验证谜题可解性
        test_puzzle = [row[:] for row in puzzle]  # 深拷贝
        is_solvable = generator.solve(test_puzzle)
        print(f"- 是否可解: {'是' if is_solvable else '否'}")
        
        # 验证解的正确性
        is_correct = True
        for row in range(generator.size):
            for col in range(generator.size):
                if puzzle[row][col] != 0 and puzzle[row][col] != test_puzzle[row][col]:
                    is_correct = False
                    break
        print(f"- 解是否正确: {'是' if is_correct else '否'}")

def demo_different_sizes():
    """演示不同大小的数独生成"""
    print("\n\n不同大小的数独生成演示")
    print("=" * 60)
    
    sizes = [4, 6, 9]
    
    for size in sizes:
        print(f"\n{size}x{size} 数独:")
        print("-" * 30)
        
        generator = SudokuGenerator(size)
        
        # 生成完整解
        complete_solution = generator.generate_complete_grid()
        print(f"完整解 ({size}x{size}):")
        print_grid(complete_solution)
        
        # 生成normal难度的谜题
        puzzle, solution = generator.generate_puzzle('normal')
        
        empty_cells = sum(1 for row in puzzle for cell in row if cell == 0)
        total_cells = size * size
        empty_percentage = empty_cells / total_cells * 100
        
        print(f"\n谜题 (挖空 {empty_percentage:.1f}%):")
        print_grid(puzzle)
        
        # 验证唯一性
        solution_count = generator.count_solutions(puzzle, 3)
        print(f"解的数量: {solution_count}")

def demo_unique_solution_verification():
    """演示解唯一性验证"""
    print("\n\n解唯一性验证演示")
    print("=" * 60)
    
    generator = SudokuGenerator(9)
    
    # 创建一个有多个解的例子（通过移除太多数字）
    complete_solution = generator.generate_complete_grid()
    
    # 创建一个测试网格，移除太多数字
    test_puzzle = [row[:] for row in complete_solution]
    
    # 移除大部分数字，只保留很少的数字
    cells_to_remove = 70  # 移除70个数字，只保留11个
    removed = 0
    attempts = 0
    
    while removed < cells_to_remove and attempts < 1000:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        
        if test_puzzle[row][col] != 0:
            test_puzzle[row][col] = 0
            removed += 1
        
        attempts += 1
    
    print("测试网格（移除太多数字，可能有多个解）:")
    print_grid(test_puzzle)
    
    # 检查解的数量
    solution_count = generator.count_solutions(test_puzzle, 5)
    print(f"\n解的数量: {solution_count}")
    
    if solution_count > 1:
        print("⚠️  这个谜题有多个解，不符合唯一解要求")
    elif solution_count == 1:
        print("✅ 这个谜题有唯一解")
    else:
        print("❌ 这个谜题无解")

if __name__ == "__main__":
    # 运行所有演示
    demo_sudoku_generation()
    demo_different_sizes()
    demo_unique_solution_verification()
    
    print("\n\n演示完成！")
    print("=" * 60)
    print("总结:")
    print("1. ✅ 先生成完整解")
    print("2. ✅ 再随机挖空")
    print("3. ✅ 不同难度代表不同挖空比例")
    print("4. ✅ 检测确保解唯一")
    print("5. ✅ 支持多种网格大小 (4x4, 6x6, 9x9)")