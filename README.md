# DataClaw Sync

Incrementally export AI agent conversations and convert them into Obsidian notes.

将 AI Agent 对话记录增量导出并转换为 Obsidian 笔记。

---

## What is this? / 这是什么？

**dataclaw-sync** is a [Skill](https://docs.anthropic.com/en/docs/claude-code/skills) (an AI agent extension) and a standalone Python script that bridges [DataClaw](https://github.com/peteromallet/dataclaw) with [Obsidian](https://obsidian.md).

**dataclaw-sync** 是一个 [Skill](https://docs.anthropic.com/en/docs/claude-code/skills)（AI Agent 技能扩展）+ 独立 Python 脚本，连接 [DataClaw](https://github.com/peteromallet/dataclaw) 与 [Obsidian](https://obsidian.md)。

**What is a Skill?** A Skill is a modular extension that gives AI coding agents new capabilities. Once installed, you can trigger it with a slash command (e.g. `/dataclaw-sync`) and the agent will execute the full workflow automatically.

**什么是 Skill？** Skill 是一种模块化扩展，为 AI 编程代理提供新能力。安装后，输入斜杠命令（如 `/dataclaw-sync`）即可自动执行完整工作流。

> **Don't use a Skill-compatible agent?** No problem — the core script `convert_to_obsidian.py` runs with plain `python3`, no agent required.
>
> **不使用支持 Skill 的 Agent？** 没关系 — 核心脚本 `convert_to_obsidian.py` 用 `python3` 直接运行即可。

## Features / 功能

- Export conversations from **7 sources**: Claude Code, Codex, Gemini CLI, Kimi, OpenCode, OpenClaw, Custom
- **Incremental conversion**: only processes new sessions, never duplicates
- Structured **Obsidian Markdown** with frontmatter (Dataview-compatible)
- Auto-organized by source (`claude/`, `opencode/`, `kimi/`, etc.)
- Optional upload to Hugging Face

---

- 支持 **7 种来源**导出：Claude Code、Codex、Gemini CLI、Kimi、OpenCode、OpenClaw、Custom
- **增量转换**：只处理新增会话，不重复生成
- 结构化 **Obsidian Markdown**，含 frontmatter（支持 Dataview 查询）
- 按来源自动分目录（`claude/`、`opencode/`、`kimi/` 等）
- 可选上传到 Hugging Face

## Install / 安装

### 1. Install DataClaw / 安装 DataClaw

```bash
brew install pipx
pipx install dataclaw
```

### 2. Clone this repo / 克隆本仓库

```bash
git clone https://github.com/UFOyyds/dataclaw-sync.git
```

### 3. Install as Skill (optional) / 安装为 Skill（可选）

There is no unified Skill directory standard across AI coding agents. Each tool has its own path convention:

目前没有跨所有 AI coding agents 的统一 Skill 目录标准，各工具有各自的路径约定：

| Agent | Skill Directory |
|-------|----------------|
| Claude Code | `~/.claude/skills/dataclaw-sync/` |
| Codex | `~/.agents/skills/dataclaw-sync/` |
| OpenClaw | `~/.openclaw/skills/dataclaw-sync/` |

Copy `SKILL.md` and `scripts/` into the corresponding directory. Once installed, trigger with `/dataclaw-sync`.

将 `SKILL.md` 和 `scripts/` 复制到对应目录，然后输入 `/dataclaw-sync` 触发。

> **Tip**: To maintain a single source and support multiple agents, use a shared directory with symlinks:
>
> **建议**：维护一份源码，通过符号链接分发到各 Agent 路径：
>
> ```bash
> # Single source of truth
> mkdir -p ~/agent-skills/dataclaw-sync
> cp -r SKILL.md scripts/ ~/agent-skills/dataclaw-sync/
>
> # Symlink to each agent
> ln -s ~/agent-skills/dataclaw-sync ~/.claude/skills/dataclaw-sync
> ln -s ~/agent-skills/dataclaw-sync ~/.agents/skills/dataclaw-sync
> ln -s ~/agent-skills/dataclaw-sync ~/.openclaw/skills/dataclaw-sync
> ```

### Update Skill / 更新 Skill

Pull the latest version from GitHub:

从 GitHub 拉取最新版本：

```bash
cd ~/agent-skills/dataclaw-sync  # or wherever you installed it
curl -sL https://raw.githubusercontent.com/UFOyyds/dataclaw-sync/main/convert_to_obsidian.py \
  -o scripts/convert_to_obsidian.py
curl -sL https://raw.githubusercontent.com/UFOyyds/dataclaw-sync/main/SKILL.md \
  -o SKILL.md
```

If using symlinks, all agents pick up the update automatically.

如果使用符号链接，所有 Agent 会自动获取更新。

## Usage / 使用

### Option A: Via Skill / 通过 Skill 触发

Type `/dataclaw-sync` in your AI agent. The agent handles everything automatically.

在 AI Agent 中输入 `/dataclaw-sync`，Agent 自动完成全流程。

### Option B: Manual / 手动执行

```bash
# Step 1: Export conversations locally
dataclaw export --no-push -o ./exports/dataclaw_export.jsonl

# Step 2: Convert new sessions to Obsidian notes
python3 convert_to_obsidian.py
```

## Configuration / 配置

### Environment Variables / 环境变量

Customize paths via environment variables (defaults used if not set):

通过环境变量自定义路径（不设则使用默认值）：

| Variable | Description | Default |
|----------|-------------|---------|
| `DATACLAW_EXPORT` | Export file path / 导出文件路径 | `~/dataclaw/exports/dataclaw_export.jsonl` |
| `DATACLAW_OBSIDIAN_DIR` | Obsidian output dir / 笔记输出目录 | `~/ObsidianVault/AI对话记录` |
| `DATACLAW_CONVERTED_LOG` | Converted sessions log / 已转换记录 | `~/.dataclaw/converted_sessions.txt` |

Example / 示例：

```bash
export DATACLAW_EXPORT="$HOME/dataclaw/exports/dataclaw_export.jsonl"
export DATACLAW_OBSIDIAN_DIR="$HOME/my-vault/AI对话记录"
python3 convert_to_obsidian.py
```

### DataClaw Config / DataClaw 配置

```bash
dataclaw config --source all                    # Set export source / 设置导出来源
dataclaw config --exclude "project1,project2"   # Exclude projects / 排除项目
dataclaw config --redact "secret-string"        # Redact strings / 脱敏字符串
dataclaw config                                 # View config / 查看配置
```

## Note Format / 笔记格式

Each note contains / 每则笔记包含：

- **Frontmatter**: title, date, source, project, model, session_id, tags
- **Info table / 基本信息表**: source, project, model, time, message count
- **Conversation / 对话内容**: user/assistant messages as Obsidian callouts

## Acknowledgements / 致谢

- [DataClaw](https://github.com/peteromallet/dataclaw) — AI conversation export tool / AI 对话导出工具
- [Obsidian](https://obsidian.md) — Local-first knowledge management / 本地知识库管理

## License

MIT
