# Very Easy 数独生成器

专门用于生成三种尺寸(4×4, 6×6, 9×9)的Very Easy数独PDF文件。

## 功能特点

- ✅ **三种尺寸**: 4×4, 6×6, 9×9
- ✅ **Very Easy难度**: 适合初学者，挖空比例较低
- ✅ **PDF输出**: 包含谜题和解答
- ✅ **高质量**: 确保每个谜题都有唯一解
- ✅ **快速生成**: 优化的算法，生成速度快

## 使用方法

### 1. 快速生成 (推荐)

使用简化脚本快速生成：

```bash
python quick_very_easy.py
```

这将生成：
- 每种尺寸2个谜题
- 每页1个谜题
- 包含解答
- 输出文件：`very_easy_sudoku.pdf`

### 2. 自定义生成

使用完整功能的脚本：

```bash
# 基本用法
python generate_very_easy_pdf.py --count 2 --per-page 1

# 生成更多谜题
python generate_very_easy_pdf.py --count 3 --per-page 2

# 不包含解答
python generate_very_easy_pdf.py --count 2 --per-page 1 --no-solutions

# 指定输出文件名
python generate_very_easy_pdf.py --count 2 --per-page 1 --output my_puzzles.pdf

# 使用固定种子确保可重现
python generate_very_easy_pdf.py --count 2 --per-page 1 --seed 42
```

## 参数说明

### `generate_very_easy_pdf.py` 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--count` | int | 2 | 每种尺寸生成的谜题数量 |
| `--per-page` | int | 1 | 每页谜题数量 (1-4) |
| `--output` | str | very_easy_sudoku.pdf | 输出PDF文件名 |
| `--no-solutions` | flag | False | 不包含解答页面 |
| `--seed` | int | None | 随机种子，用于可重现结果 |
| `--verbose` | flag | False | 显示详细输出 |

## 难度说明

Very Easy难度的挖空比例：

| 尺寸 | 挖空比例 | 填充数字 |
|------|----------|----------|
| 4×4 | 25% | 12个数字 |
| 6×6 | 30% | 25个数字 |
| 9×9 | 35% | 52个数字 |

## 输出格式

### PDF布局

- **每页1个谜题**: 谜题和解答并排显示
- **每页2个谜题**: 两个谜题上下排列
- **每页3-4个谜题**: 紧凑布局，适合打印

### 文件结构

```
very_easy_sudoku.pdf
├── 标题页
├── 4×4 谜题 1 + 解答
├── 4×4 谜题 2 + 解答
├── 6×6 谜题 1 + 解答
├── 6×6 谜题 2 + 解答
├── 9×9 谜题 1 + 解答
└── 9×9 谜题 2 + 解答
```

## 示例输出

### 命令行输出示例

```
============================================================
Very Easy 数独生成器
============================================================
尺寸: 4×4, 6×6, 9×9
难度: Very Easy
每种尺寸谜题数量: 2
每页谜题数量: 1
输出文件: very_easy_sudoku.pdf
包含解答: 是
============================================================

生成 2 个每种尺寸的 Very Easy 数独谜题...

生成 4×4 Very Easy 数独:
  谜题 1/2... ✓
  谜题 2/2... ✓

生成 6×6 Very Easy 数独:
  谜题 1/2... ✓
  谜题 2/2... ✓

生成 9×9 Very Easy 数独:
  谜题 1/2... ✓
  谜题 2/2... ✓

创建PDF文件: very_easy_sudoku.pdf
每页谜题数量: 1
包含解答: 是
✓ PDF文件已生成: very_easy_sudoku.pdf

统计信息:
  4×4: 2 个谜题
  6×6: 2 个谜题
  9×9: 2 个谜题

============================================================
生成完成！
============================================================
总谜题数量: 6
PDF文件: very_easy_sudoku.pdf
```

## 故障排除

### 常见问题

1. **生成失败**
   ```bash
   # 尝试使用不同的种子
   python generate_very_easy_pdf.py --seed 123
   ```

2. **PDF生成错误**
   ```bash
   # 检查是否安装了fpdf
   pip install fpdf
   ```

3. **内存不足**
   ```bash
   # 减少谜题数量
   python generate_very_easy_pdf.py --count 1
   ```

### 错误信息

- `Failed to generate a complete valid sudoku grid`: 生成完整解失败，尝试重试
- `Generated puzzle has X solutions, expected 1`: 谜题有多个解，会自动重试
- `PDF generation failed`: PDF生成失败，检查文件权限和磁盘空间

## 技术细节

### 生成算法

1. **完整解生成**: 使用回溯算法生成完整的合法数独解
2. **智能挖空**: 根据Very Easy难度设置挖空比例
3. **唯一解验证**: 确保挖空后的谜题有且仅有一个解
4. **质量保证**: 每个谜题都经过严格验证

### 性能优化

- 优化的回溯算法
- 智能的挖空策略
- 高效的解计数算法
- 内存友好的PDF生成

## 许可证

本项目遵循MIT许可证。