import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.layers import LSTM, Dense, Dropout
from keras.models import Sequential, load_model
from sklearn.model_selection import train_test_split
from keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# INPUT FILE
input_file = '../../STAGE 2 - Preprocessing/Datasets/Encoding/All_Data_Encoded.csv'
df = pd.read_csv(input_file)

# CONVERT DATE TO NUMERICAL FORMAT
df['Start_Date'] = pd.to_datetime(df['Start_Date'])
df['Year'] = df['Start_Date'].dt.year
df['Month'] = df['Start_Date'].dt.month
df['Day'] = df['Start_Date'].dt.day
df['Date'] = df['Start_Date'].dt.strftime('%y%m%d').astype(int)

# FEATURES SELECTION
features = ['Bedroom', 'Date', 'Year', 'Month', 'Day'] + [col for col in df.columns if col.startswith('District')]
x = df[features]
y = df['Price']

# NORMALIZE FEATURES AND TARGET
scaler_x = MinMaxScaler()
x_scaled = scaler_x.fit_transform(x)
scaler_y = MinMaxScaler()
y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1))

# SPLIT THE DATA INTO 80% TRAIN, 10% VALIDATION, 10% TEST
x_train, x_temp, y_train, y_temp = train_test_split(x_scaled, y_scaled, test_size=0.2, random_state=42)
x_test, x_val, y_test, y_val = train_test_split(x_temp, y_temp, test_size=0.5, random_state=42)

# SAVE THE SCALERS AND FEATURE NAMES
joblib.dump(scaler_x, '../Model/Features and Target/scaler_x.pkl')
joblib.dump(scaler_y, '../Model/Features and Target/scaler_y.pkl')
joblib.dump(features, '../Model/Features and Target/features.pkl')

# RESHAPE DATAFRAME TO FIT LSTM REQUIREMENTS
def reshape_for_lstm(x):
    return np.reshape(x, (x.shape[0], 1, x.shape[1]))

x_train_lstm = reshape_for_lstm(x_train)
x_test_lstm = reshape_for_lstm(x_test)
x_val_lstm = reshape_for_lstm(x_val)

# LSTM MODEL
model = Sequential()
model.add(LSTM(50, activation='tanh', input_shape=(x_train_lstm.shape[1], x_train_lstm.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# MODEL CHECKPOINT AND EARLY STOPPING AND SAVE BEST MODEL
checkpoint_callback = ModelCheckpoint('../Model/PricePredictor MODEL/BestPricePredictor.keras', monitor='val_loss', save_best_only=True, verbose=1)
early_stopping_callback = EarlyStopping(monitor='val_loss', patience=10, verbose=1)

# MODEL TRAINING
history = model.fit(
    x_train_lstm, y_train,
    epochs=100,
    batch_size=128,
    validation_data=(x_val_lstm, y_val),
    callbacks=[checkpoint_callback, early_stopping_callback],
    verbose=1
)

# LOAD THE BEST MODEL
loaded_model = load_model('../Model/PricePredictor MODEL/BestPricePredictor.keras')

# MAKE PREDICTIONS
y_test_pred = loaded_model.predict(x_test_lstm)
y_val_pred = loaded_model.predict(x_val_lstm)

# RESCALE PREDICTIONS AND ACTUAL VALUES BACK TO ORIGINAL SCALE
y_test = scaler_y.inverse_transform(y_test)
y_val = scaler_y.inverse_transform(y_val)
y_test_pred = scaler_y.inverse_transform(y_test_pred)
y_val_pred = scaler_y.inverse_transform(y_val_pred)

# MEASURES DIFFERENCE BETWEEN PREDICTIONS AND ACTUAL VALUES
mse_test = mean_squared_error(y_test, y_test_pred)
mse_val = mean_squared_error(y_val, y_val_pred)
print(f'Mean Squared Error on Test Set: {mse_test}')
print(f'Mean Squared Error on Validation Set: {mse_val}')

# MEASURES AVERAGE ABSOLUTE DIFFERENCE BETWEEN PREDICTIONS AND ACTUAL VALUES
mae_test = mean_absolute_error(y_test, y_test_pred)
mae_val = mean_absolute_error(y_val, y_val_pred)
print(f'Mean Absolute Error on Test Set: {mae_test}')
print(f'Mean Absolute Error on Validation Set: {mae_val}')

# MEASURES THE PROPORTION OF VARIANCE BY THE MODEL
r2_test = r2_score(y_test, y_test_pred)
r2_val = r2_score(y_val, y_val_pred)
print(f'R² Score on Test Set: {r2_test}')
print(f'R² Score on Validation Set: {r2_val}')

# VISUALIZATION OF PREDICTED VS ACTUAL VALUES
def plot_predictions(y_true, y_pred, title, filename):
    plt.figure(figsize=(10, 6))
    plt.scatter(y_true, y_pred, alpha=0.7, edgecolors='w', s=100, color='blue', label='Predicted Values')
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], color='red', linestyle='--')
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.title(title)
    plt.legend()
    plt.savefig(filename)
    plt.close()
plot_predictions(y_test, y_test_pred, 'Test Set: Actual vs Predicted', '../Model/Figure/Test_Predictions.png')
plot_predictions(y_val, y_val_pred, 'Validation Set: Actual vs Predicted', '../Model/Figure/Validation_Predictions.png')

# ERROR DISTRIBUTION PLOT
def error_distribution(y_true, y_pred, title, filename):
    errors = y_true.flatten() - y_pred.flatten()
    plt.figure(figsize=(10, 6))
    plt.hist(errors, bins=30, edgecolor='k', alpha=0.7, color='blue')
    plt.xlabel('Error')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.savefig(filename)
    plt.close()
error_distribution(y_test, y_test_pred, 'Test Set: Error Distribution', '../Model/Figure/Test_Error_Distribution.png')
error_distribution(y_val, y_val_pred, 'Validation Set: Error Distribution', '../Model/Figure/Validation_Error_Distribution.png')

# TRAINING AND VALIDATION LOSS PLOT
def plot_loss(history, filename):
    plt.figure(figsize=(10, 6))
    plt.plot(history.history['loss'], label='Training Loss', color='blue')
    plt.plot(history.history['val_loss'], label='Validation Loss', color='orange')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Training and Validation Loss')
    plt.legend()
    plt.savefig(filename)
    plt.close()
plot_loss(history, '../Model/Figure/Training_Validation_Loss.png')

# SAVE TRAINED MODEL
model_filename = '../Model/PricePredictor MODEL/LastPricePredictor.keras'
model.save(model_filename)