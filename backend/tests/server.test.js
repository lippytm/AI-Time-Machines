const request = require('supertest');
const { app, server } = require('../src/server');

afterAll((done) => {
  server.close(done);
});

describe('Server Health Check', () => {
  test('GET /health should return healthy status', async () => {
    const response = await request(app).get('/health');
    
    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('status', 'healthy');
    expect(response.body).toHaveProperty('service');
    expect(response.body).toHaveProperty('timestamp');
  });

  test('GET /nonexistent should return 404', async () => {
    const response = await request(app).get('/nonexistent');
    
    expect(response.status).toBe(404);
    expect(response.body).toHaveProperty('error');
  });
});

describe('Aggregate Status Endpoint', () => {
  test('GET /api/status should return backend status', async () => {
    const response = await request(app).get('/api/status');

    // Status may be degraded when python service is unreachable in test env
    expect([200, 503]).toContain(response.status);
    expect(response.body).toHaveProperty('backend');
    expect(response.body.backend).toHaveProperty('status', 'healthy');
    expect(response.body.backend).toHaveProperty('uptime');
    expect(response.body).toHaveProperty('pythonService');
    expect(response.body).toHaveProperty('timestamp');
    expect(response.body).toHaveProperty('overall');
  });
});
