from machine import I2C, Pin
from ina219 import INA219
import network
import time
import urequests

# =========================
# WiFi Credentials
# =========================
WIFI_SSID = "ISILAB CR"
WIFI_PASS = "isilab.ncut.CR"

# =========================
# Flask Server
# =========================
SERVER_URL = "http://192.168.50.204:5000/update"   # CHANGE IP

# =========================
# INA219 Setup
# =========================
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
ina = INA219(i2c=i2c)
ina.configure()

# =========================
# WiFi Connection
# =========================
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print(" Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(0.5)

    print(" WiFi connected:", wlan.ifconfig()[0])
    return wlan

# =========================
# Battery Percentage
# =========================
def battery_percentage(voltage):
    min_v = 3.0
    max_v = 4.2
    pct = int((voltage - min_v) / (max_v - min_v) * 100)
    return max(0, min(100, pct))

# =========================
# Read & Average Voltage (20 samples)
# =========================
def read_average_voltage(samples=20):
    total = 0
    for i in range(samples):
        v = ina.voltage()
        print("Reading", i + 1, ":", v, "V")
        total += v
        time.sleep(0.1)   # slightly faster sampling

    avg = total / samples
    return round(avg, 3)

# =========================
# Send to Flask Server
# =========================
def send_to_server(voltage):
    percent = battery_percentage(voltage)

    payload = {
        "voltage": voltage,
        "percentage": percent,
        "charging": False
    }

    try:
        r = urequests.post(SERVER_URL, json=payload)
        r.close()
        print(" Sent to server:", payload)
    except Exception as e:
        print(" Server send failed:", e)

# =========================
# MAIN LOOP
# =========================
connect_wifi()

while True:
    avg_voltage = read_average_voltage(20)
    print(" Average Voltage:", avg_voltage, "V")

    send_to_server(avg_voltage)

    print(" Waiting 2 seconds...\n")
    time.sleep(2)
