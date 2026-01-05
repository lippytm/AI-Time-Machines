const request = require('supertest');
const { app } = require('../src/server');

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
