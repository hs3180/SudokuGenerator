#!/usr/bin/env python3
"""
生成三种尺寸(4x4, 6x6, 9x9)的Very Easy数独PDF

使用方法:
    python generate_very_easy_pdf.py --count 3 --per-page 1
    python generate_very_easy_pdf.py --count 6 --per-page 2 --output very_easy_sudoku.pdf
"""

import argparse
import random
import sys
from typing import List, Tuple, Optional
from sudoku.generator import SudokuGenerator
from sudoku.printer import SudokuPrinter

def generate_very_easy_puzzles(count_per_size: int = 2, seed: Optional[int] = None) -> List[Tuple[List[List[int]], List[List[int]], str, int]]:
    """
    生成三种尺寸的Very Easy数独谜题
    
    Args:
        count_per_size: 每种尺寸生成的谜题数量
        seed: 随机种子
        
    Returns:
        包含(谜题, 解答, 难度, 尺寸)的列表
    """
    if seed is not None:
        random.seed(seed)
    
    sizes = [4, 6, 9]
    difficulty = 'very_easy'
    puzzles = []
    
    print(f"生成 {count_per_size} 个每种尺寸的 Very Easy 数独谜题...")
    
    for size in sizes:
        print(f"\n生成 {size}×{size} Very Easy 数独:")
        generator = SudokuGenerator(size)
        
        for i in range(count_per_size):
            print(f"  谜题 {i+1}/{count_per_size}...", end=" ", flush=True)
            try:
                puzzle, solution = generator.generate_puzzle(difficulty)
                puzzles.append((puzzle, solution, difficulty, size))
                print("✓")
            except Exception as e:
                print(f"✗ 错误: {e}")
                # 重试一次
                try:
                    puzzle, solution = generator.generate_puzzle(difficulty)
                    puzzles.append((puzzle, solution, difficulty, size))
                    print("✓ (重试成功)")
                except Exception as e2:
                    print(f"✗ 重试失败: {e2}")
                    continue
    
    return puzzles

def create_very_easy_pdf(puzzles: List[Tuple[List[List[int]], List[List[int]], str, int]], 
                        per_page: int = 1, 
                        output_file: str = "very_easy_sudoku.pdf",
                        include_solutions: bool = True):
    """
    创建Very Easy数独PDF
    
    Args:
        puzzles: 谜题列表
        per_page: 每页谜题数量
        output_file: 输出文件名
        include_solutions: 是否包含解答
    """
    if not puzzles:
        print("没有可用的谜题，无法生成PDF")
        return
    
    print(f"\n创建PDF文件: {output_file}")
    print(f"每页谜题数量: {per_page}")
    print(f"包含解答: {'是' if include_solutions else '否'}")
    
    try:
        printer = SudokuPrinter()
        
        # 设置适合Very Easy难度的格式
        if per_page == 1:
            # 单页格式：谜题和解答并排
            cell_size = 40
            font_size = 20
        elif per_page == 2:
            # 双页格式：两个谜题
            cell_size = 35
            font_size = 18
        else:
            # 多页格式：紧凑布局
            cell_size = 30
            font_size = 16
        
        # 创建PDF
        printer.create_pdf(
            puzzles=puzzles,
            per_page=per_page,
            output_file=output_file,
            cell_size=cell_size,
            font_size=font_size,
            include_solutions=include_solutions,
            title="Very Easy Sudoku Puzzles",
            subtitle=f"Generated {len(puzzles)} puzzles (4×4, 6×6, 9×9)"
        )
        
        print(f"✓ PDF文件已生成: {output_file}")
        
        # 显示统计信息
        size_counts = {}
        for _, _, _, size in puzzles:
            size_counts[size] = size_counts.get(size, 0) + 1
        
        print(f"\n统计信息:")
        for size in [4, 6, 9]:
            count = size_counts.get(size, 0)
            print(f"  {size}×{size}: {count} 个谜题")
        
    except Exception as e:
        print(f"✗ 生成PDF时出错: {e}")
        import traceback
        traceback.print_exc()

def main():
    parser = argparse.ArgumentParser(
        description="生成三种尺寸(4x4, 6x6, 9x9)的Very Easy数独PDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    # 生成每种尺寸2个谜题，每页1个
    python generate_very_easy_pdf.py --count 2 --per-page 1
    
    # 生成每种尺寸3个谜题，每页2个，不包含解答
    python generate_very_easy_pdf.py --count 3 --per-page 2 --no-solutions
    
    # 指定输出文件名
    python generate_very_easy_pdf.py --count 2 --per-page 1 --output my_very_easy.pdf
    
    # 使用固定种子确保可重现
    python generate_very_easy_pdf.py --count 2 --per-page 1 --seed 42
        """
    )
    
    parser.add_argument(
        "--count",
        type=int,
        default=2,
        help="每种尺寸生成的谜题数量 (默认: 2)"
    )
    
    parser.add_argument(
        "--per-page",
        type=int,
        choices=[1, 2, 3, 4],
        default=1,
        help="每页谜题数量 (默认: 1)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="very_easy_sudoku.pdf",
        help="输出PDF文件名 (默认: very_easy_sudoku.pdf)"
    )
    
    parser.add_argument(
        "--no-solutions",
        action="store_true",
        help="不包含解答页面"
    )
    
    parser.add_argument(
        "--seed",
        type=int,
        help="随机种子，用于可重现的生成结果"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="显示详细输出"
    )
    
    args = parser.parse_args()
    
    # 验证参数
    if args.count < 1:
        print("错误: 每种尺寸的谜题数量必须至少为1")
        sys.exit(1)
    
    if args.count > 10:
        print("警告: 每种尺寸生成超过10个谜题可能需要较长时间")
    
    print("=" * 60)
    print("Very Easy 数独生成器")
    print("=" * 60)
    print(f"尺寸: 4×4, 6×6, 9×9")
    print(f"难度: Very Easy")
    print(f"每种尺寸谜题数量: {args.count}")
    print(f"每页谜题数量: {args.per_page}")
    print(f"输出文件: {args.output}")
    print(f"包含解答: {'否' if args.no_solutions else '是'}")
    if args.seed:
        print(f"随机种子: {args.seed}")
    print("=" * 60)
    
    try:
        # 生成谜题
        puzzles = generate_very_easy_puzzles(
            count_per_size=args.count,
            seed=args.seed
        )
        
        if not puzzles:
            print("错误: 没有成功生成任何谜题")
            sys.exit(1)
        
        # 创建PDF
        create_very_easy_pdf(
            puzzles=puzzles,
            per_page=args.per_page,
            output_file=args.output,
            include_solutions=not args.no_solutions
        )
        
        print("\n" + "=" * 60)
        print("生成完成！")
        print("=" * 60)
        print(f"总谜题数量: {len(puzzles)}")
        print(f"PDF文件: {args.output}")
        
        if args.verbose:
            print(f"\n详细统计:")
            size_counts = {}
            for _, _, _, size in puzzles:
                size_counts[size] = size_counts.get(size, 0) + 1
            
            for size in [4, 6, 9]:
                count = size_counts.get(size, 0)
                print(f"  {size}×{size}: {count} 个谜题")
        
    except KeyboardInterrupt:
        print("\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n发生错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()