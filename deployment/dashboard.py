from sensor_reader import get_magnetometer, get_rssi
from feature_extractor import extract_features
from ai_engine import predict_threat

import time

# OLED Imports
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw

# OLED Setup
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

while True:

    samples = []

    for i in range(20):
        samples.append(get_magnetometer())
        time.sleep(0.1)

    features = extract_features(samples, get_rssi())

    prediction, confidence = predict_threat(features)

    # Terminal Output
    print("\n========================")
    print("FEATURES:")
    print(features)
    print("\nPREDICTION:", prediction)
    print("CONFIDENCE:", round(confidence, 2), "%")
    print("========================")

    # OLED Display
    image = Image.new("1", (128, 32))
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), prediction, fill=255)
    draw.text((0, 16), f"{round(confidence,1)}%", fill=255)

    oled.fill(0)
    oled.image(image)
    oled.show()

    time.sleep(2)
