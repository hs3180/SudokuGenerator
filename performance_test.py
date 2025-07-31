#!/usr/bin/env python3
"""
数独生成器性能测试脚本
测试生成速度、成功率和质量
"""

import time
import random
from sudoku.generator import SudokuGenerator

def test_generation_speed():
    """测试生成速度"""
    print("数独生成器性能测试")
    print("=" * 60)
    
    sizes = [4, 6, 9]
    difficulties = ['easy', 'normal', 'hard']
    
    for size in sizes:
        print(f"\n{size}×{size} 数独生成速度测试:")
        print("-" * 40)
        
        generator = SudokuGenerator(size)
        
        for difficulty in difficulties:
            times = []
            success_count = 0
            total_attempts = 10
            
            print(f"  难度: {difficulty}")
            
            for i in range(total_attempts):
                start_time = time.time()
                try:
                    puzzle, solution = generator.generate_puzzle(difficulty)
                    end_time = time.time()
                    generation_time = end_time - start_time
                    times.append(generation_time)
                    success_count += 1
                    
                    # 验证解的唯一性
                    solution_count = generator.count_solutions(puzzle, 3)
                    if solution_count != 1:
                        print(f"    ⚠️  尝试 {i+1}: 生成时间 {generation_time:.3f}s, 但解不唯一 ({solution_count} 个解)")
                    else:
                        print(f"    ✅ 尝试 {i+1}: 生成时间 {generation_time:.3f}s")
                        
                except Exception as e:
                    print(f"    ❌ 尝试 {i+1}: 生成失败 - {e}")
            
            if times:
                avg_time = sum(times) / len(times)
                min_time = min(times)
                max_time = max(times)
                success_rate = success_count / total_attempts * 100
                
                print(f"    平均时间: {avg_time:.3f}s")
                print(f"    最快时间: {min_time:.3f}s")
                print(f"    最慢时间: {max_time:.3f}s")
                print(f"    成功率: {success_rate:.1f}%")
            else:
                print(f"    ❌ 所有尝试都失败了")

def test_difficulty_distribution():
    """测试不同难度的挖空分布"""
    print("\n\n难度分布测试")
    print("=" * 60)
    
    generator = SudokuGenerator(9)
    difficulties = ['easy', 'normal', 'hard']
    
    for difficulty in difficulties:
        print(f"\n{difficulty} 难度测试 (10个样本):")
        print("-" * 30)
        
        empty_percentages = []
        
        for i in range(10):
            puzzle, solution = generator.generate_puzzle(difficulty)
            empty_cells = sum(1 for row in puzzle for cell in row if cell == 0)
            total_cells = 81
            empty_percentage = empty_cells / total_cells * 100
            empty_percentages.append(empty_percentage)
            
            print(f"  样本 {i+1}: {empty_percentage:.1f}% ({empty_cells}/{total_cells})")
        
        avg_percentage = sum(empty_percentages) / len(empty_percentages)
        target_percentage = generator.difficulty_settings[9][difficulty] * 100
        
        print(f"  平均挖空比例: {avg_percentage:.1f}%")
        print(f"  目标挖空比例: {target_percentage:.1f}%")
        print(f"  偏差: {abs(avg_percentage - target_percentage):.1f}%")

def test_unique_solution_quality():
    """测试解唯一性的质量"""
    print("\n\n解唯一性质量测试")
    print("=" * 60)
    
    generator = SudokuGenerator(9)
    difficulties = ['easy', 'normal', 'hard']
    
    for difficulty in difficulties:
        print(f"\n{difficulty} 难度唯一性测试:")
        print("-" * 30)
        
        unique_count = 0
        total_tests = 20
        
        for i in range(total_tests):
            puzzle, solution = generator.generate_puzzle(difficulty)
            solution_count = generator.count_solutions(puzzle, 5)  # 检查前5个解
            
            if solution_count == 1:
                unique_count += 1
                print(f"  ✅ 测试 {i+1}: 唯一解")
            else:
                print(f"  ❌ 测试 {i+1}: {solution_count} 个解")
        
        unique_rate = unique_count / total_tests * 100
        print(f"  唯一解比例: {unique_rate:.1f}% ({unique_count}/{total_tests})")

def test_different_sizes_quality():
    """测试不同大小数独的质量"""
    print("\n\n不同大小数独质量测试")
    print("=" * 60)
    
    sizes = [4, 6, 9]
    
    for size in sizes:
        print(f"\n{size}×{size} 数独质量测试:")
        print("-" * 30)
        
        generator = SudokuGenerator(size)
        
        # 测试完整解的有效性
        complete_solution = generator.generate_complete_grid()
        
        # 验证行
        valid_rows = True
        for i, row in enumerate(complete_solution):
            if set(row) != set(range(1, size + 1)):
                valid_rows = False
                break
        
        # 验证列
        valid_cols = True
        for col in range(size):
            col_values = [complete_solution[row][col] for row in range(size)]
            if set(col_values) != set(range(1, size + 1)):
                valid_cols = False
                break
        
        # 验证方块
        valid_boxes = True
        box_height = generator.box_height
        box_width = generator.box_width
        
        for box_row in range(0, size, box_height):
            for box_col in range(0, size, box_width):
                box_values = []
                for r in range(box_row, box_row + box_height):
                    for c in range(box_col, box_col + box_width):
                        box_values.append(complete_solution[r][c])
                
                if set(box_values) != set(range(1, size + 1)):
                    valid_boxes = False
                    break
        
        print(f"  完整解验证:")
        print(f"    行有效性: {'✅' if valid_rows else '❌'}")
        print(f"    列有效性: {'✅' if valid_cols else '❌'}")
        print(f"    方块有效性: {'✅' if valid_boxes else '❌'}")
        
        # 测试谜题生成
        puzzle, solution = generator.generate_puzzle('normal')
        solution_count = generator.count_solutions(puzzle, 3)
        
        print(f"  谜题验证:")
        print(f"    解唯一性: {'✅' if solution_count == 1 else '❌'} ({solution_count} 个解)")

def main():
    """运行所有性能测试"""
    # 设置随机种子以确保可重现的结果
    random.seed(42)
    
    test_generation_speed()
    test_difficulty_distribution()
    test_unique_solution_quality()
    test_different_sizes_quality()
    
    print("\n\n性能测试完成！")
    print("=" * 60)
    print("测试总结:")
    print("1. ✅ 生成速度测试")
    print("2. ✅ 难度分布测试")
    print("3. ✅ 解唯一性质量测试")
    print("4. ✅ 不同大小数独质量测试")

if __name__ == "__main__":
    main()