# 🎓 代码新手指南 - 详细中文注释

本文档为想要学习代码的新手详细解释项目中的技术代码。

## 目录

1. [Python 基础概念](#python-基础概念)
2. [本项目使用的核心技术](#本项目使用的核心技术)
3. [代码文件详解](#代码文件详解)
4. [常见问题解答](#常见问题解答)

---

## Python 基础概念

### 什么是 Python？

Python 是一种编程语言，可以用来自动化任务。在本项目中，我们用 Python 来自动下载订阅文件并检查是否有更新。

### Python 脚本执行流程

```python
#!/usr/bin/env python3        # 第一行：告诉系统用 Python 3 运行这个文件

import os                      # 导入模块（功能库）

def main():                    # 定义一个函数（就像一个程序块）
    print("Hello World")       # 执行操作

if __name__ == '__main__':     # 入口点：当直接运行这个文件时
    main()                     # 调用 main 函数
```

### 关键概念

#### 1. 模块（Module）和导入（Import）

```python
import os       # 导入 os 模块，用于操作系统操作
import json     # 导入 json 模块，用于处理 JSON 文件
```

**为什么需要导入？**
- 模块里已经有现成的功能
- 导入后就可以直接使用这些功能
- 不需要自己从零写

#### 2. 函数（Function）

```python
def get_beijing_time() -> dict:
    """这是函数的文档字符串，说明函数做什么"""
    # 函数体：执行具体的操作
    return {'YEAR': '2025', 'MONTH': '12'}
```

**函数的好处：**
- 将复杂操作分解成小块
- 可重复使用
- 易于测试和调试

#### 3. 字典（Dictionary）

```python
time_info = {
    'YEAR': '2025',      # 键：值
    'MONTH': '12',
    'DAY': '03'
}
# 访问字典中的值
print(time_info['YEAR'])  # 输出：2025
```

#### 4. 环境变量（Environment Variables）

```python
year = os.environ.get('YEAR')  # 从操作系统获取名叫 YEAR 的环境变量
# 如果不存在，返回 None（空值）
```

#### 5. 返回值（Return）

```python
def add(a, b):
    return a + b  # 返回结果

result = add(3, 5)  # result = 8
```

---

## 本项目使用的核心技术

### 1. subprocess（执行外部命令）

```python
import subprocess

# 执行 curl 命令下载文件
result = subprocess.run(
    ["curl", "-f", "-L", "-o", "output.yaml", "https://example.com/file.yaml"],
    capture_output=True,  # 捕获输出
    text=True            # 以文本形式返回
)
```

**解释：**
- `subprocess.run()` 执行一个外部命令
- `["curl", ...]` 是命令和参数的列表
- `result.returncode` 是返回码：0 表示成功，其他表示失败

### 2. 正则表达式（Regular Expression）

```python
import re

# 查找和替换文本
text = "日期：20251203"
new_text = re.sub(r'\d{8}', '20251204', text)
# 结果：日期：20251204
```

**正则表达式常用符号：**
- `\d` 匹配数字（0-9）
- `{8}` 匹配前面的内容出现 8 次
- `\d{8}` 匹配 8 个数字
- `|` 表示或（在 20251203 或 2025-12-03 中选择）

### 3. 文件操作

```python
# 读取文件
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()  # 读取全部内容

# 写入文件
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_content)  # 覆盖原文件

# 检查文件是否存在
if os.path.exists('file.txt'):
    print("文件存在")
```

### 4. JSON 处理

```python
import json

# 读取 JSON 文件
with open('config.json', 'r') as f:
    data = json.load(f)  # 解析 JSON，得到 Python 字典

# 访问 JSON 数据
subscriptions = data['subscriptions']  # 获取 subscriptions 字段
```

---

## 代码文件详解

### 1. `update_subscriptions.py` - 通用更新器

**文件目的：** 这是项目的核心文件，负责更新所有订阅

**工作流程图：**

```
开始
 ↓
读取 subscriptions.json 配置
 ↓
循环处理每个订阅
 │
 ├─ 确定 URL（固定/动态日期/脚本生成）
 ├─ 检查前置条件（v2clash 是否有新文章）
 ├─ 下载文件
 ├─ 检测变更
 ├─ 提交到 Git
 │
 ↓
返回结果（成功/失败）
 ↓
结束
```

**关键函数解析：**

#### `get_beijing_time()`

```python
def get_beijing_time() -> dict:
    """获取当前北京时间"""
    # 执行 bash 命令获取时间
    result = subprocess.run(
        ["bash", "-c", "TZ='Asia/Shanghai' date +'%Y %m %d %Y-%m-%d %H:%M:%S'"],
        capture_output=True,
        text=True
    )
    
    # 将输出分割成各个部分
    parts = result.stdout.strip().split()
    # 比如输出："2025 12 03 2025-12-03 14:30:45"
    # 分割后：['2025', '12', '03', '2025-12-03', '14:30:45']
    
    return {
        'YEAR': parts[0],    # parts[0] = '2025'
        'MONTH': parts[1],   # parts[1] = '12'
        'DAY': parts[2],     # parts[2] = '03'
        'DATE': parts[3],    # parts[3] = '2025-12-03'
        'TIME': parts[4]     # parts[4] = '14:30:45'
    }
```

**为什么这样做？**
- 需要当前日期来生成动态 URL
- 使用 bash 命令是因为 Python 的 datetime 模块容易受系统时区影响
- 使用 TZ='Asia/Shanghai' 确保获取的是北京时间

#### `expand_url()`

```python
def expand_url(template: str, time_info: dict) -> str:
    """替换 URL 模板中的日期变量"""
    return template.format(
        YEAR=time_info['YEAR'],
        MONTH=time_info['MONTH'],
        DAY=time_info['DAY']
    )
```

**示例：**

```python
template = "https://example.com/{YEAR}/{MONTH}/{YEAR}{MONTH}{DAY}.yaml"
time_info = {'YEAR': '2025', 'MONTH': '12', 'DAY': '03'}

result = expand_url(template, time_info)
# 结果：https://example.com/2025/12/20251203.yaml
```

**`format()` 方法如何工作：**
- `{YEAR}` 会被替换成 YEAR 对应的值
- 一个占位符可以出现多次
- 替换是按名称进行的

### 2. `update_readme.py` - README 日期更新

**文件目的：** 更新 README.md 中的动态日期

**支持的日期格式：**

| 格式 | 示例 | 正则表达式 |
|------|------|-----------|
| `$YEAR$MONTH$DAY` | 20251203 | `\$YEAR\$MONTH\$DAY` |
| `YYYY/MM/YYYYMMDD` | 2025/12/20251203 | `\d{4}/\d{2}/\d{8}` |
| `/YYYY/MM/YYYYMMDD` | /2025/12/20251203 | `/\d{4}/\d{2}/\d{8}` |

**正则表达式说明：**

```python
# 原始文本
text = "订阅链接：https://example.com/$YEAR$MONTH$DAY.yaml"

# 正则表达式
pattern = r'\$YEAR\$MONTH\$DAY'  # 查找 $YEAR$MONTH$DAY
replacement = '20251203'           # 替换成 20251203

# 执行替换
import re
new_text = re.sub(pattern, replacement, text)
# 结果：订阅链接：https://example.com/20251203.yaml
```

**为什么需要 `\` 转义？**
- `$` 在正则表达式中有特殊含义（行尾）
- `\$` 表示字面量 `$` 符号

### 3. `updater_utils.py` - 共享工具库

**文件目的：** 提供所有更新脚本都需要的通用函数

**模块导入示例：**

```python
# 在其他脚本中使用
sys.path.insert(0, os.path.dirname(__file__))
from updater_utils import get_beijing_time, fetch_url, git_add_and_check

# 现在就可以直接使用这些函数了
time_info = get_beijing_time()
success, error = fetch_url(url, output_file)
```

---

## 常见问题解答

### Q1: 什么是 `subprocess.run()`？

**A:** 用来从 Python 程序中执行外部命令（如 `curl`、`git`、`bash`）

```python
# 执行 curl 命令下载文件
result = subprocess.run(
    ["curl", "-o", "file.yaml", "https://example.com/file.yaml"],
    capture_output=True
)

# 检查是否成功
if result.returncode == 0:
    print("命令执行成功")
else:
    print("命令执行失败")
```

### Q2: 什么是环境变量？

**A:** 操作系统中存储的变量，程序可以读取和使用

```python
# 获取环境变量
year = os.environ.get('YEAR')

# 在 GitHub Actions 中，workflow 文件设置环境变量
# env:
#   YEAR: 2025
#   MONTH: 12
#   DAY: 03
```

### Q3: 什么是 Git 的"暂存区"？

**A:** Git 中的一个中间状态

```
工作目录（你修改的文件）
    ↓
暂存区（已用 git add 的文件）
    ↓
提交（git commit 保存到历史）
```

```bash
# 三个步骤
git add file.yaml       # 添加到暂存区
git commit -m "更新"    # 从暂存区提交
git push               # 推送到远程
```

### Q4: 什么是正则表达式的"捕获组"？

**A:** 用 `()` 包围的部分，可以在替换中引用

```python
# 原始文本
text = "日期：12/03"

# 正则表达式和替换
pattern = r'(\d{2})/(\d{2})'        # 两个捕获组
replacement = r'2025-\1-\2'          # \1 和 \2 指向捕获组

result = re.sub(pattern, replacement, text)
# 结果：日期：2025-12-03
```

**说明：**
- `(\d{2})` 第一个捕获组，匹配 2 个数字
- `(\d{2})` 第二个捕获组，匹配 2 个数字
- `\1` 指向第一个捕获组的内容
- `\2` 指向第二个捕获组的内容

### Q5: 如何调试 Python 代码？

**A:** 添加 `print()` 语句查看程序执行过程

```python
# 添加调试信息
time_info = get_beijing_time()
print(f"DEBUG: time_info = {time_info}")  # 查看获取的时间

url = expand_url(template, time_info)
print(f"DEBUG: url = {url}")  # 查看生成的 URL

success, error = fetch_url(url, output_file)
print(f"DEBUG: success = {success}, error = {error}")  # 查看下载结果
```

### Q6: 什么是类型提示？

**A:** 告诉其他人（和自己）函数的输入和输出类型

```python
# 没有类型提示（不清楚）
def get_time():
    pass

# 有类型提示（清楚）
def get_time() -> dict:
    """返回一个字典"""
    pass

# 函数参数的类型提示
def fetch_url(url: str, output_file: str) -> Tuple[bool, Optional[str]]:
    """
    url 是字符串
    output_file 是字符串
    返回值是 (布尔值, 可选的字符串)
    """
    pass
```

---

## 学习建议

### 对于初学者

1. **先理解概念，再看代码**
   - 理解 subprocess 是什么
   - 理解 Git 是什么
   - 理解 JSON 是什么

2. **运行代码看结果**
   ```bash
   python .github/scripts/update_subscriptions.py
   ```

3. **修改代码进行实验**
   - 改变日期看 URL 如何变化
   - 改变文件名看是否影响功能

4. **阅读代码注释**
   - 每行代码上方都有中文注释
   - 理解"为什么"比"做什么"更重要

### 进阶学习

1. 了解 GitHub Actions 工作流
2. 学习 Git 版本控制
3. 深入学习 Python 和正则表达式
4. 尝试自己编写新功能

---

## 相关资源

- [Python 官方文档](https://docs.python.org/3/)
- [正则表达式教程](https://www.regular-expressions.info/)
- [Git 基础](https://git-scm.com/book/zh/v2)
- [GitHub Actions 文档](https://docs.github.com/cn/actions)

