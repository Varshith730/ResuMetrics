import joblib
import numpy as np

# ----------------------------
# Load model once
# ----------------------------
MODEL_PATH = "models/resume_model.pkl"

model = joblib.load(MODEL_PATH)


# ----------------------------
# Predict Resume Score
# ----------------------------
def predict_resume_score(features):

    """
    features = {
        "skills_count": int,
        "resume_length": int,
        "experience_score": int,
        "achievement_score": int,
        "job_match_score": float
    }
    """

    feature_list = [
        features["skills_count"],
        features["resume_length"],
        features["experience_score"],
        features["achievement_score"],
        features["job_match_score"]
    ]

    features_array = np.array(feature_list).reshape(1, -1)

    score = model.predict(features_array)[0]

    return round(score, 2)


# ----------------------------
# Convert Score → Label
# ----------------------------
def score_label(score):

    if score < 3:
        return "Poor", "red"

    elif score < 6:
        return "Average", "orange"

    elif score < 8:
        return "Good", "green"

    else:
        return "Excellent", "darkgreen"


# ----------------------------
# Feature Importance (for UI)
# ----------------------------
def get_feature_importance():

    feature_names = [
        "skills_count",
        "resume_length",
        "experience_score",
        "achievement_score",
        "job_match_score"
    ]

    importance = model.feature_importances_

    return dict(zip(feature_names, importance))