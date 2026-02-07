require('dotenv').config({ path: '../.env' });
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');

const authRoutes = require('./routes/auth');
const timeSeriesRoutes = require('./routes/timeSeries');
const modelsRoutes = require('./routes/models');
const predictionsRoutes = require('./routes/predictions');
const aiToolsRoutes = require('./routes/aiTools');
const integrationsRoutes = require('./routes/integrations');

const { apiLimiter } = require('./middleware/rateLimiter');
const { aiFirewall, sqlInjectionProtection } = require('./middleware/aiFirewall');

const app = express();

// Security middleware
app.use(helmet());

// CORS configuration
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
  credentials: true
}));

// Body parsing middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Logging middleware
if (process.env.NODE_ENV !== 'test') {
  app.use(morgan('dev'));
}

// Security middleware - AI Firewall
app.use(aiFirewall);
app.use(sqlInjectionProtection);

// Rate limiting for all API routes
app.use('/api/', apiLimiter);

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ 
    status: 'healthy', 
    service: 'AI Time Machines Backend',
    timestamp: new Date().toISOString()
  });
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

module.exports = { app, server };
