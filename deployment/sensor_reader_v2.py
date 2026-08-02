from smbus2 import SMBus
import subprocess
import re
import math
import time

MUX_ADDR = 0x70
QMC_ADDR = 0x0D

bus = SMBus(1)

# ------------------------
# Select MUX Channel
# ------------------------
def select_channel(channel):
    bus.write_byte(MUX_ADDR, 1 << channel)
    time.sleep(0.05)


# ------------------------
# Initialize one QMC
# ------------------------
def init_qmc():

    bus.write_byte_data(QMC_ADDR, 0x0B, 0x01)
    bus.write_byte_data(QMC_ADDR, 0x09, 0x1D)

    time.sleep(0.05)


# ------------------------
# Read signed 16-bit value
# ------------------------
def read_word(reg):

    low = bus.read_byte_data(QMC_ADDR, reg)
    high = bus.read_byte_data(QMC_ADDR, reg + 1)

    value = (high << 8) | low

    if value > 32767:
        value -= 65536

    return value


# ------------------------
# Read one sensor
# ------------------------
def read_sensor(channel):

    select_channel(channel)
    init_qmc()

    x = read_word(0x00)
    y = read_word(0x02)
    z = read_word(0x04)

    magnitude = math.sqrt(x*x + y*y + z*z)

    return {
        "x": x,
        "y": y,
        "z": z,
        "magnitude": magnitude
    }


# ------------------------
# Read all four sensors
# ------------------------
def get_all_sensors():

    data = {}

    for i in range(4):
        data[f"sensor{i+1}"] = read_sensor(i)

    return data


# ------------------------
# WiFi RSSI
# ------------------------
def get_rssi():

    try:

        output = subprocess.check_output(
            "iw dev wlan0 link",
            shell=True
        ).decode()

        match = re.search(r"signal:\s*(-\d+)", output)

        if match:
            return int(match.group(1))

    except:
        pass

    return -100


# ------------------------
# Test
# ------------------------
if __name__ == "__main__":

    sensors = get_all_sensors()

    for name, value in sensors.items():

        print("--------------------------------")

        print(name)

        print("X :", value["x"])
        print("Y :", value["y"])
        print("Z :", value["z"])
        print("Magnitude :", round(value["magnitude"],2))

    print("--------------------------------")
    print("RSSI :", get_rssi())
