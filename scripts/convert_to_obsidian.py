#!/usr/bin/env python3
"""
将 dataclaw 导出的 JSONL 转换为 Obsidian 笔记
每个会话 → 一则 Markdown 笔记
"""

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

INPUT_FILE = Path(os.environ.get("DATACLAW_EXPORT", Path.home() / "coding/dataclaw/exports/dataclaw_export.jsonl"))
OUTPUT_DIR = Path(os.environ.get("DATACLAW_OBSIDIAN_DIR", Path.home() / "Obsidian/LabNotes/AI对话记录"))
CONVERTED_LOG = Path(os.environ.get("DATACLAW_CONVERTED_LOG", Path.home() / ".dataclaw/converted_sessions.txt"))


def load_converted_ids():
    """加载已转换的 session_id 集合"""
    if CONVERTED_LOG.exists():
        return set(CONVERTED_LOG.read_text(encoding="utf-8").strip().splitlines())
    return set()


def save_converted_id(session_id):
    """追加一个已转换的 session_id"""
    CONVERTED_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(CONVERTED_LOG, "a", encoding="utf-8") as f:
        f.write(session_id + "\n")


def extract_title(messages, max_len=50):
    """从前几条 user 消息提取标题"""
    for msg in messages[:5]:
        if msg.get("role") == "user":
            text = msg.get("content", "").strip()
            if not text:
                continue
            # 取第一行，清理特殊字符
            first_line = text.split("\n")[0].strip()
            # 截断
            if len(first_line) > max_len:
                first_line = first_line[:max_len] + "…"
            if first_line:
                return first_line
    return "无标题会话"


def sanitize_filename(name):
    """清理文件名中的非法字符"""
    name = re.sub(r'[\\/*?:"<>|#^[\]]', "", name)
    name = name.strip(". ")
    return name or "无标题"


def format_date(iso_str):
    """格式化日期"""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return iso_str


def format_date_short(iso_str):
    """短日期，用于文件名"""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except:
        return "unknown"


def extract_conversation(messages):
    """提取对话内容（只要 user/assistant 文字，忽略 tool_uses 和 thinking）"""
    lines = []
    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "")

        if role == "user" and content:
            lines.append(f"> [!question]- 用户\n> {content.strip()}\n")
        elif role == "assistant" and content:
            lines.append(f"> [!note]- 助手\n> {content.strip()}\n")

    return "\n".join(lines)


def convert_session(session):
    """将一个 session 转换为 Obsidian Markdown"""
    messages = session.get("messages", [])
    title = extract_title(messages)
    date_short = format_date_short(session.get("start_time", ""))
    project = session.get("project", "unknown").replace(":", "-")
    source = session.get("source", "unknown")
    model = session.get("model", "unknown")
    stats = session.get("stats", {})

    # 构建 frontmatter
    frontmatter = f"""---
title: "{title}"
date: {format_date(session.get("start_time", ""))}
source: {source}
project: {session.get("project", "")}
model: {model}
session_id: {session.get("session_id", "")}
user_messages: {stats.get("user_messages", 0)}
assistant_messages: {stats.get("assistant_messages", 0)}
tool_uses: {stats.get("tool_uses", 0)}
tags:
  - AI对话
  - {source}
---"""

    # 对话内容
    conversation = extract_conversation(messages)

    body = f"""# {title}

## 基本信息

| 字段 | 值 |
|------|----|
| 来源 | {source} |
| 项目 | {session.get("project", "")} |
| 模型 | {model} |
| 时间 | {format_date(session.get("start_time", ""))} |
| 消息数 | {len(messages)} |

## 对话内容

{conversation}
"""

    return frontmatter + "\n\n" + body


def main():
    sessions = []
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                sessions.append(json.loads(line))

    print(f"读取 {len(sessions)} 个会话")

    # 加载已转换记录
    converted_ids = load_converted_ids()
    print(f"已转换记录: {len(converted_ids)} 个")

    skipped = 0
    created = 0

    for session in sessions:
        session_id = session.get("session_id", "")

        # 跳过已转换的会话
        if session_id in converted_ids:
            skipped += 1
            continue

        source = session.get("source", "unknown")
        project = session.get("project", "unknown").replace(":", "-")
        date_short = format_date_short(session.get("start_time", ""))
        messages = session.get("messages", [])
        title = extract_title(messages)

        # 输出目录按来源分类
        out_dir = OUTPUT_DIR / source
        out_dir.mkdir(parents=True, exist_ok=True)

        # 文件名：日期 + 标题
        safe_title = sanitize_filename(title)
        filename = f"{date_short} {safe_title}.md"
        filepath = out_dir / filename

        # 如果文件名冲突，加 session_id 前缀
        if filepath.exists():
            sid = session_id[:8]
            filename = f"{date_short} {safe_title} [{sid}].md"
            filepath = out_dir / filename

        content = convert_session(session)
        filepath.write_text(content, encoding="utf-8")
        save_converted_id(session_id)
        created += 1

        if created % 20 == 0:
            print(f"  已处理 {created} 个新会话...")

    print(f"\n完成！新增 {created} 个笔记，跳过 {skipped} 个已转换 → {OUTPUT_DIR}")

    # 输出目录统计
    for sub in sorted(OUTPUT_DIR.iterdir()):
        if sub.is_dir():
            count = len(list(sub.glob("*.md")))
            print(f"  {sub.name}/: {count} 个笔记")


if __name__ == "__main__":
    main()
