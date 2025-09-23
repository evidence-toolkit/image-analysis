---
argument-hint: <task description or reference>
description: Focus on a specific task with isolated context to prevent context explosion
allowed-tools: TodoWrite, Write, Read, Bash, Grep, Glob, Edit, MultiEdit
---

# 🎯 Focus Mode: Deep Work on Specific Task

**Target Task**: $ARGUMENTS

Use the context-manager subagent to set up focused work session, then work on the specified task.

## Focus Session Setup:

1. **Context Preservation** (context-manager):
   - Save current session progress to `.claude/context/current-session.md`
   - Summarize important decisions and context
   - Note any blockers or dependencies for later
   - Handle worktree context if switching development environments

2. **Task Activation** (task-tracker):
   - Mark the specified task as "in_progress"
   - Set all other tasks to "pending"
   - Load relevant context for this specific task

3. **Work Session**:
   - Focus exclusively on the specified task
   - Avoid scope creep and tangential work
   - Document progress and decisions as you work
   - Create sub-tasks if the work expands

4. **Session Management**:
   - Keep conversation focused on this single task
   - Defer non-critical items to future tasks
   - Prevent context explosion through focused scope
   - Regular progress check-ins and summaries

## Available Tools:
- All development tools (Edit, MultiEdit, Bash, etc.)
- Task management (TodoWrite)
- Context preservation (Read, Write)
- Code exploration (Grep, Glob)

## Focus Principles:
- Single task focus - no multitasking
- Document important decisions
- Create sub-tasks for discovered work
- Maintain clean conversation scope
- Preserve context for future sessions

The context-manager and task-tracker subagents will coordinate to create an optimal focused work environment for this specific task.