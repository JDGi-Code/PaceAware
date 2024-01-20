# Pacing Detection mHealth Application

# This file runs the live classifier.

# Text Color
from colorama import Fore
# Play Sound
from playsound import playsound

from datetime import datetime
import json
import pandas as pd
from flask import Flask, request
import logging

from pandas.errors import SettingWithCopyWarning

from pacing_detection import classify_live_window

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

# CONSTANTS
ALLOWED_SENSORS = ['accelerometer', 'magnetometer']
WINDOW_SIZE = 10  # seconds
UPDATE_FREQ_MS = 100
alert_file = "C:\\Users\\jgi\\school\\cs328\\final-project-jgi\\alert.wav"

rows = []
row_count = 0
data_pkts = 0

app = Flask(__name__)

# Flask Logging Setters
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
log = logging.getLogger('flask')
log.setLevel(logging.ERROR)


@app.route("/data", methods=["POST"])
def data():  # listens to the data streamed from the sensor logger

    global row_count, data_pkts
    global rows

    if str(request.method) == "POST":
        data = json.loads(request.data)

        row = {}
        for d in data['payload']:

            if d['name'] not in ALLOWED_SENSORS:
                continue

            row['time'] = [datetime.fromtimestamp(d['time'] / 1000000000)]

            if d['name'] == 'accelerometer':
                row['accel_x'] = [d['values']['x']]
                row['accel_y'] = [d['values']['y']]
                row['accel_z'] = [d['values']['z']]

            elif d['name'] == 'magnetometer':
                row['magno_x'] = [d['values']['x']]
                row['magno_y'] = [d['values']['y']]
                row['magno_z'] = [d['values']['z']]

            rows.append(pd.DataFrame().from_dict(row))
            row_count += 1

    data_pkts += 1
    if data_pkts % WINDOW_SIZE == 0:
        classify()
        row_count = 0
        data_pkts = 0

    return "success"


@app.route("/classify", methods=["POST"])
def classify():
    df = pd.concat(rows, ignore_index=True)
    window = df.iloc[-row_count:]
    window.reset_index()
    result = classify_live_window(window)
    if result == ['not_pacing']:
        print(Fore.GREEN + 'Detecting...')
    else:
        playsound(alert_file)
        print(Fore.YELLOW + 'CAUTION: Pacing Detected')


if __name__ == "__main__":
    print('Server running...')
    app.run(port=8000, host="0.0.0.0")