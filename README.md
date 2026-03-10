# DataClaw Sync

[English](README.md) | [中文](README_zh.md)
<img width="2696" height="1138" alt="Gemini_Generated_Image_iiawauiiawauiiaw" src="https://github.com/user-attachments/assets/683bb99e-ca61-4cb4-a567-a0743dadf47e" />

Incrementally export AI agent conversations and convert them into Obsidian notes.

## What is this?

**dataclaw-sync** is a [Skill](https://docs.anthropic.com/en/docs/claude-code/skills) (an AI agent extension) and a standalone Python script that bridges [DataClaw](https://github.com/peteromallet/dataclaw) with [Obsidian](https://obsidian.md).

**What is a Skill?** A Skill is a modular extension that gives AI coding agents new capabilities. Once installed, you can trigger it with a slash command (e.g. `/dataclaw-sync`) and the agent will execute the full workflow automatically.

> **Don't use a Skill-compatible agent?** No problem — the core script `convert_to_obsidian.py` runs with plain `python3`, no agent required.

## Features

- Export conversations from **7 sources**: Claude Code, Codex, Gemini CLI, Kimi, OpenCode, OpenClaw, Custom
- **Incremental conversion**: only processes new sessions, never duplicates
- Structured **Obsidian Markdown** with frontmatter (Dataview-compatible)
- Auto-organized by source (`claude/`, `opencode/`, `kimi/`, etc.)
- Optional upload to Hugging Face

## Install

### 1. Install DataClaw

```bash
brew install pipx
pipx install dataclaw
```

### 2. Clone this repo

```bash
git clone https://github.com/UFOyyds/dataclaw-sync.git
```

### 3. Install as Skill (optional)

There is no unified Skill directory standard across AI coding agents. Each tool has its own path convention:

| Agent | Skill Directory |
|-------|----------------|
| Claude Code | `~/.claude/skills/dataclaw-sync/` |
| Codex | `~/.agents/skills/dataclaw-sync/` |
| OpenCode | `~/.config/opencode/skills/dataclaw-sync/` |
| Gemini CLI | `~/.gemini/skills/dataclaw-sync/` |
| OpenClaw | `~/.openclaw/skills/dataclaw-sync/` |

> **Note**: OpenCode and Gemini CLI also support `~/.agents/skills/` — if you've already set up the Codex path, they will discover it automatically without extra configuration.

Copy `SKILL.md` and `scripts/` into the corresponding directory. Once installed, trigger with `/dataclaw-sync`.

> **Tip**: To maintain a single source and support multiple agents, use a shared directory with symlinks:
>
> ```bash
> # Single source of truth
> mkdir -p ~/agent-skills/dataclaw-sync
> cp -r SKILL.md scripts/ ~/agent-skills/dataclaw-sync/
>
> # Symlink to each agent
> ln -s ~/agent-skills/dataclaw-sync ~/.claude/skills/dataclaw-sync
> ln -s ~/agent-skills/dataclaw-sync ~/.agents/skills/dataclaw-sync
> ln -s ~/agent-skills/dataclaw-sync ~/.config/opencode/skills/dataclaw-sync
> ln -s ~/agent-skills/dataclaw-sync ~/.gemini/skills/dataclaw-sync
> ln -s ~/agent-skills/dataclaw-sync ~/.openclaw/skills/dataclaw-sync
> ```

### Update Skill

Pull the latest version from GitHub:

```bash
cd ~/agent-skills/dataclaw-sync  # or wherever you installed it
curl -sL https://raw.githubusercontent.com/UFOyyds/dataclaw-sync/main/convert_to_obsidian.py \
  -o scripts/convert_to_obsidian.py
curl -sL https://raw.githubusercontent.com/UFOyyds/dataclaw-sync/main/SKILL.md \
  -o SKILL.md
```

If using symlinks, all agents pick up the update automatically.

## Usage

### Option A: Via Skill

Type `/dataclaw-sync` in your AI agent. The agent handles everything automatically.

### Option B: Manual

```bash
# Step 1: Export conversations locally
dataclaw export --no-push -o ./exports/dataclaw_export.jsonl

# Step 2: Convert new sessions to Obsidian notes
python3 convert_to_obsidian.py
```

## Configuration

### Environment Variables

Customize paths via environment variables (defaults used if not set):

| Variable | Description | Default |
|----------|-------------|---------|
| `DATACLAW_EXPORT` | Export file path | `~/dataclaw/exports/dataclaw_export.jsonl` |
| `DATACLAW_OBSIDIAN_DIR` | Obsidian output directory | `~/ObsidianVault/AI对话记录` |
| `DATACLAW_CONVERTED_LOG` | Converted sessions log | `~/.dataclaw/converted_sessions.txt` |

Example:

```bash
export DATACLAW_EXPORT="$HOME/dataclaw/exports/dataclaw_export.jsonl"
export DATACLAW_OBSIDIAN_DIR="$HOME/my-vault/AI对话记录"
python3 convert_to_obsidian.py
```

### DataClaw Config

```bash
dataclaw config --source all                    # Set export source
dataclaw config --exclude "project1,project2"   # Exclude projects
dataclaw config --redact "secret-string"        # Redact strings
dataclaw config                                 # View config
```

## Note Format

Each note contains:

- **Frontmatter**: title, date, source, project, model, session_id, tags
- **Info table**: source, project, model, time, message count
- **Conversation**: user/assistant messages as Obsidian callouts

## Acknowledgements

- [DataClaw](https://github.com/peteromallet/dataclaw) — AI conversation export tool
- [Obsidian](https://obsidian.md) — Local-first knowledge management

## License

MIT
