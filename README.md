# SudokuGenerator

一个用于生成和打印数独谜题的Python项目。

## 特性

- ✅ **保证可解性**: 所有生成的数独谜题都经过验证，确保有唯一解
- 🎯 **多种尺寸**: 支持4x4、6x6、9x9数独
- 📊 **难度分级**: 提供easy、normal、hard三种难度
- 🧪 **全面测试**: 包含完整的单元测试，确保生成质量

## 目录结构

```
SudokuGenerator/
  ├── sudoku/                # 主包，存放核心代码
  │   ├── __init__.py
  │   ├── generator.py       # 生成数独的逻辑
  │   ├── printer.py         # 打印/展示数独的逻辑
  ├── cli.py                 # 命令行入口
  ├── README.md
  ├── requirements.txt       # 依赖（如有）
  ├── setup.py               # 可选，便于安装和分发
  └── tests/                 # 单元测试
      ├── __init__.py
      ├── test_generator.py
      └── test_printer.py
```

## 使用方法

### 生成数独

```bash
python cli.py --size 9 --difficulty normal --count 4 --per-page 2
```

更多参数说明请见 `CLI_ARGUMENTS_GUIDE.md`。

## 开发与测试

- 核心逻辑位于`sudoku/`包中，便于维护和复用。
- 单元测试位于`tests/`目录。
- 所有生成的数独都经过可解性验证，确保质量。

### 运行测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试
python -m pytest tests/test_generator.py::TestSudokuGenerator::test_puzzle_solvability -v
```

## 依赖

- Python 3.7+
- fpdf (如需PDF导出)

安装依赖：

```bash
pip install -r requirements.txt
```

## 贡献

欢迎提交PR和建议！
