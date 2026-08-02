import csv
import os

from sensor_reader_v2 import get_all_sensors, get_rssi
from feature_extractor_v2 import extract_features

# -------------------------
# Dataset File
# -------------------------

DATASET_FILE = "dataset_v2.csv"

# -------------------------
# Create file if not exists
# -------------------------

if not os.path.exists(DATASET_FILE):

    with open(DATASET_FILE, "w", newline="") as f:

        writer = csv.writer(f)

        headers = list(extract_features(get_all_sensors(), get_rssi()).keys())
        headers.append("label")

        writer.writerow(headers)

print("="*50)
print(" AIRPORT AI DATA COLLECTION V2 ")
print("="*50)

label = input("\nEnter Object Label : ").strip().lower()

samples = int(input("Number of Samples : "))

print("\nMove the object before every capture.")
print("Press ENTER to capture each sample.\n")

# -------------------------
# Collect Data
# -------------------------

for i in range(samples):

    input(f"Sample {i+1}/{samples} -> Press ENTER")

    sensors = get_all_sensors()

    features = extract_features(
        sensors,
        get_rssi()
    )

    row = list(features.values())
    row.append(label)

    with open(DATASET_FILE, "a", newline="") as f:

        writer = csv.writer(f)
        writer.writerow(row)

    print("✓ Saved")

print("\nDataset collection completed!")
