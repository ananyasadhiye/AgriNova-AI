import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv("datasets/Crop_recommendation.csv")

X = data.drop("label", axis=1)
y = data["label"]

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

model = RandomForestClassifier()

model.fit(X_train,y_train)

joblib.dump(model,"models/crop_model.pkl")

print("Model trained and saved")