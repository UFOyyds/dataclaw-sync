---
name: dataclaw-sync
description: 增量同步 AI 对话记录到 Obsidian。使用 DataClaw 导出 Claude Code、OpenCode、Codex、Kimi、Gemini CLI、OpenClaw 等 AI Agent 的对话，转换为 Obsidian 笔记存入 LabNotes vault。支持增量更新，只处理新增会话。可选上传到 Hugging Face。当用户说"同步对话"、"导出对话"、"sync conversations"、"对话存档到 Obsidian"、"/dataclaw-sync" 时触发。
---

# DataClaw Sync

将 AI Agent 对话记录增量导出并转换为 Obsidian 笔记。

## 前置检查

```bash
command -v dataclaw >/dev/null 2>&1 && echo "dataclaw: OK" || echo "NOT INSTALLED — run: pipx install dataclaw"
```

若未安装，执行 `pipx install dataclaw`（需先 `brew install pipx`）。

## 支持的来源

claude、codex、gemini、kimi、opencode、openclaw、custom。不支持 Cursor 等 AI IDE。

## 工作流

### Step 1: 导出对话

```bash
dataclaw export --no-push -o ~/coding/dataclaw/exports/dataclaw_export.jsonl
```

- `--no-push` 仅本地导出，不上传 HF
- `--source` 筛选来源：`claude`、`codex`、`gemini`、`kimi`、`opencode`、`openclaw`、`all`（默认 all）
- 超时设置 180s（大量会话时需要时间）

### Step 2: 增量转换为 Obsidian 笔记

```bash
python3 ~/.claude/skills/dataclaw-sync/scripts/convert_to_obsidian.py
```

脚本特性：
- 读取 `~/.dataclaw/converted_sessions.txt` 跳过已处理的 session_id
- 新会话按来源分目录写入 Obsidian vault 的 `AI对话记录/{source}/`
- 文件名格式：`{日期} {标题}.md`，标题从首条 user 消息提取
- 每则笔记含 frontmatter（source、project、model、date、tags）

可通过环境变量自定义路径（不设则使用默认值）：

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `DATACLAW_EXPORT` | 导出文件路径 | `~/coding/dataclaw/exports/dataclaw_export.jsonl` |
| `DATACLAW_OBSIDIAN_DIR` | Obsidian 笔记目录 | `~/Obsidian/LabNotes/AI对话记录` |
| `DATACLAW_CONVERTED_LOG` | 已转换记录文件 | `~/.dataclaw/converted_sessions.txt` |

### Step 3: 确认结果

报告给用户：
- 新增了多少条笔记
- 各来源分布（claude/opencode/kimi 等）
- 笔记存放路径

### Step 4（可选）: 上传到 Hugging Face

仅在用户明确要求上传时执行。

1. 确认 HF 已登录：`hf auth login --token <TOKEN>`，并脱敏 token：`dataclaw config --redact "<TOKEN>"`
2. 设置 repo：`dataclaw config --repo "username/dataset-name"`
3. PII 审查 — 询问用户全名，运行扫描命令：
   ```bash
   grep -i 'FULL_NAME' ~/coding/dataclaw/exports/dataclaw_export.jsonl | head -10
   ```
4. 询问是否有公司名、客户名、私有 URL 等需要脱敏，用 `dataclaw config --redact "string"` 添加
5. 执行确认：`dataclaw confirm --full-name "NAME" --attest-full-name "..." --attest-sensitive "..." --attest-manual-scan "..."`
6. 用户明确同意后推送：`dataclaw export --publish-attestation "User explicitly approved publishing."`

## 配置管理

排除项目：`dataclaw config --exclude "project1,project2"`
脱敏字符串：`dataclaw config --redact "secret"`
脱敏用户名：`dataclaw config --redact-usernames "handle"`
查看配置：`dataclaw config`
查看状态：`dataclaw status`

## 关键路径

| 用途 | 路径 |
|------|------|
| 导出文件 | `~/coding/dataclaw/exports/dataclaw_export.jsonl` |
| 笔记目录 | `~/Obsidian/LabNotes/AI对话记录/` |
| 已转换记录 | `~/.dataclaw/converted_sessions.txt` |
| 转换脚本 | `~/.claude/skills/dataclaw-sync/scripts/convert_to_obsidian.py` |
| dataclaw 配置 | `~/.dataclaw/config.json` |
