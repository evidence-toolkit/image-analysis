#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, TypedDict  # update imports

class FormatterSpec(TypedDict):
    suffixes: Set[str]
    command: List[str]

FORMATTERS: List[FormatterSpec] = [
    {"suffixes": {".py"}, "command": ["python3", "-m", "black"]},
    {"suffixes": {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}, "command": ["npx", "prettier", "--write"]},
    {"suffixes": {".json", ".jsonc"}, "command": ["npx", "prettier", "--write"]},
]

def main() -> None:
    payload: Dict[str, Any] = json.load(sys.stdin)
    file_path = (payload.get("tool_input") or {}).get("file_path")
    if not file_path:
        sys.exit(0)

    path = Path(file_path)
    if not path.exists():
        # File may be new; let Claude handle follow-up.
        sys.exit(0)

    for formatter in FORMATTERS:
        if path.suffix in formatter["suffixes"]:
            cmd = [*formatter["command"], str(path)]
            try:
                subprocess.run(cmd, check=False)
            except FileNotFoundError:
                sys.stderr.write(
                    "Formatter not found for command: {cmd}. Install the tool or adjust FORMATTERS.\n"
                    .format(cmd=" ".join(cmd))
                )
            break

if __name__ == "__main__":
    main()
