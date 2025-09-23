#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

FORBIDDEN_FRAGMENTS: List[str] = [
    ".env",
    "secrets",
    "infra/prod",
    "deployment/production",
]

def main() -> None:
    payload: Dict[str, Any] = json.load(sys.stdin)
    file_path = (payload.get("tool_input") or {}).get("file_path", "")
    if not file_path:
        sys.exit(0)

    path = Path(file_path)
    hits = [fragment for fragment in FORBIDDEN_FRAGMENTS if fragment in path.as_posix()]

    if hits:
        sys.stderr.write(
            "Write blocked for {path} (matched: {hits}). "
            "Update FORBIDDEN_FRAGMENTS in enforce_write_policy.py if this is intentional.\n"
            .format(path=path.as_posix(), hits=", ".join(hits))
        )
        sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
