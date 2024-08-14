# Real Estate Price Prediction using LSTM 🏘️

![Real Estate Visualization](https://media.licdn.com/dms/image/D4D12AQF7aWCrSGv5_w/article-cover_image-shrink_720_1280/0/1708328033213?e=2147483647&v=beta&t=7tGBbmwb88d1DyBDQ4Du5Pn7CL3DFlFzM0aGpYzvZts)


Welcome to the Real Estate Price Prediction project! This repository contains the code and resources for predicting real estate prices based on date, bedroom count, and district using Long Short-Term Memory (LSTM) neural networks. By leveraging advanced deep learning techniques, and aim to forecast property prices and provide insights for informed decision-making in the real estate market.

## Project Overview 🔍
This project is designed to predict real estate prices by analyzing historical data. employing a four-stage approach, starting with data collection through web scraping, followed by data preprocessing, exploratory data analysis (EDA) and visualization, and finally, machine learning (ML) model development using LSTM.

## Language Used
- Python: The primary programming language used for scripting, data processing, and developing machine learning models.

## Dataset 📊
collecting the dataset using web scraping techniques, specifically Selenium, to extract data from dynamic, JavaScript-rendered websites. The dataset includes features such as date, number of bedrooms, and district. After collection, the data is cleaned and preprocessed to remove outliers and prepare it for modeling.

## Project Stages

### Data Collection
- **Tool Used:** Selenium Library
- **Description:** To automate the data extraction process using Selenium to handle dynamic content and complex website interactions, ensuring accurate and comprehensive data collection.

### Data Preprocessing
- **Tools Used:** Pandas, Numpy, OneHotEncoder (sklearn)
- **Description:** Data cleaning and transformation are performed to prepare the dataset for analysis. To remove outliers, handle missing values, and encode categorical variables into a numerical format suitable for machine learning.

### Exploratory Data Analysis & Visualization
- **Tools Used:** Matplotlib, Seaborn, Power BI
- **Description:** EDA is conducted to uncover patterns and trends in the data. And visualize these insights using interactive dashboards to enhance understanding and communication.

### Machine Learning Model Development
- **Tools Used:** Keras, LSTM, Dense, Dropout, Adam Optimizer, Scikit-learn
- **Description:** To build and train an LSTM model to handle the time-series nature of the data. The model is fine-tuned using techniques such as regularization and hyperparameter tuning. Model evaluated using various performance metrics and visualize the predicted prices against actual prices.

## Evaluation and Results 📈
After training the model, evaluate its performance on the testing dataset using metrics such as Mean Squared Error (MSE) and Mean Absolute Error (MAE). Also visualize the predicted prices against the actual prices to assess the model's accuracy and reliability.
