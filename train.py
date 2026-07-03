import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Simple dataset
data = {
    "sleep_hours": [5, 6, 7, 8, 4, 9, 6, 7],
    "stress": [8, 6, 4, 3, 9, 2, 7, 5],
    "exercise": [0, 10, 30, 40, 0, 50, 20, 30],
    "quality": ["Poor", "Average", "Good", "Good", "Poor", "Good", "Average", "Good"]
}

df = pd.DataFrame(data)

X = df[["sleep_hours", "stress", "exercise"]]
y = df["quality"]

model = RandomForestClassifier()
model.fit(X, y)

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print("✅ Model created successfully!")