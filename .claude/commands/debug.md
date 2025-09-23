# /debug [error|performance|test|integration] [description]

Debug issues using the specialized debug-specialist sub-agent.

## Usage Examples

```bash
# Debug a specific error
/debug error "TypeError: Cannot read property 'id' of undefined in user.service.js"

# Debug performance issues
/debug performance "API responses taking 5+ seconds"

# Debug test failures
/debug test "Jest tests failing with async timeout errors"

# Debug integration problems
/debug integration "Third-party API returning 401 errors"

# General debugging (auto-detects type)
/debug "Database connection randomly dropping"
```

## Process

1. **Activates debug-specialist sub-agent** with full context
2. **Creates TodoWrite task list** for complex debugging workflows
3. **Provides systematic investigation** with evidence-based diagnosis
4. **Implements targeted fixes** with verification steps
5. **Documents lessons learned** and prevention measures

## Integration

- Works with `/focus` for isolated debugging sessions
- Integrates with `/tasks` for progress tracking
- Coordinates with other sub-agents when needed
- Preserves debugging context across sessions

The debug-specialist sub-agent will automatically:
- Analyze error messages and stack traces
- Form testable hypotheses about root causes
- Implement systematic investigation procedures
- Provide comprehensive fixes with verification
- Suggest prevention measures and monitoring improvements