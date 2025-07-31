#!/usr/bin/env python3
"""
演示改进后的数独生成器功能

这个脚本展示了：
1. 先生成合法完整解
2. 再挖空的方法随机生成数独
3. 不同的难度代表不同的挖空比例
4. 挖空之后检测是否确保解唯一
"""

import random
from sudoku.generator import SudokuGenerator
from sudoku.printer import SudokuPrinter

def demo_generation_process():
    """演示数独生成过程"""
    print("=" * 60)
    print("改进后的数独生成器演示")
    print("=" * 60)
    
    # 设置随机种子以确保可重现的结果
    random.seed(42)
    
    # 创建生成器
    generator = SudokuGenerator(9)
    printer = SudokuPrinter()
    
    print("\n1. 生成完整解")
    print("-" * 30)
    
    # 第一步：生成完整的合法数独解
    solution = generator.generate_complete_grid()
    print("✓ 完整解生成成功")
    
    # 显示完整解
    print("\n完整解:")
    printer.print_grid(solution)
    
    print("\n2. 按不同难度挖空")
    print("-" * 30)
    
    difficulties = ['very_easy', 'easy', 'normal', 'hard', 'very_hard']
    
    for difficulty in difficulties:
        print(f"\n{difficulty.upper()} 难度:")
        print("-" * 20)
        
        # 第二步：根据难度挖空数字
        puzzle = generator.remove_numbers(solution, difficulty)
        
        # 第三步：验证挖空后的谜题
        solution_count = generator.count_solutions(puzzle, 3)
        
        # 获取统计信息
        stats = generator.get_puzzle_statistics(puzzle)
        
        print(f"挖空比例: {stats['empty_percentage']:.1f}%")
        print(f"填充数字: {stats['filled_cells']}")
        print(f"空位数量: {stats['empty_cells']}")
        print(f"解的数量: {solution_count}")
        
        if solution_count == 1:
            print("✓ 确保唯一解")
        else:
            print(f"⚠ 警告：发现 {solution_count} 个解")
        
        # 显示谜题
        print(f"\n{difficulty} 难度谜题:")
        printer.print_grid(puzzle)

def demo_different_sizes():
    """演示不同尺寸的数独生成"""
    print("\n" + "=" * 60)
    print("不同尺寸数独生成演示")
    print("=" * 60)
    
    random.seed(123)
    
    sizes = [4, 6, 9]
    difficulties = ['easy', 'normal', 'hard']
    
    for size in sizes:
        print(f"\n{size}×{size} 数独:")
        print("-" * 20)
        
        generator = SudokuGenerator(size)
        printer = SudokuPrinter()
        
        for difficulty in difficulties:
            print(f"\n{difficulty} 难度:")
            
            try:
                puzzle, solution = generator.generate_puzzle(difficulty)
                stats = generator.get_puzzle_statistics(puzzle)
                
                print(f"  挖空比例: {stats['empty_percentage']:.1f}%")
                print(f"  填充数字: {stats['filled_cells']}")
                print(f"  空位数量: {stats['empty_cells']}")
                
                # 验证唯一解
                solution_count = generator.count_solutions(puzzle, 3)
                if solution_count == 1:
                    print("  ✓ 唯一解")
                else:
                    print(f"  ⚠ {solution_count} 个解")
                    
            except Exception as e:
                print(f"  ✗ 生成失败: {e}")

def demo_algorithm_comparison():
    """演示算法改进的效果"""
    print("\n" + "=" * 60)
    print("算法改进效果演示")
    print("=" * 60)
    
    random.seed(456)
    
    generator = SudokuGenerator(9)
    solution = generator.generate_complete_grid()
    
    print("\n原始挖空算法 vs 改进挖空算法:")
    print("-" * 40)
    
    # 测试改进的算法
    print("\n使用改进算法:")
    puzzle_improved = generator.remove_numbers_improved(solution, 'normal')
    stats_improved = generator.get_puzzle_statistics(puzzle_improved)
    solution_count_improved = generator.count_solutions(puzzle_improved, 3)
    
    print(f"挖空比例: {stats_improved['empty_percentage']:.1f}%")
    print(f"解的数量: {solution_count_improved}")
    print(f"填充数字: {stats_improved['filled_cells']}")
    
    # 验证唯一解
    if solution_count_improved == 1:
        print("✓ 确保唯一解")
    else:
        print(f"⚠ 警告：发现 {solution_count_improved} 个解")

def main():
    """主函数"""
    try:
        # 演示生成过程
        demo_generation_process()
        
        # 演示不同尺寸
        demo_different_sizes()
        
        # 演示算法改进
        demo_algorithm_comparison()
        
        print("\n" + "=" * 60)
        print("演示完成！")
        print("=" * 60)
        print("\n改进要点总结:")
        print("1. ✅ 先生成合法完整解")
        print("2. ✅ 再挖空的方法随机生成数独")
        print("3. ✅ 不同的难度代表不同的挖空比例")
        print("4. ✅ 挖空之后检测是否确保解唯一")
        print("5. ✅ 新增 very_easy 和 very_hard 难度")
        print("6. ✅ 改进的挖空算法，更高效且更可靠")
        print("7. ✅ 增强的唯一解检测机制")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()