from sklearn.linear_model import LinearRegression
import numpy as np

def predict_price(prices):

    if len(prices) < 2:
        return prices[0]

    X = np.arange(len(prices)).reshape(-1,1)
    y = np.array(prices)

    model = LinearRegression()
    model.fit(X,y)

    future = np.array([[len(prices)+1]])

    prediction = model.predict(future)

    return round(prediction[0],2)