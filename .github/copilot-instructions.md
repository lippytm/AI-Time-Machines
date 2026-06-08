# AI Time Machines Repository

AI Time Machines is a conceptual repository for adding AI Agents to everything with Time Machines. This repository is currently in early development phase with minimal infrastructure.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Repository Status
- **CRITICAL**: This repository is currently in a minimal state with only basic files (README.md, LICENSE, .git)
- **NO BUILD SYSTEM**: There are no build scripts, package managers, or compilation steps available
- **NO SOURCE CODE**: No implementation files exist yet (.py, .js, .ts, .java, etc.)
- **NO TESTS**: No test infrastructure or test files are present
- **NO CI/CD**: No GitHub workflows or automated build processes exist
- **NO DEPENDENCIES**: No dependency management files (package.json, requirements.txt, etc.)

### Basic Operations
- Bootstrap the repository:
  - `git clone <repository-url>`
  - `cd AI-Time-Machines`
  - `git status` -- confirms clean working directory
  - `git log --oneline -5` -- shows commit history
- Validate repository state:
  - `ls -la` -- shows README.md, LICENSE, .git, and .github directories
  - `find . -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.json"` -- returns no results (no source files)

### Repository Structure
```
AI-Time-Machines/
├── .git/           # Git repository data
├── .github/        # GitHub configuration (created for Copilot instructions)
│   └── copilot-instructions.md
├── LICENSE         # GNU General Public License v3.0
└── README.md       # Basic project description
```

## Validation

### Current State Validation
- **ALWAYS** verify the minimal state before making assumptions about available tools
- The repository currently contains:
  - README.md: Basic description "adding AI Agents to everything with Time Machines"
  - LICENSE: GNU GPL v3.0 license file
  - .git/: Standard git repository metadata
  - .github/: GitHub configuration directory with copilot-instructions.md
- **NO executable code exists** - do not attempt to run, build, or test non-existent applications

### Git Operations
- All standard git operations work correctly:
  - `git status` -- takes <1 second
  - `git log` -- takes <1 second  
  - `git add .` -- takes <1 second
  - `git commit -m "message"` -- takes <1 second
  - `git push` -- takes 5-10 seconds depending on network

## Common Tasks

### Current Limitations
- **Cannot build**: No build system exists
- **Cannot test**: No test framework or tests exist
- **Cannot run**: No executable code exists
- **Cannot install dependencies**: No dependency files exist
- **Cannot lint**: No linting configuration exists

### Future Development Setup
When development begins, typical AI/ML projects in this domain might include:
- Python with requirements.txt or pyproject.toml
- Node.js with package.json for web interfaces
- Docker containers for deployment
- GitHub Actions for CI/CD
- Test frameworks like pytest, jest, or similar
- Linting tools like pylint, eslint, or pre-commit hooks

### Repository Information Cache
The following are outputs from frequently run commands. Reference them instead of running bash commands to save time.

#### Repository Root Contents
```bash
$ ls -la
total 56
drwxr-xr-x 4 runner docker  4096 Sep  1 19:31 .
drwxr-xr-x 3 runner docker  4096 Sep  1 19:28 ..
drwxr-xr-x 7 runner docker  4096 Sep  1 19:32 .git
drwxr-xr-x 2 runner docker  4096 Sep  1 19:32 .github
-rw-r--r-- 1 runner docker 35149 Sep  1 19:28 LICENSE
-rw-r--r-- 1 runner docker    70 Sep  1 19:28 README.md
```

#### README Content
```bash
$ cat README.md
# AI-Time-Machines
adding AI Agents to everything with Time Machines
```

#### Git Status
```bash
$ git status
On branch copilot/fix-11
Your branch is up to date with 'origin/copilot/fix-11'.

nothing to commit, working tree clean
```

#### Project File Search Results
```bash
$ find . -name "*.json" -o -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.yaml" -o -name "*.yml"
# No results - no project files exist yet
```

## Key Project Context

### Project Vision
- Focus: Adding AI Agents to everything with Time Machines concept
- Current State: Conceptual/planning phase
- License: GNU General Public License v3.0
- Development Stage: Pre-implementation

### Related Issues
- Issue #11: Set up Copilot instructions (this file)
- Issue #2: GitHub copilot connections need to be added with AI Agents, AI Engines, AI Chat bots
- Issue #1: Connect with GitHub Copilot

### Working Notes
- The repository name suggests integration of AI agents with temporal/historical data concepts
- Future development likely to involve AI/ML frameworks, time-series data, or historical simulation
- When adding new code, consider the project's theme of AI agents and time-related functionality
- Always check for updates to this instructions file as the project evolves from its current minimal state