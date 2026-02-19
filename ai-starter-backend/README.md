# AI Starter Backend

FastAPI backend for the full-stack AI starter application with authentication and OpenAI chat integration.

## Features

- **Authentication**: JWT-based auth with registration, login, and user info endpoints
- **Chat**: OpenAI integration with local development stub
- **Database**: PostgreSQL with async SQLAlchemy
- **Logging**: Structured JSON logging for requests/responses
- **Security**: Password hashing with bcrypt, JWT tokens

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 12+

### Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Initialize database**:
   ```bash
   python -m app.db.init_db
   ```

4. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at http://localhost:8000

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```

- `POST /api/auth/login` - Login and receive JWT token
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```

- `GET /api/auth/me` - Get current user info (requires auth header)

### Chat

- `POST /api/chat` - Send chat messages (requires auth header)
  ```json
  {
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }
  ```

## Development

### Local Model Stub

When `USE_LOCAL_MODEL=true` or `OPENAI_API_KEY` is not set, the chat endpoint uses a simple echo stub for testing without OpenAI API access.

### Environment Variables

See `.env.example` for all configuration options:

- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET` - Secret key for JWT tokens (min 32 characters)
- `JWT_EXPIRES_IN` - Token expiration in seconds (default: 3600)
- `OPENAI_API_KEY` - Your OpenAI API key
- `OPENAI_MODEL` - OpenAI model to use (default: gpt-4o)
- `USE_LOCAL_MODEL` - Use local echo stub instead of OpenAI (default: false)

## Docker

Build and run with Docker:

```bash
docker build -t ai-starter-backend .
docker run -p 8000:8000 --env-file .env ai-starter-backend
```

## Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
