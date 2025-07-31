#!/bin/bash

# Very Easy 数独生成器 Shell 脚本
# 生成三种尺寸(4x4, 6x6, 9x9)的Very Easy数独

echo "生成Very Easy数独..."

# 生成4x4 Very Easy数独
echo "生成4x4 Very Easy数独..."
python3 cli.py --size 4 --difficulty very_easy --count 2 --console

# 生成6x6 Very Easy数独
echo "生成6x6 Very Easy数独..."
python3 cli.py --size 6 --difficulty very_easy --count 2 --console

# 生成9x9 Very Easy数独
echo "生成9x9 Very Easy数独..."
python3 cli.py --size 9 --difficulty very_easy --count 2 --console

echo "完成！生成了三种尺寸的Very Easy数独"