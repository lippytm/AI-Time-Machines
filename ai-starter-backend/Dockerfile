FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run database initialization on startup, then start the app
CMD python -m app.db.init_db && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
