import datetime
from sklearn.preprocessing import MinMaxScaler

import pandas as pd
import numpy as np

class DataPreprocessing:
    def __init__(self):
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def preprocess_data(self,data : pd.DataFrame ,look_back = 100 )  :
        """ This preocess will process the data for model traning.."""
        df=data.copy()
        
        #scaling the data 
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data=scaler.fit_transform(df[["Close"]])

        #creating new features.
        global X,y
        X,y=[],[]
        for i in range(len(scaled_data)-look_back-1):
            features=scaled_data[i : (look_back + i)]
            target=scaled_data[look_back+i]

            X.append(features)
            y.append(target)

        return np.array(X),np.array(y) ,scaler 
    
    def inverse_transform(self, scaled_data):
        """Inverse scaling for the predictions."""
        return self.scaler.inverse_transform(scaled_data)



