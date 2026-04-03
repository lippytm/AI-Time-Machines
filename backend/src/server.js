require('dotenv').config({ path: '../.env' });
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const axios = require('axios');

const authRoutes = require('./routes/auth');
const timeSeriesRoutes = require('./routes/timeSeries');
const modelsRoutes = require('./routes/models');
const predictionsRoutes = require('./routes/predictions');
const aiToolsRoutes = require('./routes/aiTools');
const integrationsRoutes = require('./routes/integrations');

const app = express();

// Security middleware
app.use(helmet());

// CORS configuration
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
  credentials: true
}));

// Body parsing middleware - capture raw body for webhook signature verification
app.use(express.json({
  verify: (req, _res, buf) => {
    req.rawBody = buf.toString('utf8');
  }
}));
app.use(express.urlencoded({ extended: true }));

// Logging middleware
if (process.env.NODE_ENV !== 'test') {
  app.use(morgan('dev'));
}

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ 
    status: 'healthy', 
    service: 'AI Time Machines Backend',
    timestamp: new Date().toISOString()
  });
});

// Aggregate status endpoint for autonomous monitoring
app.get('/api/status', async (req, res) => {
  const PYTHON_SERVICE_URL = process.env.PYTHON_SERVICE_URL || 'http://localhost:8000';
  const checks = {
    backend: { status: 'healthy', uptime: process.uptime() },
    pythonService: { status: 'unknown' },
    timestamp: new Date().toISOString()
  };

  try {
    const pyResp = await axios.get(`${PYTHON_SERVICE_URL}/health`, { timeout: 3000 });
    checks.pythonService = { status: 'healthy', details: pyResp.data };
  } catch {
    checks.pythonService = { status: 'unreachable' };
  }

  const allHealthy = Object.values(checks)
    .filter(v => typeof v === 'object' && v.status)
    .every(v => v.status === 'healthy');

  res.status(allHealthy ? 200 : 503).json({ ...checks, overall: allHealthy ? 'healthy' : 'degraded' });
});

// API routes
app.use('/api/auth', authRoutes);
app.use('/api/timeseries', timeSeriesRoutes);
app.use('/api/models', modelsRoutes);
app.use('/api/predictions', predictionsRoutes);
app.use('/api/aitools', aiToolsRoutes);
app.use('/api/integrations', integrationsRoutes);

// Error handling middleware
app.use((err, req, res, _next) => {
  console.error(err.stack);
  res.status(err.status || 500).json({
    error: {
      message: err.message || 'Internal Server Error',
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    }
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: { message: 'Route not found' } });
});

const PORT = process.env.BACKEND_PORT || 5000;

const server = app.listen(PORT, () => {
  console.log(`🚀 Backend server running on port ${PORT}`);
  console.log(`📊 Environment: ${process.env.NODE_ENV || 'development'}`);
});

// Graceful shutdown for autonomous/containerised operation
const shutdown = (signal) => {
  console.log(`\n${signal} received. Closing server gracefully...`);
  server.close(() => {
    console.log('✅ Server closed.');
    process.exit(0);
  });
  // Force exit after configurable timeout if server hasn't closed
  const timeoutMs = parseInt(process.env.SHUTDOWN_TIMEOUT_MS || '10000', 10);
  setTimeout(() => {
    console.error('⚠️  Forced shutdown after timeout.');
    process.exit(1);
  }, timeoutMs).unref();
};

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));

module.exports = { app, server };
