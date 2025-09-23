---
argument-hint: [platform] [push|pull|status]
description: Sync tasks with external systems like GitHub Issues or Linear  (optional MCP integration)
allowed-tools: TodoWrite, Read, Write, Bash
---

# 🔄 External System Sync

**Sync Request**: $ARGUMENTS

Use the sync-agent subagent to handle synchronization with external project management systems.

## Available Sync Operations:

### Platform Status
- `/sync` or `/sync status` - Check available MCP integrations
- Show connected systems (GitHub, Linear, etc.)
- Display sync capabilities and current status
- List authentication requirements

### Push to External System
- `/sync github push` - Push local tasks to GitHub Issues
- `/sync linear push` - Push local tasks to Linear tickets
- `/sync [platform] push` - Push to specified platform
- Convert TodoWrite tasks to appropriate external formats

### Pull from External System
- `/sync github pull` - Import GitHub Issues as local tasks
- `/sync linear pull` - Import Linear tickets as local tasks
- `/sync [platform] pull` - Pull from specified platform
- Merge external items into local TodoWrite system

### Bidirectional Sync
- `/sync [platform]` - Two-way sync with specified platform
- Handle conflicts by asking user preference
- Update task status in both systems
- Maintain traceability between systems

## Sync Principles:
- Local TodoWrite system is always the source of truth
- External sync is completely optional
- Never break local workflow for external systems
- Work offline gracefully when MCP unavailable
- Provide clear sync status and feedback

## Fallback Options:
- Export tasks to standard formats (Markdown, JSON)
- Manual copy/paste workflows
- URL generation for external system creation
- Offline-first operation

The sync-agent will:
1. Check for available MCP servers and authentication
2. Show what will be synced before proceeding
3. Handle conflicts and authentication issues gracefully
4. Update local tasks with external IDs/URLs when successful
5. Provide detailed sync status and any error information

All sync operations are optional - your local task management works perfectly without any external systems.