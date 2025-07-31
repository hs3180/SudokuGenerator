#!/usr/bin/env python3
"""
简化版数独生成器CLI - 不依赖fpdf
"""

import argparse
import random
import sys
from sudoku.generator import SudokuGenerator

def main():
    parser = argparse.ArgumentParser(description="生成Very Easy数独")
    parser.add_argument("--size", type=int, choices=[4, 6, 9], required=True, help="数独尺寸")
    parser.add_argument("--difficulty", default="very_easy", help="难度级别")
    parser.add_argument("--count", type=int, default=1, help="生成数量")
    parser.add_argument("--seed", type=int, help="随机种子")
    
    args = parser.parse_args()
    
    if args.seed:
        random.seed(args.seed)
    
    generator = SudokuGenerator(args.size)
    
    for i in range(args.count):
        print(f"生成 {args.size}×{args.size} {args.difficulty} 数独 {i+1}/{args.count}...")
        puzzle, solution = generator.generate_puzzle(args.difficulty)
        
        print("谜题:")
        for row in puzzle:
            print(' '.join(str(cell) if cell != 0 else '.' for cell in row))
        
        print("解答:")
        for row in solution:
            print(' '.join(str(cell) for cell in row))
        print()

if __name__ == "__main__":
    main()