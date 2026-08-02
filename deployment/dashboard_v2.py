from oled_display import show_result
from sensor_reader_v2 import get_all_sensors, get_rssi
from feature_extractor_v2 import extract_features
from ai_engine_v2 import predict_object

import time
import os


def get_risk(prediction):

    prediction = prediction.lower()

    safe = [
        "empty",
        "spoon",
        "fork"
    ]

    suspicious = [
        "keys",
        "usb_adapter",
        "battery"
    ]

    threat = [
        "knife",
        "screwdriver",
        "scissors"
    ]

    if prediction in safe:
        return "SAFE"

    elif prediction in suspicious:
        return "SUSPICIOUS"

    elif prediction in threat:
        return "THREAT"

    return "UNKNOWN"


def confidence_status(conf):

    if conf >= 95:
        return "VERY HIGH"

    elif conf >= 85:
        return "HIGH"

    elif conf >= 70:
        return "MEDIUM"

    return "LOW"


def sensor_bar(value, max_value):

    length = 25

    filled = int((value / max_value) * length)

    return "█" * filled + "-" * (length - filled)


while True:

    os.system("clear")

    sensors = get_all_sensors()

    features = extract_features(
        sensors,
        get_rssi()
    )

    prediction, confidence = predict_object(features)

    risk = get_risk(prediction)

    mags = [
        sensors["sensor1"]["magnitude"],
        sensors["sensor2"]["magnitude"],
        sensors["sensor3"]["magnitude"],
        sensors["sensor4"]["magnitude"]
    ]

    max_mag = max(mags)

    strongest = mags.index(max_mag) + 1

    print("=" * 65)
    print("        AIRPORT AI THREAT DETECTION SYSTEM V2.0")
    print("=" * 65)

    print()

    print(f"OBJECT DETECTED : {prediction.upper()}")

    print(f"THREAT LEVEL    : {risk}")

    print(f"CONFIDENCE      : {round(confidence,2)} %")

    print(f"MODEL STATUS    : {confidence_status(confidence)}")

    print()

    print("-" * 65)

    print(f"STRONGEST SENSOR : SENSOR {strongest}")

    print("-" * 65)

    for i in range(4):

        print(
            f"S{i+1}  "
            f"{sensor_bar(mags[i], max_mag)} "
            f"{round(mags[i],1)}"
        )

    print("-" * 65)

    print()

    print("GLOBAL FEATURES")

    print(f"Average Magnitude : {round(features['avg_mag'],2)}")

    print(f"Range             : {round(features['range_mag'],2)}")

    print(f"Std Deviation     : {round(features['std_mag'],2)}")

    print(f"RSSI              : {get_rssi()} dBm")

    print()

    if risk == "THREAT":

        print("🚨 ACTION : STOP AND INSPECT LUGGAGE")

    elif risk == "SUSPICIOUS":

        print("⚠ ACTION : MANUAL VERIFICATION")

    else:

        print("✓ ACTION : CLEAR")

    print()

    print("=" * 65)

    time.sleep(2)
show_result(prediction, risk)
