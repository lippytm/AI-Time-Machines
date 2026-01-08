# AI-Time-Machines

**Full Stack AI Platform for Time-Series Agent Creation, Management, and OpenAI Integration**

AI-Time-Machines is a comprehensive Full Stack platform that combines React, Node.js, Python ML services, PostgreSQL, and OpenAI's advanced AI capabilities to create and manage time-series AI agents with forecasting and conversational AI features.

## 🌟 Features

### Frontend (React + TailwindCSS)
- 🎨 Modern, responsive UI with TailwindCSS
- 🔐 User authentication (Login/Register)
- 📊 Interactive dashboard with real-time statistics
- 📈 Time-series data upload and management
- 🤖 AI model training interface
- 🔮 Predictions visualization

### Backend (Node.js + Express)
- ⚡ RESTful API with Express.js
- 🔒 JWT-based authentication with bcrypt
- 🗄️ PostgreSQL database with Sequelize ORM
- 📝 Comprehensive API endpoints for:
  - User management
  - Time-series data operations
  - AI model training workflows
  - Prediction generation

### AI/ML Service (Python + TensorFlow)
- 🧠 Time-series forecasting models:
  - LSTM (Long Short-Term Memory)
  - GRU (Gated Recurrent Unit)
  - ARIMA (Statistical forecasting)
  - Prophet (Seasonal patterns)
  - Transformer (Complex patterns)
- 📊 Model training and prediction APIs
- 💾 Model persistence and versioning

### Infrastructure
- 🐳 Docker containerization
- 🔄 Docker Compose orchestration
- 🚀 CI/CD with GitHub Actions
- 🔍 Security scanning and dependency review

### OpenAI Integration & Fine-Tuning
- 🤖 Specialized AI agents for time-travel scenarios:
  - Historical Context Agent
  - Temporal Paradox Resolver
  - Time Travel Assistant
- 🎯 Fine-tuning capabilities with custom datasets
- 📚 Comprehensive API configuration and examples
- ⚙️ Easy-to-use agent system with modular architecture

## 📋 Prerequisites

- **Node.js** (version 18.0.0 or higher)
- **Python** (version 3.11 or higher)
- **PostgreSQL** (version 15 or higher)
- **Docker** and **Docker Compose** (for containerized deployment)
- **OpenAI API Key** (optional, for ChatGPT integration)

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/lippytm/AI-Time-Machines.git
   cd AI-Time-Machines
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your configuration
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - Python ML Service: http://localhost:8000

### Option 2: Local Development

#### 1. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ai_time_machines
DB_USER=postgres
DB_PASSWORD=your_password

# JWT
JWT_SECRET=your_secret_key
JWT_EXPIRES_IN=7d

# Servers
BACKEND_PORT=5000
FRONTEND_PORT=3000
PYTHON_SERVICE_PORT=8000
```

#### 2. Set Up PostgreSQL Database

```bash
createdb ai_time_machines
```

#### 3. Install Dependencies

**Backend:**
```bash
cd backend
npm install
```

**Frontend:**
```bash
cd frontend
npm install
```

**Python Service:**
```bash
cd python-service
pip install -r requirements.txt
```

#### 4. Start Services

**Terminal 1 - Backend:**
```bash
cd backend
npm run dev
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

**Terminal 3 - Python Service:**
```bash
cd python-service
python app.py
```

## 📖 Usage Guide

### 1. Register an Account
- Navigate to http://localhost:3000
- Click "Register" and create your account
- Login with your credentials

### 2. Upload Time-Series Data
- Go to "Time Series" section
- Click "+ Upload Time Series"
- Provide a name and description
- Sample data will be generated automatically (or upload your CSV)

### 3. Train an AI Model
- Navigate to "Models" section
- Click "+ Train New Model"
- Select your time series data
- Choose a model type (LSTM, GRU, ARIMA, Prophet, or Transformer)
- Click "Train Model"

### 4. Generate Predictions
- Go to "Predictions" section
- Click "+ Generate Prediction"
- Select a trained model
- Set prediction horizon (1-100 steps)
- View predicted values and confidence intervals

## 🏗️ Architecture

```
AI-Time-Machines/
├── frontend/              # React frontend application
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── contexts/     # React contexts (Auth)
│   │   ├── pages/        # Page components
│   │   ├── services/     # API service layer
│   │   └── App.js        # Main application
│   └── Dockerfile
├── backend/              # Node.js backend API
│   ├── src/
│   │   ├── config/      # Database configuration
│   │   ├── controllers/ # Request handlers
│   │   ├── middleware/  # Auth & validation
│   │   ├── models/      # Sequelize models
│   │   ├── routes/      # API routes
│   │   └── server.js    # Express server
│   └── Dockerfile
├── python-service/       # Python ML service
│   ├── models/          # ML model implementations
│   ├── app.py           # Flask application
│   ├── requirements.txt # Python dependencies
│   └── Dockerfile
├── docker-compose.yml    # Multi-container orchestration
└── .env.example         # Environment template
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user
- `PUT /api/auth/profile` - Update profile

### Time Series
- `GET /api/timeseries` - List all time series
- `POST /api/timeseries` - Create time series
- `GET /api/timeseries/:id` - Get time series
- `PUT /api/timeseries/:id` - Update time series
- `DELETE /api/timeseries/:id` - Delete time series

### Models
- `GET /api/models` - List all models
- `POST /api/models` - Create and train model
- `GET /api/models/:id` - Get model details
- `DELETE /api/models/:id` - Delete model

### Predictions
- `GET /api/predictions` - List all predictions
- `POST /api/predictions` - Generate prediction
- `GET /api/predictions/:id` - Get prediction
- `DELETE /api/predictions/:id` - Delete prediction

## 🤖 OpenAI Integration Features

### Specialized AI Agents

The platform includes pre-built specialized AI agents for time-travel scenarios:

1. **Historical Context Agent** (`agents/historical-context-agent.js`)
   - Provides historical context and information
   - Perfect for time-travel related queries

2. **Temporal Paradox Resolver** (`agents/temporal-paradox-resolver.js`)
   - Helps resolve time-travel paradoxes
   - Analyzes temporal logic and consistency

3. **Time Travel Assistant** (`agents/time-travel-assistant.js`)
   - General-purpose time-travel assistant
   - Guides users through time-travel scenarios

### Using the Agents

```javascript
const { historicalContextAgent, paradoxResolver, timeTravelAssistant } = require('./agents');

// Example: Get historical context
const context = await historicalContextAgent.chat(
  "What was happening in 1969 during the moon landing?"
);

// Example: Resolve a paradox
const resolution = await paradoxResolver.chat(
  "What happens if I prevent my own birth?"
);

// Example: Get travel assistance
const guidance = await timeTravelAssistant.chat(
  "How do I prepare for a trip to ancient Rome?"
);
```

### Fine-Tuning

Create custom AI models with your own data:

```javascript
const { fineTuneModel, listFineTuneJobs } = require('./src/fine-tuning');

// Start a fine-tuning job
const job = await fineTuneModel(
  './datasets/time-machine-training.jsonl',
  { model: 'gpt-4o-mini-2024-07-18', suffix: 'time-machine-v1' }
);

// Check fine-tuning status
const jobs = await listFineTuneJobs();
```

See the [Fine-Tuning Guide](docs/FINE_TUNING.md) for detailed instructions.

### Example Scripts

- `agent-examples.js` - Demonstrates using specialized agents
- `fine-tuning-example.js` - Shows how to fine-tune models
- `examples.js` - Basic ChatGPT integration examples

## 🧪 Testing

**Backend Tests:**
```bash
cd backend
npm test
```

**Frontend Tests:**
```bash
cd frontend
npm test
```

**Run All Tests:**
```bash
npm test
```

## 🐳 Docker Commands

```bash
# Build all images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

## 🔒 Security Features

- ✅ JWT-based authentication
- ✅ Password hashing with bcrypt
- ✅ Environment variable management
- ✅ CORS configuration
- ✅ Helmet.js security headers
- ✅ Input validation with express-validator
- ✅ SQL injection protection (Sequelize ORM)
- ✅ Regular security scanning (Trivy)

## 🚦 CI/CD Pipeline

The project includes GitHub Actions workflows for:
- Code quality and security scanning
- Dependency review
- Backend and frontend testing
- Docker image builds
- Documentation validation

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Database Connection Issues
```bash
# Check if PostgreSQL is running
pg_isready

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### Port Conflicts
If ports 3000, 5000, or 8000 are in use:
```bash
# Find and kill process on port
lsof -ti:3000 | xargs kill -9
```

### Docker Issues
```bash
# Clean up Docker resources
docker system prune -a

# Rebuild from scratch
docker-compose down -v
docker-compose up --build
```

## 📚 Resources

- [React Documentation](https://react.dev/)
- [Express.js Documentation](https://expressjs.com/)
- [TensorFlow Documentation](https://www.tensorflow.org/)
- [Sequelize Documentation](https://sequelize.org/)
- [Docker Documentation](https://docs.docker.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Fine-Tuning Guide](docs/FINE_TUNING.md)
- [API Configuration Guide](docs/API_CONFIG.md)

## 🎯 Roadmap

- [ ] Advanced visualization with Chart.js/D3.js
- [ ] Real-time predictions with WebSockets
- [ ] Model comparison and benchmarking
- [ ] Export predictions to CSV/Excel
- [ ] Multi-variate time series support
- [ ] Automated model hyperparameter tuning
- [ ] Integration with external data sources
- [ ] Mobile application
- [ ] More specialized AI agents
- [ ] Advanced fine-tuning workflows
- [ ] Agent conversation history and persistence

## 📧 Support

For questions and support:
- Open an issue on [GitHub](https://github.com/lippytm/AI-Time-Machines/issues)
- Check [GitHub Discussions](https://github.com/lippytm/AI-Time-Machines/discussions)

---

**Built with ❤️ for AI and Time-Series Enthusiasts** 
