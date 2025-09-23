# Claude-Stuff Project Overview

## Current Project: DotMgr - CLI Dotfiles Management Tool

### Project Description
DotMgr is a zero-configuration CLI tool for managing dotfiles that follows a "convention over configuration" philosophy. Unlike existing tools like chezmoi, GNU Stow, or dotbot, DotMgr requires no setup files while providing intelligent auto-discovery, automatic backups, and built-in git integration.

### Core Value Proposition
- **Zero Configuration**: No YAML, TOML, or config files required
- **Safety First**: Automatic backups before any changes
- **Smart Discovery**: Automatically finds common dotfiles
- **Single Binary**: Rust-compiled executable with no dependencies
- **Git Integration**: Built-in version control for dotfiles

### Goals
- **Primary**: Create a dotfiles manager that "just works" without complex setup
- **Secondary**: Provide safe, reversible operations that never lose user data
- **Tertiary**: Demonstrate superior simplicity compared to existing complex tools

### Target Users
- **Primary**: Developers who want simple dotfiles management
- **Secondary**: System administrators managing multiple machines
- **Tertiary**: Power users transitioning from manual symlink management

## Technical Architecture

### Technology Stack
- **Language**: Rust (single binary, performance, memory safety)
- **CLI Framework**: clap for argument parsing and help generation
- **File Operations**: std::fs with comprehensive error handling
- **Git Integration**: git2 crate for repository operations
- **Configuration**: Optional TOML for advanced users

### Core Components
1. **Discovery Engine**: Scans home directory for common dotfiles
2. **Backup System**: Creates safe backups before any modifications
3. **Repository Manager**: Handles git operations for dotfile storage
4. **Symlink Manager**: Creates and maintains symlinks between repo and home
5. **Status Reporter**: Shows current state of managed vs unmanaged files

### Key Design Principles
- **Convention over Configuration**: Smart defaults, minimal setup required
- **Safety First**: Always backup, never destructive operations
- **Transparency**: Clear status reporting, obvious what the tool is doing
- **Reversibility**: Easy to undo any operation

## Success Metrics
- **Usability**: New user can manage dotfiles in under 5 minutes
- **Safety**: Zero data loss incidents during normal operation
- **Adoption**: Simpler than existing tools for 80% of use cases
- **Reliability**: Works consistently across Linux, macOS, and Windows

## Key Assumptions
- Users want git-based dotfile management
- Symlinks are acceptable on target platforms
- Home directory scanning is acceptable for discovery
- Users prefer opinionated defaults over endless configuration

## Constraints
- Must work without network access after initial setup
- Single binary distribution preferred
- No external dependencies beyond git
- Cross-platform compatibility required

## Development Phases

### Phase 1: MVP (Minimum Viable Product)
Core commands: init, add, status, sync
Basic safety and backup features
Local git repository management

### Phase 2: Polish and Reliability
Comprehensive error handling
Cross-platform testing
Performance optimization
Documentation and examples

### Phase 3: Advanced Features
Environment profiles (work/personal/server)
Template system for common configurations
Team sharing capabilities
Integration with popular dotfile repositories

## Risk Mitigation
- **Data Loss**: Comprehensive backup system, never modify originals without backup
- **Platform Issues**: Extensive cross-platform testing in CI
- **User Error**: Clear confirmation prompts for destructive operations
- **Complexity Creep**: Strict focus on MVP features first, resist feature bloat

## Project Management System (Meta)
This project uses the Claude Code native project management system:
- **Sub-agents**: project-starter, task-tracker, context-manager, sync-agent
- **Slash commands**: /idea, /tasks, /focus, /sync
- **Context management**: Structured .claude/context/ directory
- **Task tracking**: Built on Claude Code's TodoWrite tool

---
*Last updated: 2025-09-17 - New DotMgr project initiation*