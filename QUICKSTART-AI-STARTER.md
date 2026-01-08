# AI Starter - Quick Start Guide

Get the AI starter running in 5 minutes! 🚀

## The Fastest Way (Local - No OpenAI Key Required)

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (or use Docker for just the DB)

### Step 1: Start PostgreSQL

**Option A - Using Docker** (easiest):
```bash
docker run --name ai-starter-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=ai_starter \
  -p 5432:5432 \
  -d postgres:15-alpine
```

**Option B - Local PostgreSQL**:
```bash
createdb ai_starter
```

### Step 2: Start the Backend

```bash
cd ai-starter-backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cat > .env << EOF
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ai_starter
JWT_SECRET=my-super-secret-key-change-this-in-production-must-be-32-chars
JWT_EXPIRES_IN=3600
USE_LOCAL_MODEL=true
EOF

# Initialize database
python -m app.db.init_db

# Start backend
uvicorn app.main:app --reload
```

Backend running at **http://localhost:8000** ✅

### Step 3: Start the Frontend

Open a new terminal:

```bash
cd ai-starter-frontend

# Install dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000" > .env.local

# Start frontend
npm run dev
```

Frontend running at **http://localhost:3000** ✅

### Step 4: Try It Out!

1. Open http://localhost:3000
2. Click **Register**
3. Create an account (any email, password)
4. You'll be automatically logged in
5. Start chatting! Messages will echo back

## Using OpenAI (Optional)

To use real AI responses instead of the echo stub:

1. Get an API key from https://platform.openai.com/api-keys

2. Update backend `.env`:
   ```env
   OPENAI_API_KEY=sk-your-actual-key-here
   USE_LOCAL_MODEL=false
   OPENAI_MODEL=gpt-4o
   ```

3. Restart backend:
   ```bash
   # Stop with Ctrl+C, then
   uvicorn app.main:app --reload
   ```

Now your chats will use GPT-4o! 🤖

## With Docker (When Build Works)

When SSL cert issues are fixed in your build environment:

```bash
# Create environment file
cp .env.ai-starter.example .env.ai-starter

# Start everything
docker compose -f docker-compose-ai-starter.yml --env-file .env.ai-starter up --build
```

Access at:
- Frontend: http://localhost:3001
- Backend: http://localhost:8001
- API Docs: http://localhost:8001/docs

## Troubleshooting

### "Connection refused" errors
- Backend: Check if running on port 8000
- Database: Check PostgreSQL is running
- Frontend: Check `NEXT_PUBLIC_API_BASE_URL` in .env.local

### "Module not found" errors
- Backend: Activate venv and `pip install -r requirements.txt`
- Frontend: Run `npm install`

### Database errors
- Check PostgreSQL is running: `pg_isready`
- Re-run: `python -m app.db.init_db`

### Port already in use
```bash
# Backend (port 8000)
lsof -ti:8000 | xargs kill -9

# Frontend (port 3000)
lsof -ti:3000 | xargs kill -9
```

## What You Get

✅ **Complete Authentication**
- Register new accounts
- Login with JWT tokens
- Protected routes

✅ **AI Chat Interface**
- Clean, modern UI
- Message history
- Real-time responses

✅ **Database Persistence**
- Users stored securely
- Chat messages saved
- PostgreSQL backend

✅ **Production Ready**
- Type-safe TypeScript
- Async database operations
- Structured logging
- Environment-based config

## Next Steps

- See **AI-STARTER-README.md** for full documentation
- See **IMPLEMENTATION-COMPLETE.md** for technical details
- Check **TESTING-LOCALLY.md** for more testing options

## Need Help?

- Check the logs in your terminals
- Visit http://localhost:8000/docs for API documentation
- Review the error messages carefully
- Check PostgreSQL is accessible

---

**Enjoy your new AI starter!** 🎉

Built with FastAPI, Next.js, PostgreSQL, and ❤️
