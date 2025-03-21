# Base Image
FROM python:3.10-slim

# working dir
WORKDIR /app

# install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install torch torchvision torchaudio

COPY . .
RUN mkdir -p data/raw data/processed data/external

ENV PYTHONPATH=/app
ENV FLASKAPP=predict_api.py
