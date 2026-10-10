# backend/model/fare_prediction.py
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import logging
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
from fastapi.responses import JSONResponse
from model.supabase_store import fetch_predictions, insert_prediction
import math

# Initialize FastAPI app
app = FastAPI()
router = APIRouter()

# CORS middleware to allow communication with frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model 
try:
    model_path = Path(__file__).resolve().parents[1] / "model" / "rf_regressor.pkl"
    model = joblib.load(model_path)
except Exception as e:
    logging.error(f"Error loading model: {str(e)}")
    raise RuntimeError("Model file not found.")

# Request data model for flight fare prediction
class FlightFareRequest(BaseModel):
    airline: str
    sourceCity: str
    destinationCity: str
    departureTime: str
    arrivalTime: str
    stops: str
    flightClass: str
    duration: float
    days_left: int

def transform_features(data: FlightFareRequest):
    # This function transforms the input data into the feature set used during model training.
    # It applies label encoding to categorical variables as done during training.

    # Create a DataFrame from the input data
    input_df = pd.DataFrame({
        'airline': [data.airline],
        'source_city': [data.sourceCity],
        'departure_time': [data.departureTime],
        'stops': [data.stops],
        'arrival_time': [data.arrivalTime],
        'destination_city': [data.destinationCity],
        'class': [data.flightClass],
        'duration': [data.duration],
        'days_left': [data.days_left],
    })
    
    # Apply label encoding to categorical columns (same as done during training)
    label_columns = ['airline', 'source_city', 'departure_time', 'stops', 'arrival_time', 'destination_city', 'class']
    le = LabelEncoder()
    
    for column in label_columns:
        if input_df[column].dtype == 'object':
            input_df[column] = le.fit_transform(input_df[column])

    # Assign feature names to the transformed features
    feature_names = ['airline', 'source_city', 'departure_time', 'stops', 'arrival_time', 
                     'destination_city', 'class', 'duration', 'days_left']
    
    # Return the feature set as a DataFrame with feature names
    transformed_df = pd.DataFrame(input_df.values, columns=feature_names)
    
    return transformed_df

# Prediction endpoint
@router.post("/fare/predict/")
async def predict_flight_fare(flight_data: FlightFareRequest):
    try:
        predicted_fare = await predict_and_store(flight_data, flight_data.days_left)

        # Return the predicted fare (rounded to 2 decimal places)
        return JSONResponse(content={"predicted_fare": predicted_fare})
    
    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Flight fare cannot be predicted.")

async def predict_and_store(flight_data: FlightFareRequest, days_left: int):
    request = flight_data.model_copy(update={"days_left": days_left})
    features = transform_features(request)
    predicted_fare = model.predict(features)
    predicted_fare = round(predicted_fare[0], 2)

    insert_prediction("fare_predictions", {
        "airline": request.airline,
        "source_city": request.sourceCity,
        "destination_city": request.destinationCity,
        "departure_time": request.departureTime,
        "arrival_time": request.arrivalTime,
        "stops": request.stops,
        "flight_class": request.flightClass,
        "duration": float(math.ceil(request.duration * 100)) / 100,
        "days_left": request.days_left,
        "predicted_fare": predicted_fare,
    })

    return predicted_fare

# Define separate endpoints for each scenario with different "days_left" values
@router.post("/fare/predict/day_0/")
async def predict_fare_day_0(flight_data: FlightFareRequest):
    return {"predicted_fare": await predict_and_store(flight_data, days_left=0)}

@router.post("/fare/predict/day_1/")
async def predict_fare_day_1(flight_data: FlightFareRequest):
    return {"predicted_fare": await predict_and_store(flight_data, days_left=1)}

@router.post("/fare/predict/day_7/")
async def predict_fare_day_7(flight_data: FlightFareRequest):
    return {"predicted_fare": await predict_and_store(flight_data, days_left=7)}

@router.post("/fare/predict/day_14/")
async def predict_fare_day_14(flight_data: FlightFareRequest):
    return {"predicted_fare": await predict_and_store(flight_data, days_left=14)}

@router.post("/fare/predict/day_30/")
async def predict_fare_day_30(flight_data: FlightFareRequest):
    return {"predicted_fare": await predict_and_store(flight_data, days_left=30)}

# Root endpoint 
@router.get("/fare")
async def root():
    return {"message": "Flight Fare Prediction API is running"}

# Endpoint to get the prediction record stored in the database
@router.get("/fare/predictions/")
async def get_predictions():
    try:
        return fetch_predictions("fare_predictions")
    except Exception as e:
        logging.error(f"Could not fetch fare predictions: {str(e)}")
        raise HTTPException(status_code=500, detail="Fare predictions cannot be fetched.")

# Main execution
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
