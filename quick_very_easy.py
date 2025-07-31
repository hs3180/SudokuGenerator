#!/usr/bin/env python3
"""
快速生成Very Easy数独PDF - 简化版本

快速生成三种尺寸(4x4, 6x6, 9x9)的Very Easy数独PDF
"""

import random
from sudoku.generator import SudokuGenerator
from sudoku.printer import SudokuPrinter

def quick_generate():
    """快速生成Very Easy数独PDF"""
    print("快速生成Very Easy数独PDF...")
    
    # 设置随机种子
    random.seed(42)
    
    sizes = [4, 6, 9]
    difficulty = 'very_easy'
    puzzles = []
    
    # 为每种尺寸生成2个谜题
    for size in sizes:
        print(f"生成 {size}×{size} Very Easy 数独...")
        generator = SudokuGenerator(size)
        
        for i in range(2):  # 每种尺寸2个谜题
            print(f"  谜题 {i+1}/2...", end=" ", flush=True)
            try:
                puzzle, solution = generator.generate_puzzle(difficulty)
                puzzles.append((puzzle, solution, difficulty, size))
                print("✓")
            except Exception as e:
                print(f"✗ 错误: {e}")
                continue
    
    if not puzzles:
        print("错误: 没有成功生成任何谜题")
        return
    
    # 创建PDF
    print(f"\n创建PDF文件...")
    printer = SudokuPrinter()
    
    try:
        printer.create_pdf(
            puzzles=puzzles,
            per_page=1,  # 每页1个谜题
            output_file="very_easy_sudoku.pdf",
            cell_size=40,
            font_size=20,
            include_solutions=True,
            title="Very Easy Sudoku Puzzles",
            subtitle=f"Generated {len(puzzles)} puzzles (4×4, 6×6, 9×9)"
        )
        
        print("✓ PDF文件已生成: very_easy_sudoku.pdf")
        
        # 显示统计
        size_counts = {}
        for _, _, _, size in puzzles:
            size_counts[size] = size_counts.get(size, 0) + 1
        
        print(f"\n统计信息:")
        for size in [4, 6, 9]:
            count = size_counts.get(size, 0)
            print(f"  {size}×{size}: {count} 个谜题")
        
    except Exception as e:
        print(f"✗ 生成PDF时出错: {e}")

if __name__ == "__main__":
    quick_generate()