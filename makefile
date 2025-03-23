SHELL := /bin/bash  # Ensure Makefile uses Bash
VENV_ACTIVATE = . .venv/bin/activate  # Define virtual environment activation

# Setup virtual environment
setup:
    python3 -m venv .venv
    $(VENV_ACTIVATE) && pip install -r requirements.txt

# Install dependencies
install:
    $(VENV_ACTIVATE) && pip install -r requirements.txt

# Run basic app
run-basic:
    $(VENV_ACTIVATE) && streamlit run src/app.py

# Run advanced app
run-advanced:
    $(VENV_ACTIVATE) && streamlit run src/advanced_app.py

# Run tests inside virtual environment
test:
    $(VENV_ACTIVATE) && PYTHONPATH=$(pwd) pytest test/

# Initialize MLFlow
mlflow-init:
    @echo "Initializing MLflow server"
    $(VENV_ACTIVATE) && python src/utils/mlflow_initialize.py

# Train model
train:
    @echo "Running train.py"
    $(VENV_ACTIVATE) && python model/train.py

# Predict using API
predict:
    @echo "Running predict_api.py"
    $(VENV_ACTIVATE) && python predict_api.py

# Clean up temporary files
clean:
    rm -rf __pycache__ */__pycache__
