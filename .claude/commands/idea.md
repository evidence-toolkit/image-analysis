---
argument-hint: <idea description>
description: Capture and develop new project ideas into actionable task plans
allowed-tools: TodoWrite, Write, Read, Grep
---

# 💡 New Project Idea Development

You have a new project idea: **$ARGUMENTS**

Use the project-starter subagent to:

1. **Clarify and refine** this idea by asking focused questions about:
   - Core functionality and purpose
   - Target users and use cases
   - Technical requirements and constraints
   - Success criteria and scope

2. **Create a structured breakdown** of the idea into:
   - MVP (Minimum Viable Product) features
   - Core development tasks
   - Testing and validation steps
   - Optional future enhancements

3. **Generate an actionable task list** using TodoWrite with:
   - Specific, concrete tasks
   - Logical sequencing and dependencies
   - Clear acceptance criteria
   - Complexity estimates

4. **Set up project context** by creating/updating `.claude/context/project-overview.md` with:
   - Project description and goals
   - Technical stack decisions
   - Key assumptions and constraints
   - Success metrics

Focus on creating the smallest possible working version first, then building from there. Break down complex tasks into manageable chunks that can be completed in under 2 hours each.

The project-starter subagent should take the lead on this process.