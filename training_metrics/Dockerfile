FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY training_metrics_api.py .

EXPOSE 8002

CMD ["python", "training_metrics_api.py"]
