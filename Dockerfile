FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

ENV PYTHONUNBUFFERED=1

# Expose the default port (documentative)
EXPOSE 5000

# Default command runs server; can be overridden to run client or tests
CMD ["python", "run_chatbot.py", "--mode", "server"]
