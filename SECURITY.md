# Security Policy

## Supported Versions

We actively support the following versions of AI-Time-Machines with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 2.x     | :white_check_mark: |
| 1.x     | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability in AI-Time-Machines, please report it responsibly.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report vulnerabilities by:
- Opening a [private security advisory](https://github.com/lippytm/AI-Time-Machines/security/advisories/new)
- Contacting the maintainer: [@lippytm](https://github.com/lippytm)

Please include the following information in your report:
- Type of vulnerability
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if available)
- Impact of the vulnerability, including how an attacker might exploit it

### What to Expect

When you report a vulnerability, you can expect the following response timeline:

| Stage | Timeline (SLA) |
| ----- | -------------- |
| **Initial Response** | Within 48 hours |
| **Vulnerability Assessment** | Within 5 business days |
| **Fix Development** | Varies based on severity |
| **Security Patch Release** | Within 30 days for high/critical issues |
| **Public Disclosure** | After patch is released and users have time to update |

**Note**: These are target timelines and may vary based on the complexity and severity of the issue.

### Vulnerability Severity

We classify vulnerabilities using the following severity levels:

- **Critical**: Immediate action required (e.g., remote code execution, authentication bypass)
- **High**: Should be addressed urgently (e.g., SQL injection, XSS, sensitive data exposure)
- **Medium**: Should be addressed in next release (e.g., CSRF, information disclosure)
- **Low**: Can be addressed in future releases (e.g., minor information leaks)

### Security Update Process

1. **Assessment**: Security team reviews and confirms the vulnerability
2. **Development**: Fix is developed in a private repository branch
3. **Testing**: Fix is thoroughly tested for effectiveness and side effects
4. **Release**: Security patch is released as a new version
5. **Notification**: Security advisory is published with CVE (if applicable)
6. **Disclosure**: Full details are disclosed after users have had time to update

## Security Best Practices

When using AI-Time-Machines, please follow these security best practices:

### Environment Variables
- **Never commit secrets** to version control
- Use `.env.example` as a template and create your own `.env` file
- Store sensitive credentials in secure secret management systems
- Rotate credentials regularly

### Required Secrets Configuration

The following secrets should be configured in your deployment environment:

| Secret | Purpose | Required For |
| ------ | ------- | ------------ |
| `DB_URL` | Database connection string | Backend |
| `JWT_SECRET` | JWT token signing key | Authentication |
| `OPENAI_API_KEY` | OpenAI API access | AI features |
| `WEB3_RPC_URL` | Web3 RPC endpoint | Blockchain features (optional) |
| `SLACK_BOT_TOKEN` | Slack integration | Notifications (optional) |
| `DISCORD_BOT_TOKEN` | Discord integration | Notifications (optional) |
| `S3_BUCKET` | AWS S3 bucket name | File storage (optional) |

### Authentication & Authorization
- Use strong passwords (minimum 12 characters)
- Enable multi-factor authentication when available
- Review and audit user permissions regularly
- Implement rate limiting to prevent brute force attacks

### Database Security
- Use parameterized queries (Sequelize ORM protects against SQL injection)
- Encrypt sensitive data at rest
- Use SSL/TLS for database connections in production
- Regularly backup your database

### API Security
- Always use HTTPS in production
- Implement proper CORS configuration
- Validate and sanitize all user inputs
- Use helmet.js for security headers (already included)

### Dependency Management
- Regularly update dependencies to patch security vulnerabilities
- Use `npm audit` to check for known vulnerabilities
- Review dependency-review action results on pull requests
- Use automated tools like Dependabot for dependency updates

### Docker Security
- Don't run containers as root
- Use official base images from trusted sources
- Scan images for vulnerabilities with Trivy (included in CI)
- Keep base images updated

## Security Features

AI-Time-Machines includes the following security features:

- ✅ JWT-based authentication with bcrypt password hashing
- ✅ Helmet.js for security headers
- ✅ CORS configuration
- ✅ Input validation with express-validator
- ✅ SQL injection protection via Sequelize ORM
- ✅ Regular security scanning with Trivy
- ✅ CodeQL security analysis
- ✅ Dependency vulnerability scanning
- ✅ Environment variable management

## Branch Protection Rules

The `main` branch is protected with the following rules:

- **Require pull request reviews**: At least 1 approval required
- **Require status checks**: CI must pass before merging
- **Require branches to be up to date**: Must be current with base branch
- **Require conversation resolution**: All comments must be resolved
- **Restrict force pushes**: Force pushes are not allowed
- **Restrict deletions**: Branch cannot be deleted

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details on the development workflow.

## Compliance & Privacy

- **Data Privacy**: Review our data handling practices in the documentation
- **License Compliance**: This project is licensed under GPL-3.0 (see [LICENSE](LICENSE))
- **Third-party Services**: Review privacy policies of integrated services (OpenAI, etc.)

## Security Advisories

Security advisories will be published at:
- GitHub Security Advisories: https://github.com/lippytm/AI-Time-Machines/security/advisories
- Repository Releases: https://github.com/lippytm/AI-Time-Machines/releases

## Contact

For security-related questions or concerns:
- GitHub Security Advisories: https://github.com/lippytm/AI-Time-Machines/security/advisories
- Maintainer: [@lippytm](https://github.com/lippytm)

## Acknowledgments

We appreciate responsible disclosure of security vulnerabilities and will acknowledge security researchers who report issues responsibly.

---

**Last Updated**: 2026-01-20
