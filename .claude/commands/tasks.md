---
argument-hint: [view|add|done|priority] [task description]
description: View and manage your current task list using TodoWrite
allowed-tools: TodoWrite, Read, Write
---

# 📋 Task Management

**Action**: $ARGUMENTS

Use the task-tracker subagent to handle this task management request.

## Available Actions:

### View Tasks (default)
- `/tasks` or `/tasks view` - Show current task list with status
- Display progress summary (X/Y completed)
- Show active task (what's in progress)
- Suggest next task to work on
- Identify any blockers or dependencies

### Add New Task
- `/tasks add <description>` - Add a new task to the list
- Ensure task is specific and actionable
- Generate proper content and activeForm
- Place in logical priority order

### Mark Task Complete
- `/tasks done <task reference>` - Mark task as completed
- Only mark truly finished tasks as complete
- Update task list and suggest next action
- Archive completed task information if needed

### Priority Management
- `/tasks priority` - Review and adjust task priorities
- Suggest optimal task ordering
- Identify dependencies and blockers
- Recommend which task to focus on next

## Task Management Principles:
- Maintain exactly ONE task in "in_progress" status
- Keep tasks specific and actionable (< 2 hours work)
- Provide both imperative and active forms
- Track dependencies and blockers
- Suggest logical next steps

The task-tracker subagent will use TodoWrite to maintain your task list and provide helpful status updates and recommendations.