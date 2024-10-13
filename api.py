from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Create the FastAPI app
app = FastAPI()

# Load the saved model, encoders, and scaler
with open('Model/vehicle_risk_model.pkl', 'rb') as f:
    model, encoders, scaler = joblib.load(f)


# Define the input data format using Pydantic
class RiskPredictionInput(BaseModel):
    Visibility: str
    Road_Surface_Conditions: str
    Weather: str
    Traffic_Density: str
    Road_Hazards: str
    Fatigue_Level: str
    Medical_Condition: str
    Speeding: str
    Light_Conditions: str


# Define a POST endpoint to predict the risk score
@app.post("/predict")
def predict_risk(input_data: RiskPredictionInput):
    # Extract input data
    data = input_data.dict()

    # Encode the categorical features using the loaded encoders
    encoded_data = []
    for col, le in encoders.items():
        encoded_value = le.transform([data[col]])[0]
        encoded_data.append(encoded_value)

    # Convert the list into a numpy array
    encoded_array = np.array(encoded_data).reshape(1, -1)

    # Standardize the input data using the loaded scaler
    scaled_data = scaler.transform(encoded_array)

    # Make the prediction using the loaded model
    prediction = model.predict(scaled_data)[0]

    # Interpret the prediction
    risk_label = "High Risk" if prediction == 1 else "Low Risk"

    return {"Risk_Score": int(prediction), "Risk_Label": risk_label}
