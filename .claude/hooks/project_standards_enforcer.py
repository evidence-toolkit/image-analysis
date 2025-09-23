#!/usr/bin/env python3
"""
Project Standards Enforcer Hook

Injects critical project standards and context into all sub-agent invocations via the Task tool.
Ensures consistent behavior across workflow by bridging project context from CLAUDE.md to agents.

Standards enforced:
- UV-first Python development (strict pip/python replacement)
- Tool usage limitations and reminders
- Project-specific coding conventions
- Context preservation principles
"""

import sys
import json

def main():
    try:
        # Read the hook input from stdin
        hook_input = json.loads(sys.stdin.read())

        # Extract the Task tool parameters
        tool_name = hook_input.get('tool', {}).get('name', '')
        tool_params = hook_input.get('tool', {}).get('parameters', {})

        # Only process Task tool invocations
        if tool_name != 'Task':
            print(json.dumps({"approved": True}))
            return

        # Project standards to inject into agent context
        project_standards = """

CRITICAL PROJECT STANDARDS ENFORCEMENT:
═══════════════════════════════════════════════

NEVER USE: pip, pip3, python, python3, poetry, pipenv commands directly
ALWAYS USE UV EQUIVALENTS:

• pip install package → uv add package
• pip install -e . → uv sync --dev
• python script.py → uv run script.py
• python -m module → uv run -m module
• python3 -m venv → uv venv

UV ENFORCEMENT RULES:
1. NEVER use pip, pip3, python, python3, poetry, or pipenv commands directly
2. ALWAYS prefix Python execution with 'uv run'
3. ALWAYS use 'uv add' instead of any install command
4. ALWAYS use 'uv sync' to update project environment
5. IF you attempt forbidden commands, STOP and use UV equivalent instead

TOOL USAGE REMINDER:
- You have limited tool access based on your agent definition
- Do NOT attempt to use tools not explicitly listed in your tools array
- Focus on planning and documentation rather than command execution
- If commands are needed, provide them as instructions for the user

This is STRICT enforcement across ALL Python projects.
═══════════════════════════════════════════════
"""

        # Inject project standards into the agent prompt
        original_prompt = tool_params.get('prompt', '')
        enhanced_prompt = original_prompt + project_standards

        # Update the tool parameters
        tool_params['prompt'] = enhanced_prompt

        # Return the modified tool call
        modified_tool = hook_input.copy()
        modified_tool['tool']['parameters'] = tool_params

        print(json.dumps({
            "approved": True,
            "modified_tool": modified_tool['tool']
        }))

    except Exception as e:
        # On error, allow the original tool call to proceed
        print(json.dumps({
            "approved": True,
            "error": str(e)
        }), file=sys.stderr)

if __name__ == "__main__":
    main()