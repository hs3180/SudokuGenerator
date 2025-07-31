#!/bin/bash

# Very Easy 数独生成器 Shell 脚本
# 生成三种尺寸(4x4, 6x6, 9x9)的Very Easy数独

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 默认参数
COUNT=2
OUTPUT_FORMAT="html"
OUTPUT_FILE="very_easy_sudoku"
SEED="42"
VERBOSE=false

# 显示帮助信息
show_help() {
    echo -e "${BLUE}Very Easy 数独生成器${NC}"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -c, --count NUM     每种尺寸生成的谜题数量 (默认: 2)"
    echo "  -f, --format FORMAT 输出格式: text, html (默认: html)"
    echo "  -o, --output FILE   输出文件名 (默认: very_easy_sudoku)"
    echo "  -s, --seed NUM      随机种子 (默认: 42)"
    echo "  -v, --verbose       显示详细输出"
    echo "  -h, --help          显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0                    # 使用默认设置"
    echo "  $0 -c 3 -f text      # 生成3个每种尺寸的文本文件"
    echo "  $0 -c 1 -f html -o my_puzzles  # 生成HTML文件"
    echo ""
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--count)
            COUNT="$2"
            shift 2
            ;;
        -f|--format)
            OUTPUT_FORMAT="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -s|--seed)
            SEED="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}错误: 未知参数 $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# 验证参数
if ! [[ "$COUNT" =~ ^[1-9][0-9]*$ ]]; then
    echo -e "${RED}错误: 谜题数量必须是正整数${NC}"
    exit 1
fi

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "html" ]]; then
    echo -e "${RED}错误: 输出格式必须是 'text' 或 'html'${NC}"
    exit 1
fi

# 检查Python是否可用
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到 python3${NC}"
    exit 1
fi

# 检查必要的Python文件是否存在
if [[ ! -f "sudoku/generator.py" ]]; then
    echo -e "${RED}错误: 未找到 sudoku/generator.py${NC}"
    exit 1
fi

# 显示配置信息
echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}Very Easy 数独生成器${NC}"
echo -e "${BLUE}============================================================${NC}"
echo -e "尺寸: ${YELLOW}4×4, 6×6, 9×9${NC}"
echo -e "难度: ${YELLOW}Very Easy${NC}"
echo -e "每种尺寸谜题数量: ${YELLOW}$COUNT${NC}"
echo -e "输出格式: ${YELLOW}$OUTPUT_FORMAT${NC}"
echo -e "输出文件: ${YELLOW}${OUTPUT_FILE}.${OUTPUT_FORMAT}${NC}"
echo -e "随机种子: ${YELLOW}$SEED${NC}"
echo -e "${BLUE}============================================================${NC}"

# 创建临时Python脚本
TEMP_SCRIPT=$(mktemp)
trap "rm -f $TEMP_SCRIPT" EXIT

cat > "$TEMP_SCRIPT" << 'EOF'
#!/usr/bin/env python3
import random
import sys
from sudoku.generator import SudokuGenerator

def generate_puzzles(count_per_size, seed, output_format, output_file):
    """生成数独谜题"""
    if seed:
        random.seed(int(seed))
    
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
                continue
    
    if not puzzles:
        print("错误: 没有成功生成任何谜题")
        return False
    
    # 根据格式生成输出
    if output_format == "text":
        generate_text_output(puzzles, output_file)
    elif output_format == "html":
        generate_html_output(puzzles, output_file)
    
    return True

def generate_text_output(puzzles, output_file):
    """生成文本输出"""
    filename = f"{output_file}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Very Easy Sudoku Puzzles\n")
        f.write("=" * 50 + "\n\n")
        
        for i, (puzzle, solution, difficulty, size) in enumerate(puzzles, 1):
            f.write(f"Puzzle {i} ({size}×{size} {difficulty})\n")
            f.write("=" * 30 + "\n\n")
            
            # 打印谜题
            f.write("PUZZLE:\n")
            print_grid_to_file(puzzle, f)
            f.write("\nSOLUTION:\n")
            print_grid_to_file(solution, f)
            f.write("\n" + "=" * 50 + "\n\n")
    
    print(f"✓ 文本文件已生成: {filename}")

def generate_html_output(puzzles, output_file):
    """生成HTML输出"""
    filename = f"{output_file}.html"
    
    html_content = generate_html_content(puzzles)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ HTML文件已生成: {filename}")

def print_grid_to_file(grid, file):
    """将网格打印到文件"""
    size = len(grid)
    box_height = int(size ** 0.5) if size == 4 or size == 9 else 2
    box_width = int(size ** 0.5) if size == 4 or size == 9 else 3
    
    for i, row in enumerate(grid):
        if i % box_height == 0 and i != 0:
            file.write("-" * (size * 3 + 2) + "\n")
        
        row_str = "|"
        for j, cell in enumerate(row):
            if j % box_width == 0 and j != 0:
                row_str += "|"
            if cell == 0:
                row_str += " . "
            else:
                row_str += f" {cell} "
        row_str += "|"
        file.write(row_str + "\n")
    
    file.write("-" * (size * 3 + 2) + "\n")

def generate_html_content(puzzles):
    """生成HTML内容"""
    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Very Easy Sudoku Puzzles</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
        .puzzle-section { margin: 30px 0; page-break-inside: avoid; }
        .puzzle-title { font-size: 18px; font-weight: bold; color: #007bff; margin-bottom: 15px; text-align: center; }
        .grid-container { display: flex; justify-content: space-around; margin: 20px 0; flex-wrap: wrap; }
        .grid-section { text-align: center; margin: 10px; }
        .grid-label { font-weight: bold; margin-bottom: 10px; color: #555; }
        .sudoku-grid { border-collapse: collapse; margin: 0 auto; background-color: white; }
        .sudoku-grid td { border: 1px solid #ccc; width: 40px; height: 40px; text-align: center; font-size: 16px; font-weight: bold; }
        .sudoku-grid td.empty { background-color: #f8f9fa; color: #6c757d; }
        .sudoku-grid td.filled { background-color: #e3f2fd; color: #1976d2; }
        .sudoku-grid td:nth-child(2) { border-right: 3px solid #333; }
        .sudoku-grid td:nth-child(4) { border-right: 3px solid #333; }
        .sudoku-grid tr:nth-child(2) td { border-bottom: 3px solid #333; }
        .sudoku-grid tr:nth-child(4) td { border-bottom: 3px solid #333; }
        .sudoku-grid-6x6 td:nth-child(3) { border-right: 3px solid #333; }
        .sudoku-grid-6x6 tr:nth-child(2) td { border-bottom: 3px solid #333; }
        .sudoku-grid-6x6 tr:nth-child(4) td { border-bottom: 3px solid #333; }
        .sudoku-grid-9x9 td:nth-child(3) { border-right: 3px solid #333; }
        .sudoku-grid-9x9 td:nth-child(6) { border-right: 3px solid #333; }
        .sudoku-grid-9x9 tr:nth-child(3) td { border-bottom: 3px solid #333; }
        .sudoku-grid-9x9 tr:nth-child(6) td { border-bottom: 3px solid #333; }
        .stats { background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .stats h3 { margin-top: 0; color: #333; }
        .stats ul { margin: 0; padding-left: 20px; }
        .stats li { margin: 5px 0; }
        @media print { body { background-color: white; } .container { box-shadow: none; } .puzzle-section { page-break-inside: avoid; } }
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
    
    return html_content

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("用法: python3 script.py count seed format output_file")
        sys.exit(1)
    
    count = int(sys.argv[1])
    seed = sys.argv[2]
    format_type = sys.argv[3]
    output_file = sys.argv[4]
    
    success = generate_puzzles(count, seed, format_type, output_file)
    if not success:
        sys.exit(1)
EOF

# 运行Python脚本
echo -e "${GREEN}开始生成数独谜题...${NC}"
if PYTHONPATH=. python3 "$TEMP_SCRIPT" "$COUNT" "$SEED" "$OUTPUT_FORMAT" "$OUTPUT_FILE"; then
    echo -e "${GREEN}============================================================${NC}"
    echo -e "${GREEN}生成完成！${NC}"
    echo -e "${GREEN}============================================================${NC}"
    
    # 显示统计信息
    TOTAL_PUZZLES=$((COUNT * 3))
    echo -e "总谜题数量: ${YELLOW}$TOTAL_PUZZLES${NC}"
    echo -e "输出文件: ${YELLOW}${OUTPUT_FILE}.${OUTPUT_FORMAT}${NC}"
    
    if [[ "$OUTPUT_FORMAT" == "html" ]]; then
        echo -e "\n${BLUE}使用说明:${NC}"
        echo -e "1. 在浏览器中打开 ${YELLOW}${OUTPUT_FILE}.html${NC}"
        echo -e "2. 使用浏览器的打印功能 (Ctrl+P)"
        echo -e "3. 选择'保存为PDF'选项"
        echo -e "4. 或者直接打印到纸张"
    fi
    
    # 显示文件信息
    if [[ -f "${OUTPUT_FILE}.${OUTPUT_FORMAT}" ]]; then
        FILE_SIZE=$(du -h "${OUTPUT_FILE}.${OUTPUT_FORMAT}" | cut -f1)
        echo -e "\n文件大小: ${YELLOW}$FILE_SIZE${NC}"
    fi
    
else
    echo -e "${RED}生成失败！${NC}"
    exit 1
fi