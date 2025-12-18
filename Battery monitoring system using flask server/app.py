from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

battery_data = {
    "voltage": 0.0,
    "percentage": 0,
    "charging": False,
    "timestamp": "--"
}

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/update", methods=["POST"])
def update():
    global battery_data
    data = request.json

    battery_data["voltage"] = data.get("voltage", 0)
    battery_data["percentage"] = data.get("percentage", 0)
    battery_data["charging"] = data.get("charging", False)
    battery_data["timestamp"] = datetime.now().strftime("%H:%M:%S")

    return jsonify({"status": "OK"})

@app.route("/data")
def data():
    return jsonify(battery_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)