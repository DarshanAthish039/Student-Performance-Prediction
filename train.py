import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from xgboost import XGBRegressor



data = pd.read_csv("dataset/student_data.csv")

print("\nDataset loaded successfully!")
print("Number of students:", len(data))



X = data[
    [
        "Attendance",
        "Study_Hours",
        "Previous_Marks",
        "Assignments"
    ]
]

y = data["Final_Score"]




X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)




models = {

    "Linear Regression":
        LinearRegression(),

    "Decision Tree":
        DecisionTreeRegressor(
            max_depth=4,
            random_state=42
        ),

    "Random Forest":
        RandomForestRegressor(
            n_estimators=100,
            max_depth=5,
            random_state=42
        ),

    "Gradient Boosting":
        GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.05,
            max_depth=3,
            random_state=42
        ),

    "XGBoost":
        XGBRegressor(
            n_estimators=100,
            learning_rate=0.05,
            max_depth=3,
            random_state=42,
            objective="reg:squarederror"
        )
}




results = []

best_model = None
best_model_name = None
best_r2 = float("-inf")


print("\n")
print("=" * 65)
print("MODEL COMPARISON")
print("=" * 65)

for name, model in models.items():


    model.fit(X_train, y_train)


    predictions = model.predict(X_test)


    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    results.append({
        "Model": name,
        "MAE": round(mae, 3),
        "MSE": round(mse, 3),
        "R2_Score": round(r2, 3)
    })

    print(f"\n{name}")
    print(f"MAE      : {mae:.3f}")
    print(f"MSE      : {mse:.3f}")
    print(f"R2 Score : {r2:.3f}")

   
    if r2 > best_r2:
        best_r2 = r2
        best_model = model
        best_model_name = name



results_df = pd.DataFrame(results)

print("\n")
print("=" * 65)
print("FINAL MODEL COMPARISON")
print("=" * 65)

print(results_df.to_string(index=False))



print("\n")
print("=" * 65)
print("BEST MODEL")
print("=" * 65)

print("Model :", best_model_name)
print("R2 Score :", round(best_r2, 3))



os.makedirs("models", exist_ok=True)

joblib.dump(
    best_model,
    "models/student_model.pkl"
)

print("\nBest model saved successfully!")
print("Location: models/student_model.pkl")



results_df.to_csv(
    "models/model_comparison.csv",
    index=False
)

print("Model comparison saved successfully!")
print("Location: models/model_comparison.csv")

print("\nTraining completed successfully! 🎉")