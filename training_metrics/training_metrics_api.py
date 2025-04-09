from flask import Flask, Response
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

# Example metric
training_requests = Counter('training_requests_total', 'Total training requests')

@app.route('/metrics')
def metrics():
    training_requests.inc()
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8002)
