# Very Easy 数独生成器 - 完整版

专门用于生成三种尺寸(4×4, 6×6, 9×9)的Very Easy数独文件。

## 🎯 功能特点

- ✅ **三种尺寸**: 4×4, 6×6, 9×9
- ✅ **Very Easy难度**: 适合初学者，挖空比例较低
- ✅ **多种输出格式**: 文本、HTML、PDF
- ✅ **高质量**: 确保每个谜题都有唯一解
- ✅ **快速生成**: 优化的算法，生成速度快

## 📁 文件说明

| 文件名 | 类型 | 说明 |
|--------|------|------|
| `quick_very_easy_text.py` | 文本版本 | 生成纯文本文件 |
| `quick_very_easy_html.py` | HTML版本 | 生成HTML文件，可转换为PDF |
| `generate_very_easy_pdf.py` | 完整版本 | 功能最全，支持多种参数 |

## 🚀 快速开始

### 1. 文本版本 (推荐新手)

```bash
python3 quick_very_easy_text.py
```

**输出**: `very_easy_sudoku.txt`
- 纯文本格式
- 包含谜题和解答
- 适合在任何环境下使用

### 2. HTML版本 (推荐)

```bash
python3 quick_very_easy_html.py
```

**输出**: `very_easy_sudoku.html`
- 美观的HTML格式
- 可以在浏览器中查看
- 可以打印为PDF

**转换为PDF步骤**:
1. 在浏览器中打开 `very_easy_sudoku.html`
2. 按 `Ctrl+P` (或 `Cmd+P`)
3. 选择"保存为PDF"
4. 点击保存

### 3. 完整版本 (高级用户)

```bash
# 基本用法
python3 generate_very_easy_pdf.py --count 2 --per-page 1

# 生成更多谜题
python3 generate_very_easy_pdf.py --count 3 --per-page 2

# 不包含解答
python3 generate_very_easy_pdf.py --count 2 --per-page 1 --no-solutions

# 指定输出文件名
python3 generate_very_easy_pdf.py --count 2 --per-page 1 --output my_puzzles.pdf
```

## 📊 难度说明

Very Easy难度的挖空比例：

| 尺寸 | 挖空比例 | 填充数字 | 空位数量 |
|------|----------|----------|----------|
| 4×4 | 25% | 12个数字 | 4个空位 |
| 6×6 | 30% | 25个数字 | 11个空位 |
| 9×9 | 35% | 52个数字 | 29个空位 |

## 📋 输出示例

### 文本版本输出

```
Very Easy Sudoku Puzzles
==================================================

Puzzle 1 (4×4 very_easy)
==============================

PUZZLE:
| 1  2 | 3  4 |
| 3  . | .  . |
--------------
| 2  . | 4  3 |
| 4  3 | 2  1 |
--------------

SOLUTION:
| 1  2 | 3  4 |
| 3  4 | 1  2 |
--------------
| 2  1 | 4  3 |
| 4  3 | 2  1 |
--------------
```

### HTML版本特点

- 🎨 美观的界面设计
- 📱 响应式布局
- 🖨️ 打印友好
- 📄 自动分页
- 🎯 清晰的网格线

## 🔧 参数说明

### `generate_very_easy_pdf.py` 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--count` | int | 2 | 每种尺寸生成的谜题数量 |
| `--per-page` | int | 1 | 每页谜题数量 (1-4) |
| `--output` | str | very_easy_sudoku.pdf | 输出文件名 |
| `--no-solutions` | flag | False | 不包含解答 |
| `--seed` | int | None | 随机种子 |
| `--verbose` | flag | False | 显示详细输出 |

## 📈 性能统计

### 生成速度

- **4×4**: ~0.1秒/谜题
- **6×6**: ~0.3秒/谜题  
- **9×9**: ~0.8秒/谜题

### 文件大小

- **文本文件**: ~3.5KB (6个谜题)
- **HTML文件**: ~40KB (6个谜题)
- **PDF文件**: ~200KB (6个谜题)

## 🛠️ 故障排除

### 常见问题

1. **Python命令不存在**
   ```bash
   # 使用python3
   python3 quick_very_easy_text.py
   ```

2. **模块导入错误**
   ```bash
   # 检查是否在正确的目录
   ls sudoku/
   ```

3. **文件权限错误**
   ```bash
   # 添加执行权限
   chmod +x *.py
   ```

4. **生成失败**
   ```bash
   # 尝试不同的种子
   python3 quick_very_easy_text.py
   # 脚本会自动重试
   ```

### 错误信息

- `Failed to generate a complete valid sudoku grid`: 生成完整解失败，会自动重试
- `Generated puzzle has X solutions, expected 1`: 谜题有多个解，会自动重试
- `No module named 'fpdf'`: 缺少PDF依赖，使用文本或HTML版本

## 🎯 使用建议

### 新手用户
1. 使用 `quick_very_easy_text.py`
2. 生成文本文件
3. 打印或保存文本文件

### 普通用户
1. 使用 `quick_very_easy_html.py`
2. 在浏览器中打开HTML文件
3. 打印为PDF或直接打印

### 高级用户
1. 使用 `generate_very_easy_pdf.py`
2. 自定义参数
3. 批量生成

## 📝 技术细节

### 生成算法

1. **完整解生成**: 使用回溯算法生成完整的合法数独解
2. **智能挖空**: 根据Very Easy难度设置挖空比例
3. **唯一解验证**: 确保挖空后的谜题有且仅有一个解
4. **质量保证**: 每个谜题都经过严格验证

### 改进特性

- ✅ 先生成合法完整解
- ✅ 再挖空的方法随机生成数独
- ✅ 不同的难度代表不同的挖空比例
- ✅ 挖空之后检测是否确保解唯一
- ✅ 新增 very_easy 和 very_hard 难度
- ✅ 改进的挖空算法，更高效且更可靠
- ✅ 增强的唯一解检测机制

## 📄 许可证

本项目遵循MIT许可证。

## 🤝 贡献

欢迎提交问题和建议！