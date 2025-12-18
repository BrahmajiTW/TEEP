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
# ThingSpeak
# =========================
API_KEY = "CQHT63634JWO5VAY"
THINGSPEAK_URL = "http://api.thingspeak.com/update"

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
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(0.5)

    print("WiFi connected:", wlan.ifconfig())

# =========================
# Read & Average Voltage
# =========================
def read_average_voltage(samples=50):
    total = 0
    for i in range(samples):
        v = ina.voltage()
        print("Reading", i + 1, ":", v, "V")
        total += v
        time.sleep(0.15)

    avg = total / samples
    return round(avg, 3)

# =========================
# Upload to ThingSpeak
# =========================
def upload_to_thingspeak(voltage):
    url = "{}?api_key={}&field1={}".format(
        THINGSPEAK_URL, API_KEY, voltage
    )
    r = urequests.get(url)
    r.close()
    print("Uploaded:", voltage, "V")

# =========================
# MAIN LOOP
# =========================
connect_wifi()

while True: 
    avg_voltage = read_average_voltage(50)
    print("Average Voltage:", avg_voltage, "V")

    upload_to_thingspeak(avg_voltage)

    print("Waiting 25 seconds...\n")
    time.sleep(25)   # Safe for ThingSpeak
