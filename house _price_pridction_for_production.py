import pickle
import json
import numpy as np

# Replace 'model.pkl' with your actual pickle file name
with open('banglore_home_prices_model.pickle', 'rb') as file:
    lr_clf = pickle.load(file)


# Now you can use the loaded model for predictions
print("Model loaded successfully.")



# Replace 'file_name.json' with the path to your JSON file
with open('house_price_columns.json', 'r') as file:
    X = json.load(file)

def predict_price(location, sqft, bath, bhk):
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
        if "data_columns" not in X:
            raise ValueError("The feature 'data_columns' is missing from X.")

        # Check if the location exists in 'data_columns'
        data_columns = X["data_columns"]
        # print(f"data_columns: {data_columns}")
        loc_index = data_columns.index(location) if location in data_columns else -1
        print(f"loc_index: {loc_index}")
        # Initialize the feature vector
        x = np.zeros(len(data_columns))
        x[0] = sqft  # First feature is square footage
        x[1] = bath  # Second feature is bathrooms
        x[2] = bhk   # Third feature is bedrooms

        # Set location feature to 1 if found
        if loc_index >= 0:
            x[loc_index] = 1

        # Make prediction using the trained model
        predicted_price = lr_clf.predict([x])[0]
        return predicted_price

    except Exception as e:
        print(f"Error predicting price: {e}")
        return None


# print("X["data_columns"]",X["data_columns"])
print(predict_price('1st Phase JP Nagar',1000, 2, 2))
print(predict_price('Indira Nagar',10000, 2, 2))