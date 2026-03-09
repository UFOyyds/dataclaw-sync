# DataClaw Sync

将 AI Agent 对话记录增量导出并转换为 Obsidian 笔记。

基于 [DataClaw](https://github.com/peteromallet/dataclaw) 导出 Claude Code、OpenCode、Codex、Kimi、Gemini CLI、OpenClaw 等 AI Agent 的对话，转换为结构化的 Obsidian Markdown 笔记，支持增量更新。

## 功能

- 一键导出所有 AI Agent 对话记录
- 增量转换：只处理新增会话，不重复生成
- 每则笔记含 frontmatter（支持 Dataview 查询）
- 按来源自动分目录（claude/opencode/kimi 等）
- 可选上传到 Hugging Face

## 安装

### 1. 安装 DataClaw

```bash
brew install pipx
pipx install dataclaw
```

### 2. 安装 Skill（可选，Claude Code / OpenCode 用户）

```bash
dataclaw update-skill claude
```

### 3. 克隆本仓库

```bash
git clone https://github.com/YOUR_USERNAME/dataclaw-sync.git
```

## 使用

### 方式一：通过 Skill 触发

在 Claude Code 或 OpenCode 中输入 `/dataclaw-sync`，自动执行完整流程。

### 方式二：手动执行

```bash
# Step 1: 导出对话（本地，不上传）
dataclaw export --no-push -o ./exports/dataclaw_export.jsonl

# Step 2: 增量转换为 Obsidian 笔记
python3 convert_to_obsidian.py
```

## 配置

### 环境变量

通过环境变量自定义路径（不设则使用默认值）：

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `DATACLAW_EXPORT` | 导出文件路径 | `~/dataclaw/exports/dataclaw_export.jsonl` |
| `DATACLAW_OBSIDIAN_DIR` | Obsidian 笔记输出目录 | `~/ObsidianVault/AI对话记录` |
| `DATACLAW_CONVERTED_LOG` | 已转换记录文件 | `~/.dataclaw/converted_sessions.txt` |

示例：

```bash
export DATACLAW_EXPORT="$HOME/dataclaw/exports/dataclaw_export.jsonl"
export DATACLAW_OBSIDIAN_DIR="$HOME/my-vault/AI对话记录"
python3 convert_to_obsidian.py
```

### DataClaw 配置

```bash
dataclaw config --source all                    # 设置导出来源
dataclaw config --exclude "project1,project2"   # 排除项目
dataclaw config --redact "secret-string"        # 脱敏字符串
dataclaw config                                 # 查看当前配置
```

### 支持的来源

claude、codex、gemini、kimi、opencode、openclaw、custom

## 笔记格式

每则笔记包含：

- **Frontmatter**：title、date、source、project、model、session_id、tags
- **基本信息表**：来源、项目、模型、时间、消息数
- **对话内容**：user/assistant 消息以 Obsidian callout 形式展示

## 致谢

- [DataClaw](https://github.com/peteromallet/dataclaw) — AI 对话导出工具
- [Obsidian](https://obsidian.md) — 本地知识库管理

## License

MIT
