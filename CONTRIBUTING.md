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

#### Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/) to automate version management and CHANGELOG generation with [release-please](https://github.com/googleapis/release-please).

**Commit message format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature (triggers minor version bump)
- `fix`: Bug fix (triggers patch version bump)
- `docs`: Documentation changes
- `style`: Code style changes (formatting, semicolons, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `build`: Build system changes
- `ci`: CI/CD configuration changes
- `chore`: Other changes that don't modify src or test files

**Examples:**
```
feat(backend): add user authentication endpoint
fix(frontend): resolve login form validation issue
docs: update README with new API endpoints
```

**Breaking Changes:**
Add `!` after the type/scope and include `BREAKING CHANGE:` in the footer:
```
feat(api)!: change user endpoint response format

BREAKING CHANGE: user endpoint now returns data in a different structure
```

#### Pull Request Guidelines

- Fill out the PR template completely
- Link to related issues
- Include tests for new features
- Ensure all checks pass
- Be responsive to feedback

### Development Setup

```bash
# Clone the repository
git clone https://github.com/lippytm/AI-Time-Machines.git
cd AI-Time-Machines

# Install dependencies (if applicable)
npm install

# Run tests (if applicable)
npm test

# Run the application (if applicable)
npm start
```

### Running Linters, Tests, and Builds

**Backend:**
```bash
cd backend
npm install
npm run lint    # Run ESLint
npm test        # Run tests
npm run build   # Build the backend
```

**Frontend:**
```bash
cd frontend
npm install
npm run lint    # Run ESLint
npm test        # Run tests
npm run build   # Build the frontend for production
```

**Python Service:**
```bash
cd python-service
pip install -r requirements.txt
pip install ruff mypy pytest

ruff check .    # Run linting with ruff
mypy .          # Run type checking (if pyproject.toml exists)
pytest          # Run tests
```

**Docker:**
```bash
# Build and run all services
docker-compose up --build

# Run individual service builds
docker build ./backend
docker build ./frontend
docker build ./python-service
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