import pandas as pd
import joblib
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score

from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression


# ----------------------------
# Load Dataset
# ----------------------------
df = pd.read_csv("data/upgraded_final_resume_dataset.csv")

print("Initial dataset shape:", df.shape)


# ----------------------------
# Data Cleaning
# ----------------------------

# Remove duplicates
df = df.drop_duplicates()

# Fill missing values
df = df.fillna(df.mean(numeric_only=True))

print("Dataset after cleaning:", df.shape)


# ----------------------------
# Remove Outliers
# ----------------------------

df = df[df["resume_length"] < 1500]


# ----------------------------
# Feature Selection
# ----------------------------
X = df[
    [
        "skills_count",
        "resume_length",
        "experience_score",
        "achievement_score",
        "job_match_score"
    ]
]

y = df["final_resume_score"]


# ----------------------------
# Train Test Split
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])


# ----------------------------
# Model Comparison
# ----------------------------

models = {
    "Random Forest": RandomForestRegressor(random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42),
    "Linear Regression": LinearRegression()
}

results = {}

print("\nModel Performance\n")

for name, model in models.items():

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    r2 = r2_score(y_test, preds)

    rmse = np.sqrt(mean_squared_error(y_test, preds))

    mae = mean_absolute_error(y_test, preds)

    results[name] = r2

    print(name)
    print("R2 Score:", round(r2,4))
    print("RMSE:", round(rmse,4))
    print("MAE:", round(mae,4))
    print("---------------------")


# ----------------------------
# Hyperparameter Tuning
# ----------------------------

print("\nTuning Random Forest...\n")

rf = RandomForestRegressor(random_state=42)

param_grid = {
    "n_estimators": [100,200,300],
    "max_depth": [10,15,20],
    "min_samples_split": [2,5]
}

grid = GridSearchCV(
    rf,
    param_grid,
    cv=5,
    scoring="r2",
    n_jobs=-1
)

grid.fit(X_train, y_train)

best_model = grid.best_estimator_

print("Best Parameters:", grid.best_params_)


# ----------------------------
# Cross Validation
# ----------------------------

cv_scores = cross_val_score(
    best_model,
    X,
    y,
    cv=5,
    scoring="r2"
)

print("Cross Validation Scores:", cv_scores)
print("Mean CV Score:", cv_scores.mean())


# ----------------------------
# Final Evaluation
# ----------------------------

predictions = best_model.predict(X_test)

print("\nFinal Model Performance")

print("R2 Score:", r2_score(y_test, predictions))

print("RMSE:", np.sqrt(mean_squared_error(y_test, predictions)))

print("MAE:", mean_absolute_error(y_test, predictions))


# ----------------------------
# Feature Importance
# ----------------------------

importance = best_model.feature_importances_

features = X.columns

print("\nFeature Importance")

for f, i in zip(features, importance):

    print(f, ":", round(i,3))


# ----------------------------
# Save Model
# ----------------------------

joblib.dump(best_model, "models/resume_model.pkl")

print("\nModel saved successfully!")