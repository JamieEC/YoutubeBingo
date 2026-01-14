FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Use unbuffered stdout for prints
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Start the app
CMD ["python", "server.py"]
