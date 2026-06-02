import pandas as pd

# Load datasets
rain = pd.read_csv("datasets/rainfall.csv")
temp = pd.read_csv("datasets/temp.csv")
pest = pd.read_csv("datasets/pesticides.csv")
yield_data = pd.read_csv("datasets/yield.csv")

# -----------------------
# CLEAN DATA
# -----------------------

# Fix rainfall column names
rain.columns = rain.columns.str.strip()
rain = rain.rename(columns={
"Area":"Area",
"Year":"Year",
"average_rain_fall_mm_per_year":"Rainfall"
})

# Fix temperature
temp = temp.rename(columns={
"year":"Year",
"country":"Area",
"avg_temp":"Temperature"
})

# Fix pesticides
pest = pest[["Area","Year","Value"]]
pest = pest.rename(columns={"Value":"Pesticides"})

# Fix yield
yield_data = yield_data[["Area","Year","Value"]]
yield_data = yield_data.rename(columns={"Value":"Yield"})

# -----------------------
# MERGE DATASETS
# -----------------------

data = rain.merge(temp,on=["Area","Year"],how="inner")
data = data.merge(pest,on=["Area","Year"],how="inner")
data = data.merge(yield_data,on=["Area","Year"],how="inner")

# Save dataset
data.to_csv("datasets/crop_dataset.csv",index=False)

print("✅ Dataset merged successfully")
print(data.head())