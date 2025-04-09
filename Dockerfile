# Base Image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt \
    && pip install --no-cache-dir --upgrade torch torchvision torchaudio

# Copy app source code
COPY . .

# Set up logs and data directories
RUN mkdir -p data/raw data/processed data/external logs && \
    groupadd -r app && useradd -r -g app app && \
    chown -R app:app /app

# Switch to non-root user
USER app

# Expose port and set environment
ENV PYTHONPATH=/app
ENV FLASK_APP=predict_api.py
ENV FLASK_ENV=production
EXPOSE 9000

# Start Flask app
CMD ["python3", "predict_api.py"]