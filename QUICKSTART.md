# AI-Time-Machines Quick Start Guide

This guide will help you get started with the AI-Time-Machines Full Stack platform in minutes.

## 🚀 Quick Deploy with Docker (5 minutes)

The fastest way to get the entire platform running.

### Step 1: Prerequisites
- Install [Docker](https://docs.docker.com/get-docker/)
- Install [Docker Compose](https://docs.docker.com/compose/install/)

### Step 2: Clone and Configure

```bash
# Clone the repository
git clone https://github.com/lippytm/AI-Time-Machines.git
cd AI-Time-Machines

# Copy environment file
cp .env.example .env
```

### Step 3: Edit Configuration

Open `.env` and set these essential variables:

```env
# REQUIRED: Set a secure JWT secret
JWT_SECRET=your-very-secure-random-secret-key-here

# Database credentials (or use defaults)
DB_PASSWORD=postgres
DB_NAME=ai_time_machines
```

### Step 4: Launch

```bash
# Build and start all services
docker-compose up -d

# View logs (optional)
docker-compose logs -f
```

### Step 5: Access the Platform

Open your browser to:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Python ML Service**: http://localhost:8000

That's it! 🎉

## 📝 First Steps After Login

### 1. Register Your Account
1. Go to http://localhost:3000
2. Click "Register"
3. Fill in username, email, and password
4. Click "Register" button

### 2. Upload Time Series Data
1. Click "Time Series" in the navigation
2. Click "+ Upload Time Series"
3. Enter a name (e.g., "Sales Data")
4. Add description (optional)
5. Click "Create" (demo data is auto-generated)

### 3. Train Your First AI Model
1. Navigate to "Models"
2. Click "+ Train New Model"
3. Enter model name (e.g., "Sales Forecast Model")
4. Select your time series data
5. Choose model type (LSTM recommended for beginners)
6. Click "Train Model"
7. Wait for status to change to "completed"

### 4. Generate Predictions
1. Go to "Predictions"
2. Click "+ Generate Prediction"
3. Select your trained model
4. Set horizon (e.g., 10 for 10 steps ahead)
5. Click "Generate"
6. View predicted values

## 🛠️ Local Development Setup

For developers who want to run services individually:

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+

### Backend Setup

```bash
cd backend
npm install

# Create database
createdb ai_time_machines

# Start server
npm run dev
```

Backend runs on: http://localhost:5000

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs on: http://localhost:3000

### Python ML Service Setup

```bash
cd python-service
pip install -r requirements.txt
python app.py
```

Python service runs on: http://localhost:8000

## 🔧 Common Tasks

### Stop All Services
```bash
docker-compose down
```

### Restart a Service
```bash
docker-compose restart backend
```

### View Service Logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f python-service
```

### Reset Database
```bash
docker-compose down -v
docker-compose up -d
```

### Update Code and Rebuild
```bash
git pull
docker-compose up -d --build
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -ti:3000
# Kill the process
kill -9 <PID>
```

### Cannot Connect to Database
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### Frontend Shows "API Error"
```bash
# Check backend is running
docker-compose ps backend

# Check backend logs
docker-compose logs backend
```

### Python Service Crashes
```bash
# Check Python service logs
docker-compose logs python-service

# Restart Python service
docker-compose restart python-service
```

## 📊 Understanding the Platform

### Time Series Data
- Represents sequential data points over time
- Examples: stock prices, sales figures, sensor readings
- Required format: array of `{timestamp, value}` objects

### AI Models
Five supported model types:
- **LSTM**: Best for general time series (recommended)
- **GRU**: Faster alternative to LSTM
- **ARIMA**: Statistical approach, good for simple patterns
- **Prophet**: Excellent for data with strong seasonality
- **Transformer**: For complex, long-range patterns

### Predictions
- **Horizon**: Number of future time steps to predict
- **Confidence**: Upper and lower bounds of predictions
- Based on trained model patterns

## 🎯 Next Steps

1. **Explore the Dashboard**: View statistics and overview
2. **Upload Real Data**: Replace sample data with your CSV files
3. **Compare Models**: Train multiple model types on same data
4. **Experiment**: Try different hyperparameters
5. **Integrate**: Use the REST API in your applications

## 📚 Additional Resources

- [Full README](README.md) - Complete documentation
- [Contributing Guide](CONTRIBUTING.md) - Contribution guidelines

## 💡 Tips

- Start with LSTM models for best results
- Use at least 100 data points for training
- Higher horizons need more training data
- Monitor model training in the Models page
- Save prediction results for comparison

## 🆘 Need Help?

- [GitHub Issues](https://github.com/lippytm/AI-Time-Machines/issues)
- [GitHub Discussions](https://github.com/lippytm/AI-Time-Machines/discussions)

---

Happy forecasting! 🚀
