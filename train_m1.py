import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
import pickle

# Load dataset
data = pd.read_csv("datasets/yield_df.csv")

# Select required columns
data = data[[
"average_rain_fall_mm_per_year",
"avg_temp",
"pesticides_tonnes",
"hg/ha_yield"
]]

# Rename columns
data.columns = ["Rainfall","Temperature","Pesticides","Yield"]

# Convert to numeric
data = data.apply(pd.to_numeric, errors="coerce")

# Remove missing values
data = data.dropna()

# Features and target
X = data[["Rainfall","Temperature","Pesticides"]]
y = data["Yield"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = GradientBoostingRegressor()

model.fit(X_train, y_train)

# Accuracy
score = model.score(X_test, y_test)
print("Model Accuracy:", score)

# Save model
pickle.dump(model, open("models/yield_model.pkl","wb"))

print("✅ Model trained and saved")