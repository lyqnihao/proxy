# 订阅配置指南

本目录包含统一订阅更新系统的配置文件。

## 结构说明

### subscriptions.json

定义所有需要自动更新的订阅源。每个订阅条目包含以下字段：

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `name` | string | ✅ | 订阅唯一标识符（英文，无空格） |
| `dir` | string | ✅ | 本地存储目录（相对于仓库根目录） |
| `output_file` | string | ✅ | 输出文件名（通常为 `target.yaml` 或 `output.yaml`） |
| `url_type` | string | ✅ | URL 类型：`static`、`dynamic_date` 或 `dynamic_script` |
| `url` | string | 取决于类型 | 固定URL（当 `url_type` 为 `static` 时需要） |
| `url_template` | string | 取决于类型 | URL 模板（当 `url_type` 为 `dynamic_date` 时需要，支持 `{YEAR}`、`{MONTH}`、`{DAY}` 变量） |
| `url_script` | string | 取决于类型 | 执行脚本命令（当 `url_type` 为 `dynamic_script` 时需要） |
| `requires_check` | string | ❌ | 前置检查条件（目前支持 `v2clash_blog` 用于检测是否有新发布） |
| `description` | string | ❌ | 订阅描述说明 |

## 配置示例

### 类型 1：静态 URL（最简单）

```json
{
  "name": "clashfree",
  "dir": "clashfree",
  "output_file": "output.yaml",
  "url_type": "static",
  "url": "https://raw.githubusercontent.com/free-nodes/clashfree/refs/heads/main/clash.yml",
  "description": "clashfree 订阅"
}
```

### 类型 2：动态日期 URL（带日期替换）

```json
{
  "name": "nodefree",
  "dir": "nodefree",
  "output_file": "target.yaml",
  "url_type": "dynamic_date",
  "url_template": "https://nodefree.githubrowcontent.com/{YEAR}/{MONTH}/{YEAR}{MONTH}{DAY}.yaml",
  "description": "nodefree 每日订阅"
}
```

**支持的变量：**
- `{YEAR}` - 四位年份（如 2025）
- `{MONTH}` - 两位月份（01-12）
- `{DAY}` - 两位日期（01-31）

### 类型 3：脚本生成 URL

```json
{
  "name": "v2cross",
  "dir": "v2cross",
  "output_file": "output.yaml",
  "url_type": "dynamic_script",
  "url_script": "python v2cross/update.py",
  "description": "v2cross 通过脚本生成URL"
}
```

### 类型 4：带前置检查的订阅

```json
{
  "name": "proxyqueen",
  "dir": "proxyqueen",
  "output_file": "output.yaml",
  "url_type": "dynamic_date",
  "url_template": "https://v2clash.blog/Link/{YEAR}{MONTH}{DAY}-clash.yaml",
  "requires_check": "v2clash_blog",
  "description": "proxyqueen - 仅在v2clash发布新文章时更新"
}
```

## 添加新的订阅步骤

1. **确定订阅来源**
   - 获取订阅 URL 或生成方式
   - 确定本地存储目录
   - 决定输出文件名

2. **选择合适的 URL 类型**
   - `static` - 固定 URL，每次下载相同内容
   - `dynamic_date` - URL 包含日期变量（如 `/2025/12/20251220.yaml`）
   - `dynamic_script` - 通过运行脚本生成 URL（需要在仓库中有脚本文件）

3. **在 `subscriptions.json` 中添加条目**
   ```json
   {
     "name": "your-subscription-name",
     "dir": "your-directory",
     "output_file": "your-output-file.yaml",
     "url_type": "static",
     "url": "https://example.com/subscribe.yaml",
     "description": "your description"
   }
   ```

4. **确保本地目录存在**
   ```bash
   mkdir -p your-directory
   ```

5. **提交到仓库**
   - 通用更新脚本 `update_subscriptions.py` 会自动处理目录创建和文件下载

## 工作流执行说明

主工作流 `.github/workflows/update-all.yml` 每12小时运行一次（北京时间 1:35 AM 和 1:35 PM）：

1. 检出代码
2. 更新 README.md 中的动态日期
3. 遍历 `subscriptions.json` 中的所有订阅
4. 对于每个订阅：
   - 检查前置条件（如有）
   - 生成或获取 URL
   - 下载文件
   - 检测内容变更
   - 若有变更则提交到仓库
5. 仅在出现真实错误时发送邮件通知（不会在内容无变更时发送）

## 故障排查

### 订阅更新失败

检查以下内容：
1. URL 是否有效（可手动访问测试）
2. 输出目录是否存在
3. 是否有网络连接问题或超时

### 前置检查阻止更新

如果订阅配置了 `requires_check: "v2clash_blog"`：
- 工作流会先检查 v2clash.blog 是否有今天的新文章
- 如果没有新文章，会跳过该订阅的下载

### 动态日期替换不工作

确保 URL 模板中使用了正确的变量格式：
- `{YEAR}` - 必须是花括号，如 `{YEAR}` 而不是 `$YEAR`
- `{MONTH}` 和 `{DAY}` 同理
