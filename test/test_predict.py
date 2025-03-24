import pytest
import joblib
import pandas as pd
from model.prediction import predict_used_car_region

# Load the saved KMeans clustering model and scaler frm the checkpoints folder
kmeans = joblib.load("model/checkpoints/kmeans_model.pkl")
scaler = joblib.load("model/checkpoints/scaler.pkl")

# Sample aggregated data whch coulde be used for testing 
agg_data = pd.DataFrame({
    "region_label": ["Region1", "Region2", "Region3"], # Names of the regions
    "total_sales": [500, 600, 700], # Examples sales numvers 
    "cluster": [0, 1, 2]  # Cluster IDs from KMeans
})

def test_predict_used_car_region():
    """Test the prediction function for used cars."""
    result = predict_used_car_region(25000, 60000)
    
    # Ensure output is a DataFrame
    assert isinstance(result, pd.DataFrame)
    
    # Ensure if the required columns exist
    assert "region_label" in result.columns
    assert "total_sales" in result.columns

    print(" `predict_used_car_region` passed all tests!")

   








