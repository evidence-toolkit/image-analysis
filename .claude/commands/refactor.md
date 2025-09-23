---
argument-hint: [extract|rename|modernize|simplify] [target] [new-name]
description: Systematic code refactoring with safety checks and automated transformations
allowed-tools: Read, Edit, MultiEdit, Grep, Glob, Bash, TodoWrite
---

# ♻️ Code Refactoring

**Refactoring Operation**: $ARGUMENTS

Safe, systematic code refactoring with comprehensive validation and rollback capabilities.

## Available Refactoring Operations:

### Extract Operations
- `/refactor extract function calculateTotal` - Extract code into new function
- `/refactor extract component UserProfile` - Extract UI component
- `/refactor extract module auth-utils` - Extract functionality into module
- `/refactor extract constant API_ENDPOINTS` - Extract magic numbers/strings

### Rename Operations
- `/refactor rename function oldName newName` - Rename function across codebase
- `/refactor rename variable userId userIdentifier` - Rename variable systematically
- `/refactor rename file old-utils.js new-helpers.js` - Rename and update imports
- `/refactor rename class UserService UserManager` - Rename class and references

### Modernization
- `/refactor modernize javascript` - Update to modern JS features (ES2024)
- `/refactor modernize react` - Update to modern React patterns (hooks, etc.)
- `/refactor modernize css` - Convert to modern CSS (Grid, Flexbox, custom properties)
- `/refactor modernize dependencies` - Update to latest compatible versions

### Simplification
- `/refactor simplify conditions` - Simplify complex conditional logic
- `/refactor simplify loops` - Convert to more readable iteration patterns
- `/refactor simplify nesting` - Reduce nested code complexity
- `/refactor simplify duplicates` - Remove code duplication

## Refactoring Process:

### 1. Safety Analysis
- **Impact assessment**: Identify all affected files and references
- **Dependency mapping**: Understand component relationships
- **Test coverage**: Ensure adequate test protection
- **Backup creation**: Safe rollback points

### 2. Automated Transformation
- **Symbol renaming**: IDE-level renaming with reference updates
- **Code extraction**: Safe method/component extraction
- **Import updates**: Automatic import/export adjustments
- **Pattern replacement**: Systematic code pattern updates

### 3. Validation
- **Compilation checks**: Ensure code still compiles/builds
- **Test execution**: Run affected test suites
- **Lint validation**: Code style and quality checks
- **Type checking**: Static analysis validation

### 4. Documentation
- **Change documentation**: Record refactoring decisions
- **Migration notes**: Breaking change documentation
- **Team communication**: Refactoring impact notifications

## Refactoring Patterns:

### Code Smells Addressed:
- **Long methods**: Extract into smaller, focused functions
- **Large classes**: Split into cohesive components
- **Duplicate code**: Extract common functionality
- **Complex conditionals**: Simplify with early returns or strategy patterns
- **Magic numbers**: Extract into named constants

### Design Improvements:
- **Single Responsibility**: Ensure components have clear purposes
- **Dependency Injection**: Improve testability and flexibility
- **Interface Segregation**: Split large interfaces into focused ones
- **Open/Closed Principle**: Enable extension without modification

## Safety Features:
- **Pre-refactoring snapshots** for easy rollback
- **Incremental changes** with validation at each step
- **Test-driven refactoring** ensuring behavior preservation
- **Impact analysis** showing all affected code paths

## Quality Metrics:
- **Complexity reduction**: Cyclomatic complexity improvements
- **Maintainability index**: Code maintainability scoring
- **Test coverage**: Coverage impact assessment
- **Performance impact**: Ensure no performance regressions

The refactoring system creates TodoWrite tasks for systematic code improvements while maintaining safety and quality throughout the process.