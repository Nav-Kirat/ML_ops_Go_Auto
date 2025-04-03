# Base Image
FROM python:3.10-slim

# Working directory
WORKDIR /app

# Copy requirements and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt \
    && pip install --no-cache-dir --upgrade torch torchvision torchaudio  

COPY . .   
RUN mkdir -p data/raw data/processed data/external

ENV PYTHONPATH=/app
ENV FLASKAPP=predict_api.py
EXPOSE 9000
CMD ["python", "predict_api.py"]

# Create app user and group
RUN groupadd -r app && useradd -r -g app app

# Copy app files and setup directories
COPY . .  
RUN mkdir -p data/raw data/processed data/external logs && \
    chown -R app:app logs

# Switch to non-root user
USER app

# Environment setup
ENV PYTHONPATH=/app
ENV FLASKAPP=predict_api.py
ENV FLASK_ENV=production

EXPOSE 9000

CMD ["python", "predict_api.py"]