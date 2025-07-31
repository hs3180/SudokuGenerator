#!/usr/bin/env python3
"""
快速生成Very Easy数独 - HTML版本

快速生成三种尺寸(4x4, 6x6, 9x9)的Very Easy数独，输出到HTML文件
可以打印为PDF
"""

import random
from sudoku.generator import SudokuGenerator

def generate_html(puzzles, filename="very_easy_sudoku.html"):
    """生成HTML格式的数独文件"""
    html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Very Easy Sudoku Puzzles</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }
        .puzzle-section {
            margin: 30px 0;
            page-break-inside: avoid;
        }
        .puzzle-title {
            font-size: 18px;
            font-weight: bold;
            color: #007bff;
            margin-bottom: 15px;
            text-align: center;
        }
        .grid-container {
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        .grid-section {
            text-align: center;
            margin: 10px;
        }
        .grid-label {
            font-weight: bold;
            margin-bottom: 10px;
            color: #555;
        }
        .sudoku-grid {
            border-collapse: collapse;
            margin: 0 auto;
            background-color: white;
        }
        .sudoku-grid td {
            border: 1px solid #ccc;
            width: 40px;
            height: 40px;
            text-align: center;
            font-size: 16px;
            font-weight: bold;
        }
        .sudoku-grid td.empty {
            background-color: #f8f9fa;
            color: #6c757d;
        }
        .sudoku-grid td.filled {
            background-color: #e3f2fd;
            color: #1976d2;
        }
        /* 粗边框分隔 */
        .sudoku-grid td:nth-child(2) { border-right: 3px solid #333; }
        .sudoku-grid td:nth-child(4) { border-right: 3px solid #333; }
        .sudoku-grid tr:nth-child(2) td { border-bottom: 3px solid #333; }
        .sudoku-grid tr:nth-child(4) td { border-bottom: 3px solid #333; }
        
        /* 6x6 特殊样式 */
        .sudoku-grid-6x6 td:nth-child(3) { border-right: 3px solid #333; }
        .sudoku-grid-6x6 tr:nth-child(2) td { border-bottom: 3px solid #333; }
        .sudoku-grid-6x6 tr:nth-child(4) td { border-bottom: 3px solid #333; }
        
        /* 9x9 特殊样式 */
        .sudoku-grid-9x9 td:nth-child(3) { border-right: 3px solid #333; }
        .sudoku-grid-9x9 td:nth-child(6) { border-right: 3px solid #333; }
        .sudoku-grid-9x9 tr:nth-child(3) td { border-bottom: 3px solid #333; }
        .sudoku-grid-9x9 tr:nth-child(6) td { border-bottom: 3px solid #333; }
        
        .stats {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .stats h3 {
            margin-top: 0;
            color: #333;
        }
        .stats ul {
            margin: 0;
            padding-left: 20px;
        }
        .stats li {
            margin: 5px 0;
        }
        
        @media print {
            body { background-color: white; }
            .container { box-shadow: none; }
            .puzzle-section { page-break-inside: avoid; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Very Easy Sudoku Puzzles</h1>
        
        <div class="stats">
            <h3>统计信息</h3>
            <ul>
"""
    
    # 添加统计信息
    size_counts = {}
    for _, _, _, size in puzzles:
        size_counts[size] = size_counts.get(size, 0) + 1
    
    for size in [4, 6, 9]:
        count = size_counts.get(size, 0)
        html_content += f"                <li>{size}×{size}: {count} 个谜题</li>\n"
    
    html_content += """
            </ul>
        </div>
"""
    
    # 添加每个谜题
    for i, (puzzle, solution, difficulty, size) in enumerate(puzzles, 1):
        html_content += f"""
        <div class="puzzle-section">
            <div class="puzzle-title">谜题 {i} ({size}×{size} {difficulty})</div>
            <div class="grid-container">
                <div class="grid-section">
                    <div class="grid-label">谜题</div>
                    <table class="sudoku-grid sudoku-grid-{size}x{size}">
"""
        
        # 生成谜题HTML
        for row_idx, row in enumerate(puzzle):
            html_content += "                        <tr>\n"
            for col_idx, cell in enumerate(row):
                if cell == 0:
                    html_content += "                            <td class='empty'></td>\n"
                else:
                    html_content += f"                            <td class='filled'>{cell}</td>\n"
            html_content += "                        </tr>\n"
        
        html_content += """
                    </table>
                </div>
                <div class="grid-section">
                    <div class="grid-label">解答</div>
                    <table class="sudoku-grid sudoku-grid-{size}x{size}">
""".format(size=size)
        
        # 生成解答HTML
        for row_idx, row in enumerate(solution):
            html_content += "                        <tr>\n"
            for col_idx, cell in enumerate(row):
                html_content += f"                            <td class='filled'>{cell}</td>\n"
            html_content += "                        </tr>\n"
        
        html_content += """
                    </table>
                </div>
            </div>
        </div>
"""
    
    html_content += """
    </div>
</body>
</html>
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

def quick_generate_html():
    """快速生成Very Easy数独HTML文件"""
    print("快速生成Very Easy数独HTML文件...")
    
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
    
    # 生成HTML文件
    filename = "very_easy_sudoku.html"
    print(f"\n生成HTML文件: {filename}")
    
    try:
        generate_html(puzzles, filename)
        print(f"✓ HTML文件已生成: {filename}")
        
        # 显示统计
        size_counts = {}
        for _, _, _, size in puzzles:
            size_counts[size] = size_counts.get(size, 0) + 1
        
        print(f"\n统计信息:")
        for size in [4, 6, 9]:
            count = size_counts.get(size, 0)
            print(f"  {size}×{size}: {count} 个谜题")
        
        print(f"\n使用说明:")
        print(f"1. 在浏览器中打开 {filename}")
        print(f"2. 使用浏览器的打印功能 (Ctrl+P)")
        print(f"3. 选择'保存为PDF'选项")
        print(f"4. 或者直接打印到纸张")
        
    except Exception as e:
        print(f"✗ 生成HTML文件时出错: {e}")

if __name__ == "__main__":
    quick_generate_html()