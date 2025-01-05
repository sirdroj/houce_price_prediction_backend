from fastapi import FastAPI
from houce_price_prediction_class import HousePricePredictor  # Import predictor from the appropriate module
from typing import Optional
from pydantic import BaseModel


# Create a FastAPI app instance
app = FastAPI()
hppclass=HousePricePredictor()
# Define a root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}


class PredictPriceRequest(BaseModel):
    location: Optional[str] = None
    sqft: Optional[float] = None
    bath: Optional[int] = None
    bhk: Optional[int] = None

@app.get("/predict_price")
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

