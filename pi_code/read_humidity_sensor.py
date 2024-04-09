# Complete Project Details: https://RandomNerdTutorials.com/raspberry-pi-dht11-dht22-python/
# Based on Adafruit_CircuitPython_DHT Library Example

import time
import board
import adafruit_dht
import json 
from flask import Flask

# Sensor data pin is connected to GPIO 4
# run dir(board) for pin list which maps to GPIO pinout. 
# ex) GPIO 2 = SDA  or D2 (data 2)
# ex) GPIO 8 = CEO  or D8 (data 8)
# ex) GPIO 9 = MISO or D9 (data 9)

app = Flask(__name__)

sensor = adafruit_dht.DHT11(board.D4)

@app.route("/")
def home():
    return 'home'

@app.route("/metrics")
def metrics():
    global sensor
    humidity_data = {}
    try:
        # Print the values to the serial port
        temperature_c = sensor.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = sensor.humidity
    
        humidity_data["humidity"] = humidity
        humidity_data["temperature"] = temperature_f
    
        print("Temp={0:0.1f}ºC, Temp={1:0.1f}ºF, Humidity={2:0.1f}%".format(temperature_c, temperature_f, humidity))
        # return humidity_data

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        return f"RuntimeError: {error.args[0]}", 503
        # continue

    except Exception as error:
        return f"Error:{str(error)}", 503
        # sensor.exit()
        # raise error # do you really want to exit?

    return humidity_data
    
app.run('0.0.0.0', port=5001, debug=False)