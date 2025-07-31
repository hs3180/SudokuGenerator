#!/bin/bash

# Very Easy 数独生成器 Shell 脚本
# 生成三种尺寸(4x4, 6x6, 9x9)的Very Easy数独

echo "生成Very Easy数独..."

# 生成4x4 Very Easy数独
echo "生成4x4 Very Easy数独..."
python3 -c "
import random
from sudoku.generator import SudokuGenerator
random.seed(42)
generator = SudokuGenerator(4)
puzzle, solution = generator.generate_puzzle('very_easy')
print('4x4 Very Easy数独生成完成')
"

# 生成6x6 Very Easy数独
echo "生成6x6 Very Easy数独..."
python3 -c "
import random
from sudoku.generator import SudokuGenerator
random.seed(42)
generator = SudokuGenerator(6)
puzzle, solution = generator.generate_puzzle('very_easy')
print('6x6 Very Easy数独生成完成')
"

# 生成9x9 Very Easy数独
echo "生成9x9 Very Easy数独..."
python3 -c "
import random
from sudoku.generator import SudokuGenerator
random.seed(42)
generator = SudokuGenerator(9)
puzzle, solution = generator.generate_puzzle('very_easy')
print('9x9 Very Easy数独生成完成')
"

echo "完成！生成了三种尺寸的Very Easy数独"