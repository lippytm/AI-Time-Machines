# AI Starter - Full-Stack AI Chat Application

A complete full-stack AI starter application with authentication and chat functionality, built with FastAPI (Python 3.11) backend and Next.js (TypeScript) frontend.

## 🌟 Features

### Backend (FastAPI + Python 3.11)
- ✅ **Authentication**: JWT-based auth with registration, login, and user info
- ✅ **Chat Integration**: OpenAI API integration with local development stub
- ✅ **Database**: PostgreSQL with async SQLAlchemy (asyncpg driver)
- ✅ **Security**: Password hashing with bcrypt, JWT token validation
- ✅ **Logging**: Structured JSON logging with request/response timing
- ✅ **Error Handling**: Comprehensive error handling with proper HTTP status codes

### Frontend (Next.js + TypeScript)
- ✅ **Modern UI**: Next.js 14 with App Router and TypeScript
- ✅ **Authentication**: Register, login, logout flows with auth context
- ✅ **Chat Interface**: Clean chat UI with message history
- ✅ **Styling**: Tailwind CSS for responsive design
- ✅ **State Management**: React Context API for authentication state

### DevOps
- ✅ **Docker**: Multi-stage Dockerfiles for optimized images
- ✅ **Docker Compose**: Full orchestration with health checks
- ✅ **Database Migrations**: Automatic database initialization

## 📋 Prerequisites

- **Docker** and **Docker Compose** (recommended)
- OR:
  - **Python 3.11+**
  - **Node.js 18+**
  - **PostgreSQL 15+**

## 🚀 Quick Start with Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/lippytm/AI-Time-Machines.git
   cd AI-Time-Machines
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.ai-starter.example .env.ai-starter
   # Edit .env.ai-starter if needed (default values work out of the box)
   ```

3. **Start all services**:
   ```bash
   docker-compose -f docker-compose-ai-starter.yml --env-file .env.ai-starter up --build
   ```

4. **Access the application**:
   - Frontend: http://localhost:3001
   - Backend API: http://localhost:8001
   - API Documentation: http://localhost:8001/docs

5. **Test the application**:
   - Register a new account at http://localhost:3001/register
   - Login and start chatting
   - By default, uses local echo model (no OpenAI API key required)

## 🛠️ Local Development Setup

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd ai-starter-backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your database settings
   ```

5. **Initialize database** (PostgreSQL must be running):
   ```bash
   python -m app.db.init_db
   ```

6. **Run the backend**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd ai-starter-frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment**:
   ```bash
   cp .env.example .env.local
   # Edit .env.local to point to your backend
   ```

4. **Run the frontend**:
   ```bash
   npm run dev
   ```

The frontend will be available at http://localhost:3000

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ai_starter
JWT_SECRET=your-secret-key-min-32-characters
JWT_EXPIRES_IN=3600
OPENAI_API_KEY=sk-your-api-key  # Optional
OPENAI_MODEL=gpt-4o
USE_LOCAL_MODEL=true  # Set to false to use OpenAI
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Using OpenAI API

1. Get an API key from https://platform.openai.com/api-keys
2. Set `OPENAI_API_KEY` in your `.env.ai-starter` file
3. Set `USE_LOCAL_MODEL=false`
4. Restart services

### Local Model Stub

When `USE_LOCAL_MODEL=true` or `OPENAI_API_KEY` is not set, the backend uses a simple echo stub that repeats the user's message. This is perfect for development and testing without incurring OpenAI API costs.

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info (requires auth)

### Chat
- `POST /api/chat` - Send chat messages (requires auth)

### Health
- `GET /health` - Health check endpoint

See interactive API documentation at http://localhost:8001/docs

## 🏗️ Project Structure

```
AI-Time-Machines/
├── ai-starter-backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/routes/         # API route handlers
│   │   ├── core/               # Core utilities (config, security)
│   │   ├── db/                 # Database connection and init
│   │   ├── middleware/         # Custom middleware
│   │   ├── models/             # Database and Pydantic models
│   │   └── main.py             # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile
│   └── README.md
├── ai-starter-frontend/         # Next.js frontend
│   ├── app/                    # Next.js app directory
│   │   ├── chat/              # Chat page
│   │   ├── login/             # Login page
│   │   └── register/          # Register page
│   ├── contexts/              # React contexts
│   ├── lib/                   # API client
│   ├── Dockerfile
│   └── package.json
├── docker-compose-ai-starter.yml
└── .env.ai-starter.example
```

## 🧪 Testing

### Manual Testing Flow

1. **Register**: Create a new account
   - Email: test@example.com
   - Password: password123

2. **Login**: Sign in with your credentials

3. **Chat**: Send messages and receive responses
   - With local model: Messages are echoed back
   - With OpenAI: Real AI responses

4. **Logout**: Sign out and verify redirect to login

### Backend Testing
```bash
cd ai-starter-backend
# Add tests as needed
pytest
```

### Frontend Testing
```bash
cd ai-starter-frontend
npm test
```

## 🐳 Docker Commands

```bash
# Build and start all services
docker-compose -f docker-compose-ai-starter.yml --env-file .env.ai-starter up --build

# Start in detached mode
docker-compose -f docker-compose-ai-starter.yml --env-file .env.ai-starter up -d

# View logs
docker-compose -f docker-compose-ai-starter.yml logs -f

# Stop services
docker-compose -f docker-compose-ai-starter.yml down

# Stop and remove volumes (fresh start)
docker-compose -f docker-compose-ai-starter.yml down -v
```

## 🔒 Security Features

- ✅ JWT-based authentication
- ✅ Password hashing with bcrypt (via passlib)
- ✅ CORS configuration
- ✅ HTTP-only cookie support (configurable)
- ✅ Environment-based secrets management
- ✅ SQL injection protection (SQLAlchemy ORM)

## 🚧 Troubleshooting

### Database Connection Issues

**Problem**: Backend can't connect to database

**Solution**:
```bash
# Check if PostgreSQL is running
docker-compose -f docker-compose-ai-starter.yml ps

# View database logs
docker-compose -f docker-compose-ai-starter.yml logs postgres-ai-starter

# Restart database
docker-compose -f docker-compose-ai-starter.yml restart postgres-ai-starter
```

### Port Conflicts

**Problem**: Ports 3001 or 8001 already in use

**Solution**: Edit `.env.ai-starter` or `docker-compose-ai-starter.yml` to use different ports

### Frontend Can't Connect to Backend

**Problem**: API requests fail with CORS or network errors

**Solutions**:
1. Check backend is running: http://localhost:8001/health
2. Verify `NEXT_PUBLIC_API_BASE_URL` in frontend .env.local
3. Check CORS settings in `app/main.py`

### OpenAI API Errors

**Problem**: Chat fails when using OpenAI

**Solutions**:
1. Verify API key is correct
2. Check API key has credits: https://platform.openai.com/usage
3. Ensure model name is valid (e.g., gpt-4o, gpt-3.5-turbo)
4. Set `USE_LOCAL_MODEL=true` to test without OpenAI

## 🎯 Next Steps / Extensions

- [ ] Add message persistence and chat history
- [ ] Implement streaming responses
- [ ] Add user profile management
- [ ] Implement password reset flow
- [ ] Add rate limiting
- [ ] Add conversation export
- [ ] Add multi-conversation support
- [ ] Add system prompts customization
- [ ] Add file upload support
- [ ] Add WebSocket support for real-time updates

## 📝 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📧 Support

For questions and support:
- Open an issue on [GitHub](https://github.com/lippytm/AI-Time-Machines/issues)
- Check [GitHub Discussions](https://github.com/lippytm/AI-Time-Machines/discussions)

---

**Built with ❤️ as a full-stack AI starter template**
