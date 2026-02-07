# AI Firewall Configuration Guide

## Overview

The AI Firewall is a comprehensive security middleware system that provides real-time validation for URL patterns, request validation, SQL injection detection, and rate limiting across all API endpoints.

## Features

### 1. URL Pattern Validation
- Validates URLs to ensure they use safe protocols (HTTP/HTTPS only)
- Blocks dangerous patterns like `javascript:`, `data:`, `vbscript:`, `file:`
- Prevents path traversal attacks
- Detects encoded path traversal attempts
- Prevents XSS attempts in URLs

### 2. SQL Injection Detection
Detects and blocks common SQL injection patterns including:
- SQL keywords (SELECT, INSERT, UPDATE, DELETE, DROP, etc.)
- SQL comments (`--`, `#`, `/* */`)
- SQL metacharacters and operators
- Boolean-based injection (`OR 1=1`, `AND 'a'='a'`)
- Time-based attacks (SLEEP, WAITFOR, BENCHMARK)

### 3. XSS Detection
Identifies cross-site scripting attempts:
- Script tags
- Event handlers (onclick, onerror, onload, etc.)
- Dangerous tags (iframe, object, embed)
- JavaScript protocol handlers
- VBScript protocol handlers

### 4. Rate Limiting
Multiple rate limiters for different endpoint types:
- **API Limiter**: 100 requests per 15 minutes (general endpoints)
- **Auth Limiter**: 5 requests per 15 minutes (authentication endpoints)
- **Create Limiter**: 10 requests per minute (resource creation)
- **Export Limiter**: 5 requests per minute (data export)
- **Webhook Limiter**: 20 requests per minute (webhook endpoints)

## Implementation

### Backend Integration

The AI Firewall is integrated into the Express server middleware stack:

```javascript
const { aiFirewall, sqlInjectionProtection } = require('./middleware/aiFirewall');
const { apiLimiter } = require('./middleware/rateLimiter');

// Apply security middleware
app.use(aiFirewall);
app.use(sqlInjectionProtection);
app.use('/api/', apiLimiter);
```

### Route-Specific Protection

Routes can apply additional validation:

```javascript
const { validateUrlParams } = require('../middleware/aiFirewall');
const { webhookLimiter } = require('../middleware/rateLimiter');

// Webhook endpoint with specific rate limiting
router.post('/webhooks/:platform', webhookLimiter, receiveWebhook);

// Integration creation with URL validation
router.post('/', 
  createLimiter,
  validateUrlParams(['webhookUrl']),
  createIntegration
);
```

## Security Event Logging

When threats are detected, the AI Firewall logs comprehensive security events:

```json
{
  "timestamp": "2026-02-07T16:50:00.000Z",
  "method": "POST",
  "path": "/api/users",
  "ip": "192.168.1.1",
  "userAgent": "Mozilla/5.0...",
  "threats": [
    {
      "type": "sql_injection",
      "field": "username",
      "value": "admin'--"
    }
  ]
}
```

## Response Codes

### 400 Bad Request
Returned when URL validation fails for specific parameters:
```json
{
  "error": {
    "message": "Invalid URL in parameter: webhookUrl",
    "code": "INVALID_URL"
  }
}
```

### 403 Forbidden
Returned when security threats are detected:
```json
{
  "error": {
    "message": "Request blocked by security firewall",
    "code": "SECURITY_VIOLATION",
    "details": "Your request contains potentially malicious content"
  }
}
```

For SQL injection detection:
```json
{
  "error": {
    "message": "Request blocked: SQL injection detected",
    "code": "SQL_INJECTION_DETECTED"
  }
}
```

### 429 Too Many Requests
Returned when rate limits are exceeded:
```json
{
  "error": {
    "message": "Too many requests from this IP, please try again later.",
    "code": "RATE_LIMIT_EXCEEDED",
    "retryAfter": "900"
  }
}
```

## Best Practices

### 1. Parameterized Queries
Always use parameterized queries for database operations:

```javascript
// ✅ GOOD - Parameterized query
const user = await User.findOne({ 
  where: { username: req.body.username } 
});

// ❌ BAD - String concatenation
const query = `SELECT * FROM users WHERE username = '${req.body.username}'`;
```

### 2. Input Validation
Validate and sanitize all user input:

```javascript
const { body, validationResult } = require('express-validator');

router.post('/',
  [
    body('email').isEmail().normalizeEmail(),
    body('name').trim().isLength({ min: 1, max: 255 }),
    body('webhookUrl').optional().isURL()
  ],
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    // Process request
  }
);
```

### 3. URL Validation
Always validate URLs before using them:

```javascript
const { validateUrlParams } = require('../middleware/aiFirewall');

// Validate specific URL parameters
router.post('/redirect', 
  validateUrlParams(['redirectUrl', 'callbackUrl']),
  handleRedirect
);
```

### 4. Rate Limiting
Apply appropriate rate limits based on endpoint sensitivity:

```javascript
const { authLimiter, createLimiter } = require('../middleware/rateLimiter');

// Strict limit for authentication
router.post('/login', authLimiter, loginHandler);

// Moderate limit for resource creation
router.post('/resources', createLimiter, createHandler);
```

## Configuration Options

### Customizing Rate Limits

Edit `/backend/src/middleware/rateLimiter.js`:

```javascript
const apiLimiter = createRateLimiterWithLogging({
  windowMs: 15 * 60 * 1000,  // Time window
  max: 100,                   // Max requests per window
  message: 'Custom message',  // Error message
  standardHeaders: true,      // Send rate limit info in headers
  legacyHeaders: false,
  skipSuccessfulRequests: false, // Count all requests
}, 'API');
```

### Customizing Threat Detection

Edit `/backend/src/middleware/aiFirewall.js` to add custom patterns:

```javascript
// Add custom SQL injection patterns
const sqlPatterns = [
  /your-custom-pattern/i,
  // ... existing patterns
];

// Add custom XSS patterns
const xssPatterns = [
  /your-custom-pattern/i,
  // ... existing patterns
];
```

## Testing

Run the AI Firewall test suite:

```bash
cd backend
npm test -- aiFirewall.test.js
```

### Test Coverage
- URL pattern validation
- SQL injection detection
- XSS detection
- Request body validation
- Middleware integration
- Rate limiting

## Monitoring

Security events are logged to the console with a 🔒 emoji prefix:

```
🔒 Security threat detected: {
  "timestamp": "2026-02-07T16:50:00.000Z",
  "threats": [...]
}
```

Rate limit violations are logged with a 🚨 emoji:

```
🚨 Rate limit exceeded for Auth: {
  "ip": "192.168.1.1",
  "path": "/api/auth/login"
}
```

## CI/CD Integration

The AI Firewall is automatically tested in the CI pipeline:

- CodeQL security analysis
- SQL injection vulnerability scanning
- Security test execution
- AI-driven diagnostics

See `.github/workflows/ci.yml` and `.github/workflows/reusable-security-pipeline.yml` for details.

## Export Capabilities

The system supports multiple export formats with built-in security:

- **JSON**: Standard JSON format with proper escaping
- **CSV**: CSV format with proper field escaping
- **XML**: XML format with XML entity escaping
- **ManyChat**: Facebook Messenger chatbot format
- **BotBuilders**: Multi-platform chatbot format
- **OpenClaw**: Analytics platform format
- **Moltbook**: Interactive notebook format

All exports are subject to rate limiting via the `exportLimiter`.

## Migration Guide

### For Existing Repositories

1. Copy middleware files:
   - `/backend/src/middleware/aiFirewall.js`
   - `/backend/src/middleware/rateLimiter.js` (updated version)

2. Update `package.json` dependencies:
   ```json
   "validator": "^13.15.22"
   ```

3. Update `server.js` to include middleware:
   ```javascript
   const { aiFirewall, sqlInjectionProtection } = require('./middleware/aiFirewall');
   app.use(aiFirewall);
   app.use(sqlInjectionProtection);
   ```

4. Update routes to use enhanced rate limiting and validation

5. Copy workflow files:
   - `.github/workflows/reusable-security-pipeline.yml`

6. Update existing CI workflow to include CodeQL

7. Run tests to ensure compatibility

## Support

For issues or questions:
- Review the test suite in `/backend/tests/aiFirewall.test.js`
- Check CI/CD logs for security diagnostics
- Review security event logs in application output
