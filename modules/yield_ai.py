import pickle

model=pickle.load(open("models/yield_model.pkl","rb"))

def predict_yield(rain, temp, pesticide):

    pred = model.predict([[rain, temp, pesticide]])

    return round(pred[0], 2)