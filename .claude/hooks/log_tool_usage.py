#!/usr/bin/env python3
import datetime
import json
import os
import sys
from typing import Any, Dict

def main() -> None:
    try:
        payload: Dict[str, Any] = json.load(sys.stdin)
    except json.JSONDecodeError:
        return

    log_dir = os.path.expanduser("~/.claude/logs")
    os.makedirs(log_dir, exist_ok=True)

    tool = payload.get("tool_name", "unknown")
    tool_input = payload.get("tool_input", {}) or {}

    summary = tool_input.get("description") or ""
    command = tool_input.get("command")
    if not summary and command:
        if isinstance(command, list):
            summary = " ".join(str(part) for part in command)
        else:
            summary = str(command)

    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "event": payload.get("hook_event_name", ""),
        "tool": tool,
        "target": tool_input.get("file_path")
                 or tool_input.get("glob")
                 or tool_input.get("path")
                 or "",
        "summary": summary.strip(),
    }

    log_path = os.path.join(log_dir, "pretool.log")
    with open(log_path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    main()
