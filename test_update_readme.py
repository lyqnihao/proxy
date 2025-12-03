import os, re
readme='README.md'
with open(readme,'r',encoding='utf-8') as f:
    content=f.read()
# 使用环境变量或默认值
year=os.environ.get('YEAR','2025')
month=os.environ.get('MONTH','12')
day=os.environ.get('DAY','03')
date_str=f"{year}{month}{day}"
year_month=f"{year}/{month}"
print('Using date:', date_str)
replacements=[
    (r'\\$YEAR\\$MONTH\\$DAY', date_str),
    (r'\\$YEAR/\\$MONTH/\\$YEAR\\$MONTH\\$DAY', f"{year_month}/{date_str}"),
    (r'\\$YEAR/\\$MONTH/\\d{8}', f"{year_month}/{date_str}"),
    (r'/\\d{4}/\\d{2}/\\d{8}', f"/{year}/{month}/{date_str}"),
    (r'(clashgithub\\.com/wp-content/uploads/rss/)\\d{8}(\\.txt|\\.yml)', rf'\\g<1>{date_str}\\2'),
]
has_v2=os.environ.get('HAS_V2CLASH_NEW','false').lower()=='true'
if has_v2:
    rep=(r'(v2clash\\.blog/Link/)\\d{8}(-v2ray\\.txt|\\.yaml)', rf'\\g<1>{date_str}\\2')
    replacements.insert(4, rep)
    print('Including v2clash replacement')
else:
    print('Skipping v2clash replacement')

original=content
for pattern, replacement in replacements:
    content = re.sub(pattern, replacement, content)
changed = (content != original)
out = 'README.md.sim.true' if has_v2 else 'README.md.sim.false'
with open(out,'w',encoding='utf-8') as f:
    f.write(content)
print('Wrote', out, 'changed=', changed)
