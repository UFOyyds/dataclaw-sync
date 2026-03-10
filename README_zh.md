# DataClaw Sync

[English](README.md) | [中文](README_zh.md)

将 AI Agent 对话记录增量导出并转换为 Obsidian 笔记。

## 这是什么？

**dataclaw-sync** 是一个 [Skill](https://docs.anthropic.com/en/docs/claude-code/skills)（AI Agent 技能扩展）+ 独立 Python 脚本，连接 [DataClaw](https://github.com/peteromallet/dataclaw) 与 [Obsidian](https://obsidian.md)。

**什么是 Skill？** Skill 是一种模块化扩展，为 AI 编程代理提供新能力。安装后，输入斜杠命令（如 `/dataclaw-sync`）即可自动执行完整工作流。

> **不使用支持 Skill 的 Agent？** 没关系 — 核心脚本 `convert_to_obsidian.py` 用 `python3` 直接运行即可。

## 功能

- 支持 **7 种来源**导出：Claude Code、Codex、Gemini CLI、Kimi、OpenCode、OpenClaw、Custom
- **增量转换**：只处理新增会话，不重复生成
- 结构化 **Obsidian Markdown**，含 frontmatter（支持 Dataview 查询）
- 按来源自动分目录（`claude/`、`opencode/`、`kimi/` 等）
- 可选上传到 Hugging Face

## 安装

### 1. 安装 DataClaw

```bash
brew install pipx
pipx install dataclaw
```

### 2. 克隆本仓库

```bash
git clone https://github.com/UFOyyds/dataclaw-sync.git
```

### 3. 安装为 Skill（可选）

目前没有跨所有 AI coding agents 的统一 Skill 目录标准，各工具有各自的路径约定：

| Agent | Skill 目录 |
|-------|-----------|
| Claude Code | `~/.claude/skills/dataclaw-sync/` |
| Codex | `~/.agents/skills/dataclaw-sync/` |
| OpenCode | `~/.config/opencode/skills/dataclaw-sync/` |
| Gemini CLI | `~/.gemini/skills/dataclaw-sync/` |
| OpenClaw | `~/.openclaw/skills/dataclaw-sync/` |

> **注意**：OpenCode 和 Gemini CLI 也兼容 `~/.agents/skills/`，若已配置 Codex 路径则无需重复安装。

将 `SKILL.md` 和 `scripts/` 复制到对应目录，然后输入 `/dataclaw-sync` 触发。

> **建议**：维护一份源码，通过符号链接分发到各 Agent 路径：
>
> ```bash
> # 统一源码目录
> mkdir -p ~/agent-skills/dataclaw-sync
> cp -r SKILL.md scripts/ ~/agent-skills/dataclaw-sync/
>
> # 符号链接到各 Agent
> ln -s ~/agent-skills/dataclaw-sync ~/.claude/skills/dataclaw-sync
> ln -s ~/agent-skills/dataclaw-sync ~/.agents/skills/dataclaw-sync
> ln -s ~/agent-skills/dataclaw-sync ~/.config/opencode/skills/dataclaw-sync
> ln -s ~/agent-skills/dataclaw-sync ~/.gemini/skills/dataclaw-sync
> ln -s ~/agent-skills/dataclaw-sync ~/.openclaw/skills/dataclaw-sync
> ```

### 更新 Skill

从 GitHub 拉取最新版本：

```bash
cd ~/agent-skills/dataclaw-sync  # 或你安装的位置
curl -sL https://raw.githubusercontent.com/UFOyyds/dataclaw-sync/main/convert_to_obsidian.py \
  -o scripts/convert_to_obsidian.py
curl -sL https://raw.githubusercontent.com/UFOyyds/dataclaw-sync/main/SKILL.md \
  -o SKILL.md
```

如果使用符号链接，所有 Agent 会自动获取更新。

## 使用

### 方式一：通过 Skill 触发

在 AI Agent 中输入 `/dataclaw-sync`，Agent 自动完成全流程。

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
