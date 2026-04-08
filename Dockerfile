# Use official Python runtime as a parent image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies required for audio processing
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    libsndfile1-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir fastapi uvicorn python-dotenv

# Copy the entire project
COPY . .

# Create necessary directories
RUN mkdir -p data/raw_audio data/resampled output logs

# Expose port (FastAPI default)
EXPOSE 8013

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the FastAPI application with Uvicorn
CMD ["uvicorn", "Api:app", "--host", "0.0.0.0", "--port", "8013"]
