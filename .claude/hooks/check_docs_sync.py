#!/usr/bin/env python3
"""
Documentation sync checker for V2 Legal Evidence Analysis System
Triggers documentation-generator agent when core files change.
"""
import os
import sys
from pathlib import Path

# Files that should trigger documentation updates for V2 Legal Evidence Analysis System
CRITICAL_FILES = [
    "v2",                          # CLI interface
    "v2_core_architecture.py",     # Core analysis engine and models
    "CLAUDE.md"                   # Project memory and specifications
]

# File patterns that indicate API or model changes
TRIGGER_PATTERNS = [
    "v2_core_architecture.py",  # Core analysis engine
    "v2",                      # CLI interface
    "requirements.txt",            # Dependencies
    "pyproject.toml",              # Project configuration
    ".claude/agents/*.md",         # Agent definitions
    ".claude/commands/*.md",       # Command definitions
    ".claude/hooks/*.py",          # Hook scripts
]

def should_trigger_docs_update(changed_file_path: str) -> tuple[bool, str]:
    """
    Check if file change should trigger documentation update for V2 system.

    Returns:
        (should_trigger, reason)
    """
    if not changed_file_path:
        return False, ""

    file_path = Path(changed_file_path)
    file_name = file_path.name

    # Check critical V2 system files
    if file_name in CRITICAL_FILES:
        if file_name == "v2":
            return True, "CLI interface updated - CLI documentation may need refresh"
        elif file_name == "v2_core_architecture.py":
            return True, "Core analysis models updated - API and model documentation needs review"
        elif file_name == "CLAUDE.md":
            return True, "Project specifications updated - documentation standards may have changed"
        else:
            return True, f"Critical V2 file {file_name} updated - documentation review needed"

    # Check file patterns
    for pattern in TRIGGER_PATTERNS:
        try:
            if file_path.match(pattern):
                return True, f"Code in {pattern} updated - related documentation may need updates"
        except ValueError:
            # Pattern matching failed, skip
            continue

    # Check for specific API-related changes
    if "openai" in changed_file_path.lower() or "response" in changed_file_path.lower():
        return True, "OpenAI API integration code changed - API documentation needs review"

    # Check for legal evidence model changes
    if any(keyword in changed_file_path.lower() for keyword in ["legal", "evidence", "severity", "compliance"]):
        return True, "Legal evidence models changed - model documentation needs update"

    return False, ""

def get_documentation_recommendations(file_path: str, reason: str) -> list[str]:
    """Get specific documentation recommendations based on changed file."""
    recommendations = []

    if "v2_core_architecture.py" in file_path:
        recommendations.extend([
            "Update Pydantic model documentation for LegalEvidence, SeverityLevel, EvidenceType",
            "Verify OpenAI Responses API examples are correct",
            "Update cost estimates if API usage patterns changed",
            "Review legal compliance documentation"
        ])

    elif file_path.endswith("v2"):
        recommendations.extend([
            "Update CLI usage documentation",
            "Verify command examples and cost estimates",
            "Update user guide and workflow documentation"
        ])

    elif "models" in file_path:
        recommendations.extend([
            "Update API schema documentation",
            "Verify model validation examples",
            "Update legal evidence type documentation"
        ])

    elif "api" in file_path or "openai" in file_path.lower():
        recommendations.extend([
            "Verify OpenAI Responses API examples (NOT ChatCompletions)",
            "Update cost tracking documentation",
            "Review API integration patterns"
        ])

    return recommendations

def main():
    """Main hook execution for documentation sync checking."""

    # Get the file that was just modified
    # Claude Code sets environment variables for hook context
    modified_file = os.environ.get('CLAUDE_MODIFIED_FILE', '')

    # If no specific file, check if we can infer from command arguments
    if not modified_file and len(sys.argv) > 1:
        modified_file = sys.argv[1]

    # Check if this change should trigger documentation updates
    should_trigger, reason = should_trigger_docs_update(modified_file)

    if should_trigger:
        print(f"📝 V2 Legal Evidence Analysis System - Documentation Check")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📄 File changed: {modified_file}")
        print(f"⚠️  Reason: {reason}")
        print()

        recommendations = get_documentation_recommendations(modified_file, reason)
        if recommendations:
            print("📋 Recommended documentation updates:")
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")
            print()

        print("💡 Consider running the documentation-generator agent to update relevant docs:")
        print("   Use the Task tool with subagent_type='documentation-generator'")
        print()

        # Special warnings for critical V2 files
        if "v2_core_architecture.py" in modified_file:
            print("⚠️  CRITICAL: Core analysis engine changed!")
            print("   → Verify OpenAI Responses API examples are still correct")
            print("   → Update cost estimates if needed")
            print("   → Check legal compliance documentation")

        elif modified_file.endswith("v2"):
            print("⚠️  CLI INTERFACE CHANGED")
            print("   → Update user documentation and examples")
            print("   → Verify cost estimates in help text")

    return 0

if __name__ == "__main__":
    sys.exit(main())