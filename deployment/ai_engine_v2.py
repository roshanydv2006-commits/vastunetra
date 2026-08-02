import joblib
import pandas as pd

# Load trained model
model = joblib.load("airport_threat_model_v2.pkl")


def predict_object(features):
    """
    Predict object from extracted features.
    Returns:
        prediction (str)
        confidence (float)
    """

    # Convert dictionary to DataFrame
    df = pd.DataFrame([features])

    # Predict class
    prediction = model.predict(df)[0]

    # Predict confidence
    confidence = max(model.predict_proba(df)[0]) * 100

    # Confidence threshold
    if confidence < 47:
        prediction = "unknown"

    return prediction, confidence


if __name__ == "__main__":

    from sensor_reader_v2 import get_all_sensors, get_rssi
    from feature_extractor_v2 import extract_features

    # Read sensors
    sensors = get_all_sensors()

    # Extract features
    features = extract_features(
        sensors,
        get_rssi()
    )

    # Predict
    prediction, confidence = predict_object(features)

    # Display result
    print(f"\nPrediction : {prediction}")
    print(f"Confidence : {confidence:.2f}%")
