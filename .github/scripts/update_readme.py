#!/usr/bin/env python3
import re
import os
import sys

def main():
    readme_path = 'README.md'
    if not os.path.exists(readme_path):
        print('README.md not found')
        sys.exit(0)

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    year = os.environ.get('YEAR') or ''
    month = os.environ.get('MONTH') or ''
    day = os.environ.get('DAY') or ''
    date_str = f"{year}{month}{day}"
    year_month = f"{year}/{month}"

    print(f"准备更新日期为：{date_str}")
    print(f"准备更新路径为：{year_month}")

    original_content = content

    # 基本替换规则
    replacements = [
        (r'\$YEAR\$MONTH\$DAY', date_str),
        (r'\$YEAR/\$MONTH/\$YEAR\$MONTH\$DAY', f"{year_month}/{date_str}"),
        (r'\$YEAR/\$MONTH/\d{8}', f"{year_month}/{date_str}"),
        (r'/\d{4}/\d{2}/\d{8}', f"/{year}/{month}/{date_str}"),
        (r'(clashgithub\.com/wp-content/uploads/rss/)\d{8}(\.txt|\.yml)', rf'\g<1>{date_str}\2'),
    ]

    has_v2 = os.environ.get('HAS_V2CLASH_NEW', 'false').lower() == 'true'
    if has_v2:
        v2_pattern = (r'(v2clash\.blog/Link/)\d{8}(-v2ray\.txt|\.yaml)', rf'\g<1>{date_str}\2')
        replacements.insert(4, v2_pattern)
        print('包含 v2clash 替换')
    else:
        print('跳过 v2clash 替换（未检测到新帖）')

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)

    if content != original_content:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('✓ 已更新 README.md')
    else:
        print('✗ 未找到需要更新的动态日期标记')

if __name__ == '__main__':
    main()
