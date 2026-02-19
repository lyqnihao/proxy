#!/usr/bin/env python3
"""
README 动态日期更新器

功能：
1. 读取 README.md 文件
2. 查找其中的日期占位符（如 $YEAR$MONTH$DAY）
3. 根据当前日期替换这些占位符
4. 支持多种日期格式（YYYYMMDD、YYYY/MM/DD 等）
5. 智能检查 v2clash.blog 是否有新文章（如果需要）
"""
import re       # 正则表达式库（用于查找和替换日期模式）
import os       # 操作系统接口
import sys      # 系统特定参数和函数

def main():
    """主函数 - 执行 README 日期更新"""
    # README 文件路径
    readme_path = 'README.md'
    # 检查 README.md 是否存在
    if not os.path.exists(readme_path):
        print('README.md 文件未找到')
        sys.exit(0)  # 不存在也不算错误，直接退出

    # 以 UTF-8 编码读取 README 文件内容
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 从环境变量读取年月日信息
    year = os.environ.get('YEAR') or ''      # 年份（4位，如 2025）
    month = os.environ.get('MONTH') or ''    # 月份（2位，如 12）
    day = os.environ.get('DAY') or ''        # 日期（2位，如 03）
    
    # 生成几种常用的日期格式
    date_str = f"{year}{month}{day}"        # YYYYMMDD 格式：20251203
    year_month = f"{year}/{month}"           # YYYY/MM 格式：2025/12

    # 打印日期信息（用于调试）
    print(f"准备更新日期为：{date_str}")
    print(f"准备更新路径为：{year_month}")

    # 保存原始内容（用于对比是否有变更）
    original_content = content

    # 定义需要替换的日期模式列表
    # 每个元组是 (正则表达式模式, 替换文本)
    replacements = [
        # 基础占位符替换
        (r'\$YEAR\$MONTH\$DAY', date_str),              # $YEAR$MONTH$DAY -> YYYYMMDD
        (r'\$YEAR/\$MONTH', year_month),                # $YEAR/$MONTH -> YYYY/MM

        # 各种网站的具体替换规则
        # clashgithub.com 的日期格式（新格式）
        (r'(clashgithub\.com/wp-content/uploads/rss/)(clash)?(\d{8})(\.\w+)', rf'\g<1>{date_str}\4'),
        # 旧的 GitHub raw 地址（保留用于向后兼容，但不再使用）
        (r'(raw\.githubusercontent\.com/free-nodes/clashfree/refs/heads/main/clash)(\d{8})(\.yml)', rf'\g<1>{date_str}\g<3>'),

        # nodefree 的日期格式（通用方法，支持各种前缀）
        (r'(node\.nodefree\.me/)\d{4}/\d{2}/([a-zA-Z]*)\d{8}(\.txt|\.yaml)', rf'\g<1>{year_month}/\g<2>{date_str}\g<3>'),
    ]
    
    # 检查是否需要包含 v2clash 的替换
    # HAS_V2CLASH_NEW 是一个环境变量，如果 v2clash.blog 有新文章就设为 true
    has_v2 = os.environ.get('HAS_V2CLASH_NEW', 'false').lower() == 'true'
    if has_v2:
        print('包含 v2clash 多种格式替换')
        # 添加 v2clash.blog 的日期格式替换规则
        v2clash_replacements = [
            (r'(v2clash\.blog/Link/)\d{8}(-v2ray\.txt|-clash\.yaml)', rf'\g<1>{date_str}\2'),
            (r'(v2clash\.blog/clash/)\d{8}\.yaml', rf'\g<1>{date_str}.yaml'),
            (r'(v2clash\.blog/v2ray/)\d{8}\.txt', rf'\g<1>{date_str}.txt'),
            (r'(v2clash\.blog/rss/)\d{8}(-v2ray)?\.txt', rf'\g<1>{date_str}\2.txt'),
        ]
        replacements.extend(v2clash_replacements)
    else:
        # v2clash 无新文章，不更新 v2clash 相关的 URL
        print('跳过 v2clash 替换（未检测到新帖）')



    # 应用所有替换规则
    # 对每个规则，使用 re.sub() 进行正则替换
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)

    # 检查内容是否有变更
    if content != original_content:
        # 有变更，保存更新后的文件
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('✓ 已更新 README.md')
    else:
        # 无变更，说明没有找到需要更新的日期标记
        print('✗ 未找到需要更新的动态日期标记')

# 添加一个特殊函数，只更新特定区域的日期
def update_specific_area_only():
    """
    只更新特定区域的日期，避免修改其他内容
    """
    readme_path = 'README.md'
    if not os.path.exists(readme_path):
        print('README.md 文件未找到')
        sys.exit(0)
    print(f"DEBUG: update_specific_area_only called with YEAR={os.environ.get('YEAR')}, MONTH={os.environ.get('MONTH')}, DAY={os.environ.get('DAY')}")

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    year = os.environ.get('YEAR') or ''
    month = os.environ.get('MONTH') or ''
    day = os.environ.get('DAY') or ''
    
    date_str = f"{year}{month}{day}"
    year_month = f"{year}/{month}"
    
    # 检查是否需要包含 v2clash 的替换
    has_v2 = os.environ.get('HAS_V2CLASH_NEW', 'false').lower() == 'true'
    if has_v2:
        print('包含 v2clash 多种格式替换')
    else:
        print('跳过 v2clash 替换（未检测到新帖）')

    # 只更新包含特定关键词的行，避免修改其他内容
    lines = content.split('\n')
    updated_lines = []
    updated = False
    
    for line in lines:
        # 只更新包含特定关键词的行
        if any(keyword in line for keyword in ['nodefree', 'clashfree', 'clashgithub', 'xconfig', 'xConfig', 'v2clash']):
            # 应用日期替换
            original_line = line
            # 替换 $YEAR$MONTH$DAY 格式
            line = re.sub(r'\$YEAR\$MONTH\$DAY', date_str, line)
            # 替换 $YEAR/$MONTH/XXXXXXXX 格式
            line = re.sub(r'\$YEAR/\$MONTH/\d{8}', f"{year_month}/{date_str}", line)
            # 替换 /YYYY/MM/XXXXXXXX 格式
            line = re.sub(r'/\d{4}/\d{2}/\d{8}', f"/{year}/{month}/{date_str}", line)
            # 替换 clashgithub.com 的日期格式（新格式：YYYYMMDD.yml，无clash前缀）
            line = re.sub(
                r'(clashgithub\.com/wp-content/uploads/rss/)(clash)?(\d{8})(\.\w+)',
                rf'\g<1>{date_str}\4',
                line
            )
            # 替换 raw.githubusercontent.com/clashfree 的日期格式
            line = re.sub(
                r'(raw\.githubusercontent\.com/free-nodes/clashfree/refs/heads/main/clash)(\d{8})(\.yml)', 
                rf'\g<1>{date_str}\g<3>', 
                line
            )
            # 替换 v2clash.blog 的多种日期格式（仅在检测到新文章时更新）
            if has_v2:
                line = re.sub(
                    r'(v2clash\.blog/Link/)\d{8}(-v2ray\.txt|-clash\.yaml)', 
                    rf'\g<1>{date_str}\2', 
                    line
                )
                line = re.sub(
                    r'(v2clash\.blog/clash/)\d{8}\.yaml', 
                    rf'\g<1>{date_str}.yaml', 
                    line
                )
                line = re.sub(
                    r'(v2clash\.blog/v2ray/)\d{8}\.txt', 
                    rf'\g<1>{date_str}.txt', 
                    line
                )
                line = re.sub(
                    r'(v2clash\.blog/rss/)\d{8}(-v2ray)?\.txt', 
                    rf'\g<1>{date_str}\2.txt', 
                    line
                )
            else:
                # v2clash 无新文章，跳过更新 v2clash 相关的 URL
                pass
            # 添加 nodefree 的日期格式替换，包括 Mihomo 订阅链接
            line = re.sub(
                r'(node\.nodefree\.me/)\d{4}/\d{2}/(m?)\d{8}(\.txt|\.yaml)', 
                rf'\g<1>{year}/{month}/\g<2>{date_str}\g<3>', 
                line
            )
            
            if line != original_line:
                updated = True
                
        updated_lines.append(line)
    
    # 如果有更新，则写入文件
    if updated:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(updated_lines))
        print('✓ 已更新 README.md 中的特定区域')
    else:
        print('✗ 未找到需要更新的特定区域')

if __name__ == '__main__':
    # 检查是否设置了 SPECIAL_UPDATE_MODE 环境变量
    if os.environ.get('SPECIAL_UPDATE_MODE') == 'specific_area':
        update_specific_area_only()
    else:
        main()