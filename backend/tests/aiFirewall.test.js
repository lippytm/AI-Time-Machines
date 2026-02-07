const {
  validateUrlPattern,
  detectSqlInjection,
  detectXss,
  validateRequestBody,
  aiFirewall,
  sqlInjectionProtection,
  validateUrlParams
} = require('../src/middleware/aiFirewall');

describe('AI Firewall Middleware', () => {
  describe('validateUrlPattern', () => {
    test('should accept valid HTTP URLs', () => {
      expect(validateUrlPattern('http://example.com')).toBe(true);
      expect(validateUrlPattern('https://example.com/path')).toBe(true);
      expect(validateUrlPattern('https://example.com/path?query=value')).toBe(true);
    });

    test('should reject invalid URLs', () => {
      expect(validateUrlPattern('not-a-url')).toBe(false);
      expect(validateUrlPattern('ftp://example.com')).toBe(false);
      expect(validateUrlPattern('')).toBe(false);
      expect(validateUrlPattern(null)).toBe(false);
    });

    test('should reject dangerous URL patterns', () => {
      expect(validateUrlPattern('javascript:alert(1)')).toBe(false);
      expect(validateUrlPattern('data:text/html,<script>alert(1)</script>')).toBe(false);
      expect(validateUrlPattern('vbscript:msgbox(1)')).toBe(false);
      expect(validateUrlPattern('file:///etc/passwd')).toBe(false);
    });

    test('should reject path traversal attempts', () => {
      expect(validateUrlPattern('http://example.com/../../etc/passwd')).toBe(false);
      expect(validateUrlPattern('http://example.com/%2e%2e/secret')).toBe(false);
    });

    test('should reject XSS attempts in URLs', () => {
      expect(validateUrlPattern('http://example.com/<script>alert(1)</script>')).toBe(false);
      expect(validateUrlPattern('http://example.com/page?param=<script>alert(1)</script>')).toBe(false);
    });
  });

  describe('detectSqlInjection', () => {
    test('should detect SQL injection patterns', () => {
      expect(detectSqlInjection("' OR '1'='1")).toBe(true);
      expect(detectSqlInjection("admin'--")).toBe(true);
      expect(detectSqlInjection("1; DROP TABLE users")).toBe(true);
      expect(detectSqlInjection("1 UNION SELECT * FROM users")).toBe(true);
      expect(detectSqlInjection("1 AND 1=1")).toBe(true);
    });

    test('should detect SQL comment patterns', () => {
      expect(detectSqlInjection("test--comment")).toBe(true);
      expect(detectSqlInjection("test/*comment*/")).toBe(true);
      expect(detectSqlInjection("test#comment")).toBe(true);
    });

    test('should detect timing attack patterns', () => {
      expect(detectSqlInjection("1; SLEEP(5)")).toBe(true);
      expect(detectSqlInjection("1; WAITFOR DELAY '00:00:05'")).toBe(true);
      expect(detectSqlInjection("BENCHMARK(1000000,MD5('test'))")).toBe(true);
    });

    test('should detect EXEC and EXECUTE patterns', () => {
      expect(detectSqlInjection("EXEC('SELECT * FROM users')")).toBe(true);
      expect(detectSqlInjection("EXEC sp_executesql")).toBe(true);
      expect(detectSqlInjection("EXECUTE IMMEDIATE 'DROP TABLE users'")).toBe(true);
    });

    test('should allow normal input', () => {
      expect(detectSqlInjection("normal text")).toBe(false);
      expect(detectSqlInjection("user@example.com")).toBe(false);
      expect(detectSqlInjection("john's data")).toBe(false);
      expect(detectSqlInjection("test-value")).toBe(false);
    });

    test('should handle edge cases', () => {
      expect(detectSqlInjection(null)).toBe(false);
      expect(detectSqlInjection('')).toBe(false);
      expect(detectSqlInjection(123)).toBe(false);
    });
  });

  describe('detectXss', () => {
    test('should detect script tags', () => {
      expect(detectXss('<script>alert(1)</script>')).toBe(true);
      expect(detectXss('<SCRIPT>alert(1)</SCRIPT>')).toBe(true);
      expect(detectXss('<script src="evil.js"></script>')).toBe(true);
    });

    test('should detect event handlers', () => {
      expect(detectXss('<img onerror="alert(1)">')).toBe(true);
      expect(detectXss('<div onclick="alert(1)">test</div>')).toBe(true);
      expect(detectXss('<body onload="alert(1)">')).toBe(true);
    });

    test('should detect dangerous tags', () => {
      expect(detectXss('<iframe src="evil.com"></iframe>')).toBe(true);
      expect(detectXss('<object data="evil.swf"></object>')).toBe(true);
      expect(detectXss('<embed src="evil.swf">')).toBe(true);
    });

    test('should detect javascript: protocol', () => {
      expect(detectXss('javascript:alert(1)')).toBe(true);
      expect(detectXss('vbscript:msgbox(1)')).toBe(true);
    });

    test('should allow normal HTML entities and text', () => {
      expect(detectXss('normal text')).toBe(false);
      expect(detectXss('text with <b>bold</b>')).toBe(false);
      expect(detectXss('text with &lt;escaped&gt;')).toBe(false);
    });

    test('should handle edge cases', () => {
      expect(detectXss(null)).toBe(false);
      expect(detectXss('')).toBe(false);
      expect(detectXss(123)).toBe(false);
    });
  });

  describe('validateRequestBody', () => {
    test('should detect SQL injection in body fields', () => {
      const body = {
        username: "admin'--",
        email: 'test@example.com'
      };
      const errors = validateRequestBody(body);
      expect(errors.length).toBeGreaterThan(0);
      expect(errors[0].threat).toBe('sql_injection');
    });

    test('should detect XSS in body fields', () => {
      const body = {
        comment: '<script>alert(1)</script>',
        name: 'John'
      };
      const errors = validateRequestBody(body);
      expect(errors.length).toBeGreaterThan(0);
      expect(errors[0].threat).toBe('xss');
    });

    test('should validate nested objects', () => {
      const body = {
        user: {
          name: 'John',
          bio: '<script>alert(1)</script>'
        }
      };
      const errors = validateRequestBody(body);
      expect(errors.length).toBeGreaterThan(0);
      expect(errors[0].field).toContain('bio');
    });

    test('should validate arrays', () => {
      const body = {
        items: ['normal', "' OR '1'='1", 'safe']
      };
      const errors = validateRequestBody(body);
      expect(errors.length).toBeGreaterThan(0);
      expect(errors[0].field).toContain('[1]');
    });

    test('should return empty array for clean data', () => {
      const body = {
        username: 'johndoe',
        email: 'john@example.com',
        age: 25
      };
      const errors = validateRequestBody(body);
      expect(errors).toEqual([]);
    });
  });

  describe('aiFirewall middleware', () => {
    let req, res, next;

    beforeEach(() => {
      req = {
        method: 'POST',
        path: '/api/test',
        ip: '127.0.0.1',
        get: jest.fn().mockReturnValue('Test User Agent'),
        query: {},
        body: {}
      };
      res = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn()
      };
      next = jest.fn();
    });

    test('should allow clean requests', () => {
      req.body = { name: 'John', email: 'john@example.com' };
      aiFirewall(req, res, next);
      expect(next).toHaveBeenCalled();
      expect(res.status).not.toHaveBeenCalled();
    });

    test('should block requests with SQL injection', () => {
      req.body = { search: "' OR '1'='1" };
      aiFirewall(req, res, next);
      expect(res.status).toHaveBeenCalledWith(403);
      expect(res.json).toHaveBeenCalledWith(
        expect.objectContaining({
          error: expect.objectContaining({
            code: 'SECURITY_VIOLATION'
          })
        })
      );
      expect(next).not.toHaveBeenCalled();
    });

    test('should block requests with XSS', () => {
      req.body = { comment: '<script>alert(1)</script>' };
      aiFirewall(req, res, next);
      expect(res.status).toHaveBeenCalledWith(403);
      expect(next).not.toHaveBeenCalled();
    });

    test('should validate URL parameters', () => {
      req.query = { redirectUrl: 'javascript:alert(1)' };
      aiFirewall(req, res, next);
      expect(res.status).toHaveBeenCalledWith(403);
      expect(next).not.toHaveBeenCalled();
    });
  });

  describe('sqlInjectionProtection middleware', () => {
    let req, res, next;

    beforeEach(() => {
      req = {
        query: {},
        body: {}
      };
      res = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn()
      };
      next = jest.fn();
    });

    test('should allow clean requests', () => {
      req.body = { search: 'normal search' };
      sqlInjectionProtection(req, res, next);
      expect(next).toHaveBeenCalled();
    });

    test('should block SQL injection in body', () => {
      req.body = { search: "1' OR '1'='1" };
      sqlInjectionProtection(req, res, next);
      expect(res.status).toHaveBeenCalledWith(403);
      expect(res.json).toHaveBeenCalledWith(
        expect.objectContaining({
          error: expect.objectContaining({
            code: 'SQL_INJECTION_DETECTED'
          })
        })
      );
    });

    test('should block SQL injection in query params', () => {
      req.query = { id: "1; DROP TABLE users" };
      sqlInjectionProtection(req, res, next);
      expect(res.status).toHaveBeenCalledWith(403);
    });
  });

  describe('validateUrlParams middleware', () => {
    let req, res, next;

    beforeEach(() => {
      req = {
        query: {},
        body: {}
      };
      res = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn()
      };
      next = jest.fn();
    });

    test('should validate specified URL parameters', () => {
      const middleware = validateUrlParams(['webhookUrl']);
      req.body = { webhookUrl: 'https://example.com/webhook' };
      middleware(req, res, next);
      expect(next).toHaveBeenCalled();
    });

    test('should reject invalid URLs', () => {
      const middleware = validateUrlParams(['webhookUrl']);
      req.body = { webhookUrl: 'javascript:alert(1)' };
      middleware(req, res, next);
      expect(res.status).toHaveBeenCalledWith(400);
      expect(res.json).toHaveBeenCalledWith(
        expect.objectContaining({
          error: expect.objectContaining({
            code: 'INVALID_URL'
          })
        })
      );
    });

    test('should allow requests without specified parameters', () => {
      const middleware = validateUrlParams(['webhookUrl']);
      req.body = { name: 'test' };
      middleware(req, res, next);
      expect(next).toHaveBeenCalled();
    });
  });
});
