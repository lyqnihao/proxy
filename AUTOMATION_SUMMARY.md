# 订阅自动更新系统 - 项目完成总结

## 项目概述

完成了将 7 个独立的订阅更新工作流合并为一个统一、可扩展的系统。

### 关键成就

✅ **工作流整合**：7 个独立工作流 → 1 个主工作流 + 6 个配置条目
✅ **智能调度**：每 12 小时自动更新（北京时间 1:35 AM 和 1:35 PM）
✅ **配置驱动**：基于 JSON 配置，添加新订阅无需修改代码
✅ **灵活的 URL 类型**：支持静态 URL、动态日期模板、脚本生成
✅ **v2clash 感知**：仅当有新发布时更新相关订阅
✅ **智能通知**：仅在出现真实错误时发送邮件

---

## 架构说明

### 核心文件

```
.github/
├── config/
│   ├── subscriptions.json          # 订阅配置注册表
│   └── README.md                   # 配置文档
├── scripts/
│   ├── update_subscriptions.py     # 通用更新器（核心）
│   ├── update_readme.py            # README 日期更新
│   ├── updater_utils.py            # 共享工具函数
│   ├── update_proxyqueen.py        # 旧脚本（保留兼容）
│   └── update_nodefree.py          # 旧脚本（保留兼容）
└── workflows/
    ├── update-all.yml              # 主工作流（新）
    ├── update-*.yml                # 个别工作流（转为手动）
    └── ...
```

### 执行流程

1. **主工作流每 12 小时触发一次**（北京时间 1:35 & 13:35）
   ```
   cron: '35 17,5 * * *'  # UTC 时间
   = 北京时间 2025-01-01 01:35 & 13:35
   ```

2. **步骤序列**
   - ① 检出代码
   - ② 计算北京时间（YEAR, MONTH, DAY）
   - ③ 检查 v2clash.blog 有无新文章
   - ④ 更新 README.md 动态日期
   - ⑤ 调用 `update_subscriptions.py` 处理所有订阅
   - ⑥ 检测变更并提交
   - ⑦ 仅在失败时发送邮件通知

3. **订阅更新流程**（通用脚本）
   ```
   加载 subscriptions.json
   └─→ 遍历每个订阅
       ├─→ 检查前置条件（如 v2clash 检查）
       ├─→ 生成或获取 URL
       │   ├─ static: 直接使用
       │   ├─ dynamic_date: 替换日期变量
       │   └─ dynamic_script: 执行脚本
       ├─→ 下载文件
       ├─→ 检测内容变更
       └─→ 若有变更则 git 提交
   ```

---

## 配置详情

### 订阅配置（subscriptions.json）

目前支持 **6 个订阅源**：

| 名称 | 类型 | 来源 | 检查条件 |
|------|------|------|---------|
| cmliu | static | CF Workers 汇聚 | 无 |
| nodefree | dynamic_date | nodefree 每日 | 无 |
| clashfree | static | free-nodes | 无 |
| proxyqueen | dynamic_date | v2clash.blog | v2clash_blog |
| v2cross | dynamic_script | Python 脚本 | 无 |
| xconfig | static | xray-proxy | 无 |

### URL 类型说明

#### Type 1: Static（静态）
```json
{
  "name": "clashfree",
  "url_type": "static",
  "url": "https://raw.githubusercontent.com/..."
}
```
→ 每次下载相同的固定 URL

#### Type 2: Dynamic Date（动态日期）
```json
{
  "name": "nodefree",
  "url_type": "dynamic_date",
  "url_template": "https://raw.../2025/12/20251220.yaml"
  // {YEAR}, {MONTH}, {DAY} 会被替换
}
```
→ URL 包含日期，自动按当前时间替换

#### Type 3: Dynamic Script（脚本生成）
```json
{
  "name": "v2cross",
  "url_type": "dynamic_script",
  "url_script": "python v2cross/update.py"
}
```
→ 执行脚本获取 URL（脚本输出作为 URL）

#### Type 4: 前置检查
```json
{
  "name": "proxyqueen",
  "requires_check": "v2clash_blog",
  // ...
}
```
→ 仅当 v2clash.blog 有新发布时才下载

---

## 关键改进

### 1. 统一调度
**之前**：7 个不同的 cron 时间表
- cmliu: 每天 4:05 UTC
- nodefree: 每2天 4:05 UTC
- clashfree: 每8小时 17:35 UTC
- proxyqueen: 每天 1:35 UTC
- v2cross: 每6小时 1:05 UTC
- xconfig: 每天 4:05 UTC
- readme: 每天 0:00 UTC

**现在**：统一每12小时，北京时间 1:35 & 13:35
```yaml
cron: '35 17,5 * * *'  # 推理：
# UTC 17:35 = 北京时间次日 01:35
# UTC 05:35 = 北京时间当日 13:35
```

### 2. 错误处理
**之前**：邮件在任何情况下都发送
**现在**：智能过滤
- ✅ 发送：真实错误（下载失败、脚本错误）
- ❌ 不发送：内容无变更

### 3. 可扩展性
**之前**：每添加订阅需要新建工作流文件
**现在**：只需修改 `subscriptions.json`
```json
{
  "name": "new-subscription",
  "dir": "new-sub",
  "output_file": "output.yaml",
  "url_type": "static",
  "url": "https://..."
}
```

---

## 使用说明

### 添加新的订阅

1. 编辑 `.github/config/subscriptions.json`
2. 添加新条目：
```json
{
  "name": "my-new-sub",
  "dir": "my-new-sub",
  "output_file": "output.yaml",
  "url_type": "static",
  "url": "https://example.com/subscribe.yaml"
}
```
3. 本地创建对应目录：`mkdir -p my-new-sub`
4. 提交更改
5. 主工作流会自动在下次运行时处理新订阅

### 手动触发

所有旧工作流已转为手动模式（`workflow_dispatch`），可在 GitHub Actions 页面手动触发。

主工作流也可手动触发：
1. 进入 GitHub 仓库 → Actions
2. 选择 "Update All Subscriptions"
3. 点击 "Run workflow"

### README 动态日期

支持的日期格式：
- `$YEAR$MONTH$DAY` → 替换为 `20251220`
- `$YEAR/$MONTH/$YEAR$MONTH$DAY` → 替换为 `2025/12/20251220`
- `/YYYY/MM/YYYYMMDD` → 替换为 `/2025/12/20251220`
- `v2clash.blog/Link/YYYYMMDD` → 替换为 `v2clash.blog/Link/20251220`（需 v2clash 有新文章）

---

## 技术细节

### 时间处理
- **主工作流**：提取北京时间 YEAR/MONTH/DAY
- **通用脚本**：优先使用环境变量，回退到系统计算
- **v2clash 检查**：在下载前检查该日期是否有新文章

### Git 操作
```bash
git add <file>
git diff --staged --quiet  # 检测变更
git commit -m "..."
git push
```

### 错误恢复
- 单个订阅失败不阻止其他订阅更新
- 所有步骤都有 `continue-on-error: true`
- 邮件仅在实际失败时发送

---

## 测试清单

□ 主工作流每12小时正常运行
□ 所有6个订阅都被正确更新
□ README.md 的日期被正确替换
□ 无内容变更时不发送邮件
□ 出现错误时邮件正确发送
□ v2clash 检查逻辑正常工作
□ 可通过手动触发运行工作流
□ 日期变量正确传递到 Python 脚本

---

## 故障排查

### 工作流不运行
- 检查 cron 表达式是否正确
- 验证 GitHub Actions 是否启用
- 查看 "Actions" 标签下的日志

### 订阅不更新
- 检查 `subscriptions.json` 中的 URL 是否有效
- 验证 `dir` 目录是否存在
- 查看工作流运行日志中的错误信息

### 日期替换不工作
- 确保 README.md 包含正确的日期模式
- 验证环境变量是否正确导出
- 查看 `update_readme.py` 的输出

---

## 下一步优化

可考虑的未来改进：

1. **数据库集成**：记录每个订阅的更新历史
2. **高级监控**：内容大小变化警告
3. **多地区支持**：支持不同时区的调度
4. **订阅验证**：周期性验证订阅 URL 有效性
5. **备份系统**：为每个订阅保留版本历史
6. **通知定制**：按订阅类型或优先级发送不同通知

---

## 相关文件

- [订阅配置指南](.github/config/README.md)
- [工作流详情](.github/workflows/update-all.yml)
- [通用更新脚本](.github/scripts/update_subscriptions.py)

