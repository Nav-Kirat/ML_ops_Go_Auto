from flask import Flask, request, jsonify
import joblib, pandas as pd, os, logging, time, psutil, threading
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Histogram, Gauge

# 🔹 Flask app setup
app = Flask(__name__)

# 🔹 Prometheus metrics
metrics = PrometheusMetrics(app)  # /metrics exposed

prediction_requests = Counter('model_prediction_requests_total', 'Total prediction requests', ['model_version', 'status'])
prediction_time = Histogram('model_prediction_duration_seconds', 'Prediction latency', ['model_version'])
cpu_usage = Gauge('app_cpu_usage_percent', 'CPU usage %')
memory_usage = Gauge('app_memory_usage_bytes', 'Memory usage in bytes')
input_data_size = Gauge('input_payload_size_bytes', 'Size of incoming JSON payload')
model_load_time = Histogram('model_load_time_seconds', 'Time taken to load models and scaler')
api_uptime = Gauge('api_uptime_seconds_total', 'Total uptime of the API in seconds')



def monitor_resources():
    while True:
        proc = psutil.Process(os.getpid())
        cpu_usage.set(proc.cpu_percent(interval=1))
        memory_usage.set(proc.memory_info().rss)
        time.sleep(15)

threading.Thread(target=monitor_resources, daemon=True).start()

def track_uptime():
    start = time.time()
    while True:
        api_uptime.set(time.time() - start)
        time.sleep(10)

threading.Thread(target=track_uptime, daemon=True).start()


# 🔹 Logging
log_dir = os.environ.get("LOG_DIR", "logs")
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f"{log_dir}/api.log")
    ]
)
logger = logging.getLogger("car_cluster_api")

# 🔹 Load models
try:
    model_v1 = joblib.load("model/checkpoints/kmeans_model_6.pkl")
    model_v2 = joblib.load("model/checkpoints/kmeans_model_8.pkl")
    scaler = joblib.load("model/checkpoints/scaler.pkl")
    logger.info("✅ Models and scaler loaded successfully.")
except Exception as e:
    logger.error(f"❌ Failed to load model(s): {e}")
    model_v1 = model_v2 = scaler = None

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Car Prediction API!",
        "endpoints": {
            "Health Check": "/health_status",
            "Prediction V1": "/v1/predict",
            "Prediction V2": "/v2/predict"
        },
        "expected_input_format": {
            "avg_price": "float",
            "mileage": "float"
        }
    })

@app.route("/health_status", methods=["GET"])
def health_check():
    return jsonify({"status": "API is running!"}), 200

@app.route("/v1/predict", methods=["POST"])
def predict_v1():
    start_time = time.time()
    data = request.get_json()
    input_data_size.set(len(str(data)))
    logger.info(f"📥 Input (v1): {data}")

    if "avg_price" not in data or "mileage" not in data:
        return jsonify({"error": "Missing avg_price or mileage"}), 400

    try:
        features = pd.DataFrame([[data["avg_price"], data["mileage"]]], columns=["avg_price", "mileage"])
        scaled = scaler.transform(features)
        cluster = model_v1.predict(scaled)[0]

        prediction_requests.labels(model_version="v1", status="success").inc()
        prediction_time.labels(model_version="v1").observe(time.time() - start_time)

        logger.info(f"🎯 Prediction V1: {cluster}")
        return jsonify({"model_version": "V1", "predicted_cluster": int(cluster)})
    except Exception as e:
        prediction_requests.labels(model_version="v1", status="error").inc()
        return jsonify({"error": str(e)}), 500

@app.route("/v2/predict", methods=["POST"])
def predict_v2():
    start_time = time.time()
    data = request.get_json()
    input_data_size.set(len(str(data)))
    logger.info(f"📥 Input (v2): {data}")

    if "avg_price" not in data or "mileage" not in data:
        return jsonify({"error": "Missing avg_price or mileage"}), 400

    try:
        features = pd.DataFrame([[data["avg_price"], data["mileage"]]], columns=["avg_price", "mileage"])
        scaled = scaler.transform(features)
        cluster = model_v2.predict(scaled)[0]

        prediction_requests.labels(model_version="v2", status="success").inc()
        prediction_time.labels(model_version="v2").observe(time.time() - start_time)

        logger.info(f"🎯 Prediction V2: {cluster}")
        return jsonify({"model_version": "V2", "predicted_cluster": int(cluster)})
    except Exception as e:
        prediction_requests.labels(model_version="v2", status="error").inc()
        return jsonify({"error": str(e)}), 500
    
with model_load_time.time():
    try:
        model_v1 = joblib.load("model/checkpoints/kmeans_model_6.pkl")
        model_v2 = joblib.load("model/checkpoints/kmeans_model_8.pkl")
        scaler = joblib.load("model/checkpoints/scaler.pkl")
        logger.info("✅ Models and scaler loaded successfully.")
    except Exception as e:
        logger.error(f"❌ Failed to load model(s): {e}")
        model_v1 = model_v2 = scaler = None

if not all([model_v1, model_v2, scaler]):
    logger.critical("🚨 One or more models failed to load. Exiting...")
    exit(1)


if __name__ == "__main__":
    logger.info("🚀 Starting Flask API on port 9999...")
    app.run(host="0.0.0.0", port=9000)
