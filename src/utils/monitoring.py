from prometheus_client import start_http_server, Gauge, Counter
import threading

class TrainingMonitor:
    def __init__(self, port=8002):
        self.port = port
        self.epoch = Counter('training_epochs_total', 'Total number of epochs completed')
        self.batch = Counter('training_batches_total', 'Total number of batches completed')
        self.loss = Gauge('training_loss', 'Training loss')
        self.val_loss = Gauge('validation_loss', 'Validation loss')
        self.cpu_usage = Gauge('training_cpu_usage_percent', 'CPU usage during training')
        self.memory_usage = Gauge('training_memory_usage_bytes', 'Memory usage during training')

        # Start Prometheus metrics server
        threading.Thread(target=start_http_server, args=(self.port,), daemon=True).start()

    def update_metrics(self, epoch=None, batch=None, loss=None, val_loss=None):
        if epoch is not None:
            self.epoch.inc()
        if batch is not None:
            self.batch.inc()
        if loss is not None:
            self.loss.set(loss)
        if val_loss is not None:
            self.val_loss.set(val_loss)
