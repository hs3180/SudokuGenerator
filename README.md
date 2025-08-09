# SudokuGenerator

一个用于生成和打印数独谜题的 Python 项目，支持 4×4、6×6、9×9 三种尺寸，支持按页布局输出 PDF/HTML，并保证谜题唯一解（可配置）。

### 特性
- **保证唯一解**: 生成时校验解的唯一性（也可使用 `--allow-multiple-solutions` 提升速度）
- **多种尺寸**: 支持 4×4、6×6、9×9
- **难度分级**: `very_easy`、`easy`、`normal`、`hard`、`very_hard`；或用自定义挖空比例
- **多种输出**: 默认输出 PDF；也可输出 HTML 或仅在控制台显示
- **可打印排版**: 每页 1–9 个谜题，自动网格与粗边框
- **样式可配**: 网格/单元格边框、字号、颜色、页边距、标题等
- **可复现**: 支持随机种子 `--seed`
- **文件输入**: 可从文本文件读取并解析谜题
- **单元测试**: 包含生成与打印的测试

### 安装
```bash
pip install -r requirements.txt
# 可选：安装为命令行工具
pip install -e .
```
安装为命令行工具后，可直接使用 `sudoku-generator` 命令。

### 快速开始
- 生成 4 个 9×9 正常难度的数独，按每页 2 个排版（默认输出 PDF）
```bash
python cli.py --size 9 --difficulty normal --count 4 --per-page 2
# 或（若已安装为命令行）
sudoku-generator --size 9 --difficulty normal --count 4 --per-page 2
```
输出文件默认是 `sudoku_puzzles.pdf`。

- 仅在控制台输出（不生成文件）
```bash
python cli.py --size 6 --difficulty easy --count 2 --console
```

- 生成 HTML 文件（将输出文件扩展名设为 .html 即可）
```bash
python cli.py --size 9 --difficulty hard --output puzzles.html
```

### 命令行参数速览
- **基础设置**
  - `--size {4,6,9}`: 棋盘尺寸，默认 9
  - `--difficulty {very_easy,easy,normal,hard,very_hard}`: 难度，默认 `normal`
  - `--count N`: 生成谜题数量，默认 4（从文件读取时不需要）
  - `--per-page N`: 每页谜题数 1–9，默认 2
- **生成控制**
  - `--seed SEED`: 固定随机种子，便于复现
  - `--custom-difficulty PERCENT`: 自定义挖空比例 0.1–0.9，覆盖 `--difficulty`
  - `--max-attempts-multiplier N`: 生成尝试倍数，默认 10（更高更慢但质量更高）
  - `--allow-multiple-solutions`: 允许多解（更快但不保证唯一解）
- **样式与颜色**
  - `--cell-size/--font-size`: 单元格尺寸/字号（像素），按尺寸有默认值
  - `--solution-cell-size/--solution-font-size`: 解答页的单元格尺寸/字号
  - `--border-width/--cell-border-width/--thick-border-width`: 边框粗细
  - `--grid-color/--cell-border-color/--text-color/--background-color`: 颜色（十六进制）
- **页面布局**
  - `--page-margin`: 页边距（CSS 格式，默认 `0.5in`）
  - `--puzzle-margin`: 每个谜题外边距（默认 20）
  - `--title-font-size/--solution-title-font-size`: 标题字号
- **输入/输出**
  - `--no-solutions`: 不包含解答页
  - `--output FILE`: 输出文件名，默认 `sudoku_puzzles.pdf`
  - `--pdf`: 强制以 PDF 输出（通常无需设置，只要输出名以 `.pdf` 结尾即会输出 PDF）
  - `--console`: 输出到控制台（不生成文件）
  - `--mixed`: 生成混合尺寸与难度的集合
  - `--files FILE1 FILE2 ...`: 从指定文本文件读取谜题
  - `--file-pattern "PATTERN"`: 按通配符批量读取文件，如 `"Easy*.txt"`

提示：要生成 HTML，请把 `--output` 指定为以 `.html` 结尾的文件名，且不要加 `--pdf`。

### 常用示例
- **自定义难度（挖空比例）**
```bash
python cli.py --size 9 --custom-difficulty 0.7 --count 2
```
- **可复现的生成**
```bash
python cli.py --seed 12345 --count 4
```
- **混合尺寸/难度**
```bash
python cli.py --mixed --count 9 --per-page 3 --seed 54321
```
- **自定义样式与颜色**
```bash
python cli.py \
  --cell-size 35 --font-size 18 \
  --grid-color "#0066cc" --text-color "#003366" \
  --background-color "#f0f0f0" --print-info \
  --count 6 --per-page 3
```
- **从文件读取谜题**
```bash
python cli.py --files Easy1.txt Easy2.txt --per-page 2
# 或者
python cli.py --file-pattern "Easy*.txt" --per-page 2
```

### 快捷脚本：生成 Very Easy 谜题
仓库提供了 `generate_very_easy.sh`，用于快速生成 4×4、6×6、9×9 三种尺寸的 Very Easy 谜题并在控制台展示：
```bash
./generate_very_easy.sh
```
如需将输出保存为 PDF/HTML，可直接使用上面的命令行方式并指定 `--output`。

### 目录结构
```
SudokuGenerator/
  ├── sudoku/                # 主包，核心代码
  │   ├── __init__.py
  │   ├── generator.py       # 生成数独
  │   ├── parser.py          # 解析文本谜题
  │   └── printer.py         # 输出 HTML/PDF
  ├── cli.py                 # 命令行入口
  ├── generate_very_easy.sh  # Very Easy 快速生成脚本
  ├── README.md
  ├── requirements.txt       # 依赖
  ├── setup.py               # 可选，安装与发布
  └── tests/                 # 单元测试
      ├── __init__.py
      ├── test_generator.py
      └── test_printer.py
```

### 开发与测试
- 运行测试
```bash
python -m pytest tests/ -v
```
- 生成器位于 `sudoku/generator.py`，解析器位于 `sudoku/parser.py`，输出相关位于 `sudoku/printer.py`。

### 依赖
- Python 3.7+
- `fpdf`（PDF 输出所需）
```bash
pip install -r requirements.txt
```

### 许可证与贡献
- 许可证：MIT（如无单独 LICENSE 文件，可按 MIT 使用）
- 欢迎提交 PR 与建议
