from src.scripts.data_fetching import GetData
from src.scripts.data_preprocessing import DataPreprocessing
from src.utils import load_model

import pandas as pd
import numpy as np
from datetime import datetime

class PredictPrice:
    def __init__(self):
        self.model_filepath = "src/model/lstm_model.pkl"
        self.data = GetData()
        self.data_processor = DataPreprocessing()

    def prediction(self, company_ticker, lookback=100, n_prediction =10):
        """THIS WILL PREDICT THE FUTURE DATA AFTER UTILIZING THE PAST DATA"""
        model = load_model(filepath=self.model_filepath)

        df, labels = self.data.get_data(company_ticker, start_date="2020-1-10", end_date="2025-02-10")
        X, y, scaler = self.data_processor.preprocess_data(df)

        if len(X) < lookback:
            raise ValueError(f"Not enough data points! Required: {lookback}, but got: {len(X)}")

        temp_X = list(X[-lookback:].flatten())  # Use only last lookback values
        list_output = []

        i = 0  
        while i < n_prediction:
            if len(temp_X) > lookback:
                input_x = np.array(temp_X[-lookback:]).reshape(1, lookback, 1)  # Ensure correct shape
                yhat = model.predict(input_x, verbose=0)
                temp_X.append(yhat[0][0])  # Append only single value
                list_output.append(yhat[0][0])
            else:
                input_x = np.array(temp_X).reshape((1, lookback, 1))
                yhat = model.predict(input_x, verbose=0)
                temp_X.append(yhat[0][0])
                list_output.append(yhat[0][0])

            i += 1  

        """results=[]
        for i in list_output:
            result = np.array(i).reshape(1,-1)

            results.append(result)"""

        return scaler.inverse_transform(np.array(list_output).reshape(-1,1))

