---
argument-hint: [create|list|switch|cleanup] [branch-name|path]
description: Manage Git worktrees for parallel development sessions
allowed-tools: Bash, Read, Write, TodoWrite
---

# 🌳 Git Worktree Management

**Operation**: $ARGUMENTS

Use the worktree-manager subagent to handle parallel development environments.

## Available Operations:

### Create New Worktree
- `/worktree create feature-auth` - Create new worktree with new branch
- `/worktree create feature-auth existing-branch` - Create worktree from existing branch
- Automatically sets up development environment
- Copies `.claude/` configuration for consistent workflow
- Provides instructions for switching to new environment

### List Current Worktrees
- `/worktree list` - Show all worktrees with status
- Display branch names, paths, and current status
- Identify which worktree is currently active
- Show any uncommitted changes or issues

### Switch Between Worktrees
- `/worktree switch ../project-bugfix` - Switch to existing worktree
- Save current context before switching
- Provide clear navigation instructions
- Handle Claude Code session management

### Cleanup Completed Work
- `/worktree cleanup feature-auth` - Remove completed worktree
- Check for uncommitted changes before removal
- Clean up both worktree and branch if requested
- Ensure no data loss during cleanup

## Worktree Benefits:
- Complete code isolation between parallel tasks
- Independent Claude Code sessions per worktree
- No interference between different development streams
- Easy context switching for complex projects

## Environment Setup:
- Each worktree maintains its own file state
- Development dependencies need setup per worktree
- Claude Code context is copied for consistency
- Git history and remotes are shared

The worktree-manager subagent will handle all Git operations safely and provide clear guidance for working with multiple development environments.