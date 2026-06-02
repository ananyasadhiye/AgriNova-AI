import joblib
import numpy as np

model = joblib.load("models/crop_model.pkl")

def recommend_crop(n,p,k,ph,rain):

    temp = 25
    humidity = 70

    data = np.array([[n,p,k,temp,humidity,ph,rain]])

    pred = model.predict(data)

    return pred[0]