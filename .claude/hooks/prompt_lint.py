#!/usr/bin/env python3
import json
import sys
from typing import Any, Dict, List

def main() -> None:
    payload: Dict[str, Any] = json.load(sys.stdin)
    prompt = (payload.get("prompt") or "").strip()

    hints: List[str] = []
    if len(prompt) < 40:
        hints.append("Add a bit more detail so Claude understands the intent.")
    if "please fix" in prompt.lower() and "@" not in prompt:
        hints.append("Reference the specific files or commands to inspect (use @path syntax).")
    if "todo" in prompt.lower():
        hints.append("Clarify whether TODOs should remain or be addressed now.")

    result: Dict[str, Any] = {"continue": True}
    if hints:
        result["systemMessage"] = "Prompt lint suggestions:\n- " + "\n- ".join(hints)

    print(json.dumps(result))

if __name__ == "__main__":
    main()
