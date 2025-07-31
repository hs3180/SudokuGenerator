# 数独生成器详细指南

## 概述

这个数独生成器实现了"先生成完整解，再挖空"的方法，确保生成的数独谜题有且仅有一个解。支持多种网格大小（4×4、6×6、9×9）和不同难度级别。

## 核心算法

### 1. 先生成完整解

数独生成器首先创建一个完整的、有效的数独解：

```python
def generate_complete_grid(self) -> List[List[int]]:
    """生成一个完整的有效数独网格"""
    grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
    
    # 对于9x9数独，预填充对角box然后回溯
    if self.size == 9:
        for i in range(0, self.size, max(self.box_height, self.box_width)):
            self.fill_box(grid, i, i)
    
    if not self.solve(grid):
        raise RuntimeError("Failed to generate a complete valid sudoku grid")
    return grid
```

**算法步骤：**
1. 创建空的数独网格
2. 对于9×9数独，预填充对角线的3×3方块（这些方块互不冲突）
3. 使用回溯算法填充剩余的空格
4. 验证生成的网格是有效的数独解

### 2. 再随机挖空

从完整解中随机移除数字，创建谜题：

```python
def remove_numbers(self, grid: List[List[int]], difficulty: str) -> List[List[int]]:
    """从完整网格中移除数字以创建谜题"""
    puzzle = deepcopy(grid)
    cells_to_remove = int(self.size * self.size * self.difficulty_settings[self.size][difficulty])
    
    attempts = 0
    removed = 0
    max_attempts = cells_to_remove * self.max_attempts_multiplier
    
    while removed < cells_to_remove and attempts < max_attempts:
        row = random.randint(0, self.size - 1)
        col = random.randint(0, self.size - 1)
        
        if puzzle[row][col] != 0:
            backup = puzzle[row][col]
            puzzle[row][col] = 0
            
            # 检查是否仍然可解且有唯一解
            test_puzzle = deepcopy(puzzle)
            if self.solve(test_puzzle):
                if not self.require_unique_solution or self.count_solutions(puzzle, 2) == 1:
                    removed += 1
                else:
                    puzzle[row][col] = backup
            else:
                puzzle[row][col] = backup
        
        attempts += 1
    
    return puzzle
```

**挖空策略：**
1. 根据难度设置计算需要移除的格子数量
2. 随机选择位置进行挖空
3. 每次挖空前检查：
   - 谜题是否仍然可解
   - 是否仍然有唯一解
4. 如果挖空后不满足条件，则恢复该位置的数字

### 3. 不同难度代表不同挖空比例

```python
self.difficulty_settings = {
    4: {'easy': 0.3, 'normal': 0.4, 'hard': 0.5},      # 4×4数独
    6: {'easy': 0.35, 'normal': 0.45, 'hard': 0.55},   # 6×6数独
    9: {'easy': 0.4, 'normal': 0.5, 'hard': 0.6}       # 9×9数独
}
```

**挖空比例说明：**
- **Easy（简单）**：移除30-40%的数字，保留较多提示
- **Normal（中等）**：移除40-50%的数字，平衡难度
- **Hard（困难）**：移除50-60%的数字，需要更多推理

### 4. 检测确保解唯一

使用回溯算法计算解的数量：

```python
def count_solutions(self, grid: List[List[int]], limit: int = 2) -> int:
    """计算解的数量（限制上限以提高效率）"""
    def solve_count(g, count):
        if count[0] >= limit:
            return
            
        for row in range(self.size):
            for col in range(self.size):
                if g[row][col] == 0:
                    for num in range(1, self.size + 1):
                        if self.is_valid(g, row, col, num):
                            g[row][col] = num
                            solve_count(g, count)
                            g[row][col] = 0
                    return
        count[0] += 1
    
    test_grid = deepcopy(grid)
    count = [0]
    solve_count(test_grid, count)
    return count[0]
```

**唯一性检测：**
1. 使用回溯算法尝试所有可能的填充方式
2. 限制搜索深度以提高效率（通常只检查前2-3个解）
3. 如果找到多个解，则拒绝该挖空操作

## 算法优势

### 1. 保证解的存在性
- 从完整解开始，确保谜题一定有解
- 避免了生成无解谜题的问题

### 2. 保证解的唯一性
- 每次挖空后都验证解的唯一性
- 确保生成的谜题有且仅有一个解

### 3. 可控的难度
- 通过挖空比例精确控制难度
- 不同大小的数独有不同的难度设置

### 4. 高效的生成
- 预填充策略减少回溯搜索空间
- 限制解的数量检查提高效率

## 使用示例

### 基本使用

```python
from sudoku.generator import SudokuGenerator

# 创建9×9数独生成器
generator = SudokuGenerator(9)

# 生成normal难度的谜题
puzzle, solution = generator.generate_puzzle('normal')

# 验证解的唯一性
solution_count = generator.count_solutions(puzzle, 3)
print(f"解的数量: {solution_count}")  # 应该输出: 1
```

### 不同大小和难度

```python
# 4×4数独，简单难度
generator_4x4 = SudokuGenerator(4)
puzzle_4x4, solution_4x4 = generator_4x4.generate_puzzle('easy')

# 6×6数独，困难难度
generator_6x6 = SudokuGenerator(6)
puzzle_6x6, solution_6x6 = generator_6x6.generate_puzzle('hard')

# 9×9数独，中等难度
generator_9x9 = SudokuGenerator(9)
puzzle_9x9, solution_9x9 = generator_9x9.generate_puzzle('normal')
```

### 自定义难度

```python
generator = SudokuGenerator(9)

# 自定义挖空比例（70%）
generator.difficulty_settings[9]['custom'] = 0.7
puzzle, solution = generator.generate_puzzle('custom')

# 或者临时修改
generator.difficulty_settings[9]['normal'] = 0.6  # 增加normal难度
puzzle, solution = generator.generate_puzzle('normal')
```

## 算法复杂度

### 时间复杂度
- **生成完整解**：O(9^81) 最坏情况，但通过预填充策略大幅优化
- **挖空过程**：O(k × n² × s)，其中k是挖空数量，n是网格大小，s是解的数量检查
- **唯一性检测**：O(9^m)，其中m是空格数量，但通常限制检查深度

### 空间复杂度
- **网格存储**：O(n²)
- **回溯栈**：O(n²)

## 质量保证

### 1. 有效性验证
- 每行、每列、每个方块中的数字都不重复
- 所有数字都在有效范围内（1到网格大小）

### 2. 可解性验证
- 使用回溯算法验证谜题可解
- 确保从完整解挖空后的谜题仍然有解

### 3. 唯一性验证
- 计算解的数量，确保只有一个解
- 拒绝会导致多个解的挖空操作

### 4. 测试覆盖
- 单元测试覆盖所有核心功能
- 验证不同大小和难度的数独生成
- 测试边界情况和错误处理

## 总结

这个数独生成器通过"先生成完整解，再挖空"的方法，确保了：

1. ✅ **解的存在性**：从完整解开始，保证谜题有解
2. ✅ **解的唯一性**：每次挖空后验证唯一性
3. ✅ **难度可控**：通过挖空比例精确控制难度
4. ✅ **高效生成**：使用预填充和限制搜索等优化策略
5. ✅ **质量保证**：全面的验证和测试机制

这种方法比直接生成谜题的方法更可靠，能够保证生成高质量的数独谜题。