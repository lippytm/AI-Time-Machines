const rateLimit = require('express-rate-limit');

// Enhanced rate limiter with security logging
const createRateLimiterWithLogging = (options, limiterName) => {
  return rateLimit({
    ...options,
    handler: (req, res) => {
      console.warn(`🚨 Rate limit exceeded for ${limiterName}:`, {
        ip: req.ip,
        path: req.path,
        userAgent: req.get('user-agent'),
        timestamp: new Date().toISOString()
      });
      
      res.status(429).json({
        error: {
          message: options.message,
          code: 'RATE_LIMIT_EXCEEDED',
          retryAfter: res.getHeader('Retry-After')
        }
      });
    }
  });
};

// General API rate limiter
const apiLimiter = createRateLimiterWithLogging({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
}, 'API');

// Strict rate limiter for authentication endpoints
const authLimiter = createRateLimiterWithLogging({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // Limit each IP to 5 login/register requests per windowMs
  message: 'Too many authentication attempts, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
  skipSuccessfulRequests: true, // Don't count successful requests
}, 'Auth');

// Rate limiter for resource creation
const createLimiter = createRateLimiterWithLogging({
  windowMs: 60 * 1000, // 1 minute
  max: 10, // Limit each IP to 10 create requests per minute
  message: 'Too many create requests, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
}, 'Create');

// Aggressive rate limiter for export endpoints
const exportLimiter = createRateLimiterWithLogging({
  windowMs: 60 * 1000, // 1 minute
  max: 5, // Limit each IP to 5 export requests per minute
  message: 'Too many export requests, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
}, 'Export');

// Rate limiter for webhook endpoints
const webhookLimiter = createRateLimiterWithLogging({
  windowMs: 60 * 1000, // 1 minute
  max: 20, // Limit each IP to 20 webhook requests per minute
  message: 'Too many webhook requests, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
}, 'Webhook');

module.exports = {
  apiLimiter,
  authLimiter,
  createLimiter,
  exportLimiter,
  webhookLimiter
};
