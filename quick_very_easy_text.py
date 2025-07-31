#!/usr/bin/env python3
"""
快速生成Very Easy数独 - 纯文本版本

快速生成三种尺寸(4x4, 6x6, 9x9)的Very Easy数独，输出到文本文件
"""

import random
from sudoku.generator import SudokuGenerator

def print_grid(grid, title=""):
    """打印数独网格到控制台"""
    size = len(grid)
    box_height = int(size ** 0.5) if size == 4 or size == 9 else 2
    box_width = int(size ** 0.5) if size == 4 or size == 9 else 3
    
    if title:
        print(f"\n{title}")
        print("-" * (size * 3 + 2))
    
    for i, row in enumerate(grid):
        if i % box_height == 0 and i != 0:
            print("-" * (size * 3 + 2))
        
        row_str = "|"
        for j, cell in enumerate(row):
            if j % box_width == 0 and j != 0:
                row_str += "|"
            if cell == 0:
                row_str += " . "
            else:
                row_str += f" {cell} "
        row_str += "|"
        print(row_str)
    
    print("-" * (size * 3 + 2))

def save_to_text(puzzles, filename="very_easy_sudoku.txt"):
    """保存数独到文本文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Very Easy Sudoku Puzzles\n")
        f.write("=" * 50 + "\n\n")
        
        for i, (puzzle, solution, difficulty, size) in enumerate(puzzles, 1):
            f.write(f"Puzzle {i} ({size}×{size} {difficulty})\n")
            f.write("=" * 30 + "\n\n")
            
            # 打印谜题
            f.write("PUZZLE:\n")
            size = len(puzzle)
            box_height = int(size ** 0.5) if size == 4 or size == 9 else 2
            box_width = int(size ** 0.5) if size == 4 or size == 9 else 3
            
            for i, row in enumerate(puzzle):
                if i % box_height == 0 and i != 0:
                    f.write("-" * (size * 3 + 2) + "\n")
                
                row_str = "|"
                for j, cell in enumerate(row):
                    if j % box_width == 0 and j != 0:
                        row_str += "|"
                    if cell == 0:
                        row_str += " . "
                    else:
                        row_str += f" {cell} "
                row_str += "|"
                f.write(row_str + "\n")
            
            f.write("-" * (size * 3 + 2) + "\n\n")
            
            # 打印解答
            f.write("SOLUTION:\n")
            for i, row in enumerate(solution):
                if i % box_height == 0 and i != 0:
                    f.write("-" * (size * 3 + 2) + "\n")
                
                row_str = "|"
                for j, cell in enumerate(row):
                    if j % box_width == 0 and j != 0:
                        row_str += "|"
                    row_str += f" {cell} "
                row_str += "|"
                f.write(row_str + "\n")
            
            f.write("-" * (size * 3 + 2) + "\n\n")
            f.write("\n" + "=" * 50 + "\n\n")

def quick_generate_text():
    """快速生成Very Easy数独文本文件"""
    print("快速生成Very Easy数独文本文件...")
    
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
    
    # 保存到文本文件
    filename = "very_easy_sudoku.txt"
    print(f"\n保存到文本文件: {filename}")
    
    try:
        save_to_text(puzzles, filename)
        print(f"✓ 文本文件已生成: {filename}")
        
        # 显示统计
        size_counts = {}
        for _, _, _, size in puzzles:
            size_counts[size] = size_counts.get(size, 0) + 1
        
        print(f"\n统计信息:")
        for size in [4, 6, 9]:
            count = size_counts.get(size, 0)
            print(f"  {size}×{size}: {count} 个谜题")
        
        # 显示前几个谜题预览
        print(f"\n预览 (前2个谜题):")
        for i, (puzzle, solution, difficulty, size) in enumerate(puzzles[:2]):
            print_grid(puzzle, f"谜题 {i+1} ({size}×{size} {difficulty})")
            print_grid(solution, f"解答 {i+1}")
        
    except Exception as e:
        print(f"✗ 生成文本文件时出错: {e}")

if __name__ == "__main__":
    quick_generate_text()