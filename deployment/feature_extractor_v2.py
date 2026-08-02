import numpy as np


def extract_features(sensor_data, rssi):

    # ----------------------------------
    # Magnitudes
    # ----------------------------------

    mags = [
        sensor_data["sensor1"]["magnitude"],
        sensor_data["sensor2"]["magnitude"],
        sensor_data["sensor3"]["magnitude"],
        sensor_data["sensor4"]["magnitude"],
    ]

    features = {}

    # ----------------------------------
    # Individual Sensor Magnitudes
    # ----------------------------------

    for i in range(4):
        features[f"mag_{i+1}"] = mags[i]

    # ----------------------------------
    # Individual XYZ values
    # ----------------------------------

    for i in range(4):

        sensor = sensor_data[f"sensor{i+1}"]

        features[f"x_{i+1}"] = sensor["x"]
        features[f"y_{i+1}"] = sensor["y"]
        features[f"z_{i+1}"] = sensor["z"]

    # ----------------------------------
    # Global Statistics
    # ----------------------------------

    features["avg_mag"] = np.mean(mags)
    features["max_mag"] = np.max(mags)
    features["min_mag"] = np.min(mags)

    features["range_mag"] = np.max(mags) - np.min(mags)

    features["std_mag"] = np.std(mags)

    # ----------------------------------
    # Spatial Features
    # ----------------------------------

    left = (mags[0] + mags[2]) / 2
    right = (mags[1] + mags[3]) / 2

    top = (mags[0] + mags[1]) / 2
    bottom = (mags[2] + mags[3]) / 2

    diag1 = mags[0] - mags[3]
    diag2 = mags[1] - mags[2]

    features["left_right_diff"] = left - right
    features["top_bottom_diff"] = top - bottom

    features["diag1_diff"] = diag1
    features["diag2_diff"] = diag2

    # ----------------------------------
    # Strongest Sensor
    # ----------------------------------

    features["strongest_sensor"] = np.argmax(mags) + 1

    # ----------------------------------
    # RSSI
    # ----------------------------------

    features["rssi"] = rssi

    return features


if __name__ == "__main__":

    from sensor_reader_v2 import get_all_sensors, get_rssi

    sensors = get_all_sensors()

    features = extract_features(sensors, get_rssi())

    print("\nExtracted Features:\n")

    for key, value in features.items():
        print(f"{key:20} : {value}")
