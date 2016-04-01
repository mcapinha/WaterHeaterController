import time
import readadc
import datetime
import sqlite3
import plotly.plotly as py
import json

import RPi.GPIO as GPIO

def read_temperature():
    sensor_data = readadc.readadc(SENSOR_PIN,
                                  readadc.PINS.SPICLK,
                                  readadc.PINS.SPIMOSI,
                                  readadc.PINS.SPIMISO,
                                  readadc.PINS.SPICS)

    millivolts = (sensor_data) * (3300.0 / 1024.0)
    temp_C = ((millivolts - 100.0) / 10.0) - 40.0

    # write the data to plotly
    print("mV: %d \t Temp: %.1f" % (millivolts, temp_C) )

    return temp_C


def log_temperature(value):
    global cursor  # , stream
    print('Logging into db: ', value)
    cursor.execute("INSERT INTO logger (temperature) VALUES (?)", (value, ))


def plot_temperature(value):
    print('Plotting to plotly')
    stream.write({'x': datetime.datetime.now(), 'y': value})


# True = off, False = on
def set_relay_state(state):
    state = not state ## Logic is reversed, this makes is easier to compreend
    GPIO.output(RELAY_PIN, state)



with open('./config.json') as config_file:
    config = json.load(config_file)


## Pin definitions
RELAY_PIN = 17
SENSOR_PIN = 0

## Sleep cycle
SLEEP_TIME = 1
SAMPLES = 60
PLOT_EVERY = 5


## Some control damping
MIN_TEMP = 30
MAX_TEMP = 40
SEEN_THRESHOLD = 5


## Variables
counter = 0
total = 0
seen = 0
plot_counter = 0

conn = sqlite3.connect(config['db_path'], isolation_level=None)
cursor = conn.cursor()

## Initializ
readadc.initialize()

py.sign_in(config["plotly_username"], config["plotly_api_key"])
url = py.plot([
    {
        'type': 'scatter',
        'stream': {
            'token': config['plotly_streaming_tokens'][0],
        }
    }], filename=config['plotly_filename'],
    fileopt='extend'
)


stream = py.Stream(config['plotly_streaming_tokens'][0])
stream.open()

GPIO.setup(RELAY_PIN, GPIO.OUT)
set_relay_state(False)  # Alwasy start off

# the main sensor reading and plotting loop
while True:

    counter += 1
    temp_C = read_temperature()
    total += float(temp_C)

    ## Average the taken samples to reduce reading fluctuations
    if counter == SAMPLES:
        avg = round((total / SAMPLES), 1)
        total = 0
        counter = 0
        log_temperature(avg)

        plot_counter += 1

        if plot_counter % PLOT_EVERY:
            plot_temperature(avg)
            plot_counter = 0

        if avg < MIN_TEMP or avg > MAX_TEMP:
            print("Incrementing seen")
            seen = seen + 1
        else:
            print("Resetting seen counter")
            seen = 0

        if seen > SEEN_THRESHOLD:
            print("Seen over threshold, executing")

            if (avg < MIN_TEMP):
                print("Starting heater")
                set_relay_state(True)

            if avg > MAX_TEMP:
                print("Stopping heater")
                set_relay_state(False)

            print("Resetting seen")
            seen = 0

    time.sleep(SLEEP_TIME)
