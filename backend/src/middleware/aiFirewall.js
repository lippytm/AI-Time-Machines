// AI Firewall Middleware
// Implements real-time validation for URL & request patterns, rate limiting, and security controls

const validator = require('validator');

/**
 * URL Pattern Validation
 * Validates and sanitizes URLs to prevent malicious patterns
 */
function validateUrlPattern(url) {
  if (!url || typeof url !== 'string') {
    return false;
  }

  // Check for valid URL format
  if (!validator.isURL(url, { 
    protocols: ['http', 'https'], 
    require_protocol: true,
    require_valid_protocol: true,
    allow_underscores: false
  })) {
    return false;
  }

  // Prevent common attack patterns
  const dangerousPatterns = [
    /javascript:/i,
    /data:/i,
    /vbscript:/i,
    /file:/i,
    /<script/i,
    /onerror=/i,
    /onclick=/i,
    /\.\.\/\.\.\//,  // Path traversal
    /%2e%2e/i,       // Encoded path traversal
    /\x00/,          // Null byte
  ];

  for (const pattern of dangerousPatterns) {
    if (pattern.test(url)) {
      return false;
    }
  }

  return true;
}

/**
 * SQL Injection Detection
 * Detects potential SQL injection patterns in input
 */
function detectSqlInjection(input) {
  if (!input || typeof input !== 'string') {
    return false;
  }

  const sqlPatterns = [
    /(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE|UNION|DECLARE)\b)/i,
    /(EXEC\s*\(|EXECUTE\s+IMMEDIATE)/i,  // EXEC() and EXECUTE IMMEDIATE patterns
    /(--|#|\/\*|\*\/)/,  // SQL comments
    /;.*(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)\b)/i,  // Semicolon followed by SQL keyword
    /(\bOR\b|\bAND\b)\s+\d+\s*=\s*\d+/i,  // OR 1=1, AND 1=1
    /(\bOR\b|\bAND\b)\s+['"]\w+['"]\s*=\s*['"]\w+['"]/i,  // OR 'a'='a'
    /'\s*(\bOR\b|\bAND\b)/i,  // ' OR, ' AND
    /SLEEP\s*\(/i,
    /BENCHMARK\s*\(/i,
    /WAITFOR\s+DELAY/i,
  ];

  for (const pattern of sqlPatterns) {
    if (pattern.test(input)) {
      return true;
    }
  }

  return false;
}

/**
 * XSS Detection
 * Detects potential cross-site scripting patterns
 */
function detectXss(input) {
  if (!input || typeof input !== 'string') {
    return false;
  }

  const xssPatterns = [
    /<script[\s\S]*?>[\s\S]*?<\/script>/i,
    /<iframe[\s\S]*?>/i,
    /<object[\s\S]*?>/i,
    /<embed[\s\S]*?>/i,
    /on\w+\s*=\s*["'][^"']*["']/i,  // Event handlers
    /javascript:/i,
    /vbscript:/i,
    /<img[\s\S]*?onerror[\s\S]*?>/i,
  ];

  for (const pattern of xssPatterns) {
    if (pattern.test(input)) {
      return true;
    }
  }

  return false;
}

/**
 * Validate request body for security threats
 */
function validateRequestBody(body) {
  const errors = [];

  function checkValue(value, path = '') {
    if (typeof value === 'string') {
      if (detectSqlInjection(value)) {
        errors.push({ field: path, threat: 'sql_injection', value: value.substring(0, 50) });
      }
      if (detectXss(value)) {
        errors.push({ field: path, threat: 'xss', value: value.substring(0, 50) });
      }
    } else if (Array.isArray(value)) {
      value.forEach((item, index) => {
        checkValue(item, `${path}[${index}]`);
      });
    } else if (typeof value === 'object' && value !== null) {
      Object.keys(value).forEach(key => {
        checkValue(value[key], path ? `${path}.${key}` : key);
      });
    }
  }

  if (body) {
    checkValue(body);
  }

  return errors;
}

/**
 * AI Firewall Middleware
 * Main middleware function for request validation
 */
const aiFirewall = (req, res, next) => {
  const securityLog = {
    timestamp: new Date().toISOString(),
    method: req.method,
    path: req.path,
    ip: req.ip,
    userAgent: req.get('user-agent'),
    threats: []
  };

  // Validate URLs in query parameters
  if (req.query) {
    Object.entries(req.query).forEach(([key, value]) => {
      if (typeof value === 'string' && (key.toLowerCase().includes('url') || key.toLowerCase().includes('redirect'))) {
        if (!validateUrlPattern(value)) {
          securityLog.threats.push({ type: 'invalid_url', field: key, value });
        }
      }
    });
  }

  // Validate request body
  if (req.body && Object.keys(req.body).length > 0) {
    const bodyThreats = validateRequestBody(req.body);
    if (bodyThreats.length > 0) {
      securityLog.threats.push(...bodyThreats);
    }
  }

  // Log security events if threats detected
  if (securityLog.threats.length > 0) {
    console.warn('🔒 Security threat detected:', JSON.stringify(securityLog, null, 2));
    
    return res.status(403).json({
      error: {
        message: 'Request blocked by security firewall',
        code: 'SECURITY_VIOLATION',
        details: 'Your request contains potentially malicious content'
      }
    });
  }

  next();
};

/**
 * URL validation middleware for specific parameters
 */
const validateUrlParams = (paramNames = []) => {
  return (req, res, next) => {
    const params = { ...req.query, ...req.body };
    
    for (const paramName of paramNames) {
      if (params[paramName]) {
        if (!validateUrlPattern(params[paramName])) {
          return res.status(400).json({
            error: {
              message: `Invalid URL in parameter: ${paramName}`,
              code: 'INVALID_URL'
            }
          });
        }
      }
    }
    
    next();
  };
};

/**
 * SQL injection protection middleware
 */
const sqlInjectionProtection = (req, res, next) => {
  const params = { ...req.query, ...req.body };
  
  for (const [key, value] of Object.entries(params)) {
    if (typeof value === 'string' && detectSqlInjection(value)) {
      console.warn(`🔒 SQL injection attempt detected in ${key}:`, value);
      return res.status(403).json({
        error: {
          message: 'Request blocked: SQL injection detected',
          code: 'SQL_INJECTION_DETECTED'
        }
      });
    }
  }
  
  next();
};

module.exports = {
  aiFirewall,
  validateUrlPattern,
  validateUrlParams,
  sqlInjectionProtection,
  detectSqlInjection,
  detectXss,
  validateRequestBody
};
