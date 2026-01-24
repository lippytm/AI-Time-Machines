# Contributing to AI-Time-Machines

Thank you for considering contributing to AI-Time-Machines! We welcome contributions from everyone.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find that the issue is already reported. When creating a bug report, please include as many details as possible:

- Use a clear and descriptive title
- Describe the steps to reproduce the problem
- Describe the behavior you observed and the behavior you expected
- Include screenshots if applicable
- Include your environment details

### Suggesting Features

Feature suggestions are welcome! Please:

- Use a clear and descriptive title
- Provide a detailed description of the proposed feature
- Explain why this feature would be useful
- Consider providing examples of how the feature would work

### Code Contributions

#### Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/AI-Time-Machines.git`
3. Create a feature branch from `main`: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes (see "Running Tests" below)
6. Commit your changes (see "Commit Messages" below)
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request to the `main` branch

#### Branch and PR Process

- **Base branch**: All PRs should target the `main` branch
- **Branch naming**: Use descriptive names like `feature/add-model-export`, `fix/api-timeout`, `docs/update-readme`
- **Keep PRs focused**: One feature or fix per PR
- **Stay up to date**: Regularly sync your fork with upstream `main`
- **CI must pass**: All automated checks must pass before merging

#### Commit Messages

We use **Conventional Commits** for better release automation. While optional, this is **strongly recommended** as it enables automatic changelog generation and semantic versioning through Release Please.

Format: `type(scope): description`

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

**Examples:**
```
feat(frontend): add time series export to CSV
fix(backend): resolve database connection timeout
docs(readme): update installation instructions
chore(deps): update dependencies
```

#### Code Standards

- Write clear, readable code
- Follow existing code style and patterns
- Include tests for new functionality
- Update documentation as needed
- Keep commits atomic and well-described

#### Pull Request Guidelines

- Fill out the PR template completely
- Link to related issues
- Include tests for new features
- Ensure all checks pass (linting, tests, builds)
- Be responsive to feedback
- Keep the PR scope focused and manageable

### Development Setup

```bash
# Clone the repository
git clone https://github.com/lippytm/AI-Time-Machines.git
cd AI-Time-Machines

# Install all dependencies
npm run install:all

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Start development servers
npm run dev
```

### Running Lint, Test, and Build

#### Linting

**Node.js/JavaScript:**
```bash
# Root and backend/frontend
npm run lint

# Or individually
cd backend && npm run lint
cd frontend && npm run lint
```

**Python:**
```bash
# Install linting tools
pip install ruff mypy

# Run linters
ruff check .
mypy .
```

#### Testing

**Node.js:**
```bash
# Run all tests
npm test

# Backend tests only
cd backend && npm test

# Frontend tests only
cd frontend && npm test
```

**Python:**
```bash
# Install pytest if not already installed
pip install pytest

# Run tests
cd python-service && pytest
```

#### Building

**Full build:**
```bash
npm run build
```

**Individual builds:**
```bash
# Backend
cd backend && npm run build

# Frontend
cd frontend && npm run build
```

**Docker:**
```bash
# Build all services
docker-compose build

# Or build individually
docker build -t ai-timemachines-backend ./backend
docker build -t ai-timemachines-frontend ./frontend
docker build -t ai-timemachines-python ./python-service
```

### Code of Conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

### Questions?

If you have questions, please:
- Check existing [GitHub Discussions](https://github.com/lippytm/AI-Time-Machines/discussions)
- Open a new discussion
- Contact the maintainers

## Recognition

Contributors will be recognized in our README and release notes. We appreciate all contributions, no matter how small!

Thank you for contributing! 🎉