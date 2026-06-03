# AI Usage Guide - Subscription Auto-Update System

## Quick Overview
This is a GitHub Actions based subscription auto-update system for proxy nodes.

## Key Files
- `.github/config/subscriptions.json` - Subscription configuration
- `.github/scripts/update_subscriptions.py` - Core update script
- `.github/workflows/update-all.yml` - Main workflow

## Subscription Configuration Format
```json
{
  "name": "subscription_name",
  "dir": "directory_name",
  "output_file": "output.yaml",
  "url_type": "static|dynamic_date|dynamic_script|git_sync",
  "url": "https://...",
  "url_template": "https://.../{YEAR}/{MONTH}/{YEAR}{MONTH}{DAY}.yaml",
  "url_script": "python script.py",
  "requires_check": "check_function_name",
  "description": "Description"
}
```

## URL Types
1. **static**: Fixed URL, no date variables
2. **dynamic_date**: URL with `{YEAR}`, `{MONTH}`, `{DAY}` variables
3. **dynamic_script**: Execute script to get URL
4. **git_sync**: Clone git repository

## Pre-check Functions
Available check functions (for `requires_check`):
- `v2clash_blog` - Check v2clash.blog new post
- `nodefree_blog` - Check nodefree.me new post
- `clashfree` - Check clashfree new post
- `clash_meta_blog` - Check clash-meta.github.io new post
- `nodev2ray_blog` - Check nodev2ray.com new post
- `oneclash_blog` - Check oneclash.cc new post
- `v2rayhare_blog` - Check v2rayshare.net new post

## Commit Message Format
```
{name}_{datetime} - Update from {url} (at {tracking_url})
```

## Log Output Format
```
[{name}] 尝试地址: `{url}`
[{name}] ✓ 地址成功: `{url}` ({size} bytes)
[{name}] 已更新: `{url}`
[{name}] 无变更
[{name}] 跳过: {reason}
[{name}] 错误: {error}
```

## Execution Flow
1. Check blog updates (if requires_check)
2. Generate URL (replace date variables if needed)
3. Download to temp file
4. Detect encoding & convert to UTF-8
5. Compare with existing file
6. Replace if changed
7. Git commit if changed

## Environment Variables
- `YEAR`, `MONTH`, `DAY` - Current Beijing time
- `CI` - GitHub Actions environment flag

## Workflow Schedule
- Cron: `05 16,4 * * *` (UTC)
- Beijing time: 00:05 & 12:05 daily

## Python Dependencies
- requests>=2.32.0
- beautifulsoup4==4.12.2
- chardet>=5.2.0

## How to Add New Subscription
1. Add entry to `subscriptions.json`
2. Create directory: `mkdir -p {dir}`
3. Add commit step in `update-all.yml`
4. Update push conditions

## Error Handling
- Single subscription failure doesn't block others
- Email notification only on actual errors
- `continue-on-error: true` for all steps

## Key Features
- Automatic encoding detection & conversion (UTF-8)
- Pre-check before downloading
- Config-driven architecture
- Idempotent updates (no changes = no commit)
- Comprehensive logging
