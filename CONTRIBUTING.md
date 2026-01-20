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
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit your changes: `git commit -m "Add your commit message"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

#### Code Standards

- Write clear, readable code
- Follow existing code style and patterns
- Include tests for new functionality
- Update documentation as needed
- Keep commits atomic and well-described

#### Pull Request Guidelines

Before submitting a pull request, ensure you have completed the following:

- Fill out the PR template completely
- Link to related issues using `Fixes #123` or `Closes #456`
- Include tests for new features
- Ensure all CI checks pass (lint, test, security scans)
- Be responsive to feedback and requested changes

#### Pull Request Checklist

Use this checklist when creating a pull request:

- [ ] **Code Quality**
  - [ ] Code follows the project's style guidelines
  - [ ] No linting errors (`npm run lint` passes)
  - [ ] Code is properly formatted
  - [ ] No commented-out code or debug statements
  
- [ ] **Testing**
  - [ ] All existing tests pass (`npm test`)
  - [ ] New tests added for new functionality
  - [ ] Test coverage is maintained or improved
  - [ ] Manual testing performed for UI changes
  
- [ ] **Documentation**
  - [ ] Code changes are documented with comments where necessary
  - [ ] README updated if functionality changed
  - [ ] API documentation updated if endpoints changed
  - [ ] CHANGELOG updated (if applicable)
  
- [ ] **Security**
  - [ ] No sensitive data (API keys, passwords) committed
  - [ ] Security best practices followed
  - [ ] Dependencies reviewed for vulnerabilities
  - [ ] Input validation implemented for user inputs
  
- [ ] **Performance**
  - [ ] No obvious performance regressions
  - [ ] Database queries optimized
  - [ ] Large files or assets properly handled
  
- [ ] **Git Hygiene**
  - [ ] Commits are atomic and well-described
  - [ ] Branch is up-to-date with base branch
  - [ ] No merge conflicts
  - [ ] Commit messages follow conventional format

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

### Running Tests

Testing is a critical part of the development process. Please ensure all tests pass before submitting a PR.

#### Backend Tests

```bash
# Run backend tests
cd backend
npm test

# Run tests with coverage
npm run test:coverage

# Run tests in watch mode
npm run test:watch
```

#### Frontend Tests

```bash
# Run frontend tests
cd frontend
npm test

# Run tests without watch mode (for CI)
npm test -- --watchAll=false

# Run tests with coverage
npm run test:coverage
```

#### Python Tests

```bash
# Run Python tests
cd python-service
pytest

# Run tests with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_app.py
```

#### Integration Tests

```bash
# Run all tests across the stack
npm test

# Run linting across all projects
npm run lint
```

### Linting and Formatting

```bash
# Lint JavaScript/TypeScript
npm run lint

# Lint Python (if configured)
cd python-service
flake8 .
black --check .

# Auto-fix linting issues
npm run lint:fix  # if configured
black .           # for Python formatting
```

### Branch Protection Rules

The `main` branch is protected with the following rules to ensure code quality and security:

#### Required Checks
- ✅ All CI workflows must pass (lint, test, security scans)
- ✅ CodeQL analysis must complete successfully
- ✅ Dependency review must pass (no high/critical vulnerabilities)
- ✅ At least 1 approval from a code owner required

#### Branch Rules
- 🔒 Direct pushes to `main` are not allowed
- 🔒 Force pushes are disabled
- 🔒 Branch deletion is disabled
- 🔒 All conversations must be resolved before merging
- 🔒 Branches must be up to date before merging

#### Workflow
1. Create a feature branch from `main`: `git checkout -b feature/your-feature-name`
2. Make your changes and commit them
3. Push your branch: `git push origin feature/your-feature-name`
4. Open a pull request against `main`
5. Wait for CI checks to pass and get approval from a code owner
6. Address any review comments
7. Once approved and all checks pass, the PR can be merged

See [SECURITY.md](SECURITY.md) for more details on security requirements.

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