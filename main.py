from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from houce_price_prediction_class import HousePricePredictor  # Import predictor from the appropriate module
from typing import Optional
from pydantic import BaseModel

# Create a FastAPI app instance
app = FastAPI()
hppclass = HousePricePredictor()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:3000"],  # Add your frontend's origin here
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define a root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

class PredictPriceRequest(BaseModel):
    location: Optional[str] = None
    sqft: Optional[float] = None
    bath: Optional[int] = None
    bhk: Optional[int] = None

@app.post("/predict_price")
def predict_price_api(request: PredictPriceRequest):
    """
    API endpoint to predict house price based on input parameters.

    Parameters:
    - request (PredictPriceRequest): The input data including location, sqft, bath, and bhk.

    Returns:
    - dict: Predicted price of the property.
    """
    try:
        predicted_price = hppclass.predict_price(request.location, request.sqft, request.bath, request.bhk)
        if predicted_price is not None:
            return {"predicted_price": predicted_price}
        else:
            return {"error": "Could not predict the price. Please check the input values."}
    except Exception as e:
        return {"error": str(e)}
