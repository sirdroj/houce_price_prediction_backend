import pickle
import json
import numpy as np

class HousePricePredictor:
    def __init__(self):
        """
        Initialize the HousePricePredictor class by loading the model and column data.

        Parameters:
        - model_file (str): Path to the pickle file containing the trained model.
        - columns_file (str): Path to the JSON file containing the feature columns.
        """
        try:
            # Load the trained model
            with open("banglore_home_prices_model.pickle", 'rb') as file:
                self.lr_clf = pickle.load(file)
            print("Model loaded successfully.")

            # Load the column data
            with open("house_price_columns.json", 'r') as file:
                self.X = json.load(file)
            print("Feature columns loaded successfully.")
        except Exception as e:
            raise RuntimeError(f"Error initializing HousePricePredictor: {e}")

    def predict_price(self, location, sqft, bath, bhk):
        """
        Predict the price of a property based on location, sqft, bathrooms, and bedrooms.

        Parameters:
        - location (str): The location of the property.
        - sqft (float): The square footage of the property.
        - bath (int): The number of bathrooms.
        - bhk (int): The number of bedrooms.

        Returns:
        - float: Predicted price of the property.
        """
        location = location.lower()
        try:
            # Ensure the 'data_columns' key exists in X and contains the columns
            if "data_columns" not in self.X:
                raise ValueError("The feature 'data_columns' is missing from the input JSON file.")

            # Check if the location exists in 'data_columns'
            data_columns = self.X["data_columns"]
            loc_index = data_columns.index(location) if location in data_columns else -1

            # Initialize the feature vector
            x = np.zeros(len(data_columns))
            x[0] = sqft  # First feature is square footage
            x[1] = bath  # Second feature is bathrooms
            x[2] = bhk   # Third feature is bedrooms

            # Set location feature to 1 if found
            if loc_index >= 0:
                x[loc_index] = 1

            # Make prediction using the trained model
            predicted_price = self.lr_clf.predict([x])[0]
            return predicted_price

        except Exception as e:
            print(f"Error predicting price: {e}")
            return None

# Example usage
if __name__ == "__main__":
    # Replace with actual file paths
    model_file_path = 'banglore_home_prices_model.pickle'
    columns_file_path = 'house_price_columns.json'

    predictor = HousePricePredictor(model_file_path, columns_file_path)

    # Test predictions
    print(predictor.predict_price('1st Phase JP Nagar', 1000, 2, 2))
    print(predictor.predict_price('Indira Nagar', 10000, 2, 2))
