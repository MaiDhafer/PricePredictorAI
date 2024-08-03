# IMPORT LIBRARIES
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
from keras.models import load_model

# INPUT FILES
model_path = '../Model/PricePredictor MODEL/BestPricePredictor.keras'
model = load_model(model_path)
scaler_x_path = '../Model/Features and Target/scaler_x.pkl'
scaler_x = joblib.load(scaler_x_path)
scaler_y_path = '../Model/Features and Target/scaler_y.pkl'
scaler_y = joblib.load(scaler_y_path)
features_path = '../Model/Features and Target/features.pkl'
features = joblib.load(features_path)

# FUNCTION TO ADJUST THE INPUT DATA FOR PREDICTION
def input(bedroom, district_name, date, features, scaler_x):

    # CONVERT DATE TO NUMERICAL FORMAT
    date = datetime.strptime(date, "%Y %m %d")
    year = date.year
    month = date.month
    day = date.day
    date_str = date.strftime('%y%m%d')
    date_num = int(date_str)

    # INPUT DATA
    input_data = [bedroom, date_num, year, month, day]

    # LOOP IN DISTRICT
    district_features = [0] * (len(features) - 5)
    for i, feature in enumerate(features[5:]):
        if district_name in feature:
            district_features[i] = 1
            break
    input_data.extend(district_features)
    df_input = pd.DataFrame([input_data], columns=features)
    x_scaled = scaler_x.transform(df_input)
    x_lstm = np.reshape(x_scaled, (x_scaled.shape[0], 1, x_scaled.shape[1]))
    return x_lstm

# FUNCTION TO PREDICT PRICE
def predict_price(bedroom, district_name, date):

    # INPUT
    x_lstm = input(bedroom, district_name, date, features, scaler_x)

    # PREDICT PRICE
    y_pred_scaled = model.predict(x_lstm)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)

    # PRINTING FORMAT
    print(f"Date: {date}")
    print(f"District: {district_name}")
    print(f"Number of Bedrooms: {bedroom}")
    print(f"Predicted Price: {y_pred[0][0]:,.2f}")

# SELECTED INPUT TO PREDICT PRICE
inputs = [
    (1, "حي العقيق", "2024 08 09"),
    (2, "حي الملقا", "2024 08 15"),
    (3, "حي القيروان", "2024 08 26"),
]

# OUTPUT FOR PREDICTION OF PRICE
for bedroom, district_name, date in inputs:
    predict_price(bedroom, district_name, date)