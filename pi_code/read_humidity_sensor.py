# Complete Project Details: https://RandomNerdTutorials.com/raspberry-pi-dht11-dht22-python/
# Based on Adafruit_CircuitPython_DHT Library Example

import time
import board
import adafruit_dht

# Sensor data pin is connected to GPIO 4
# run dir(board) for pin list which maps to GPIO pinout. 
# ex) GPIO 2 = SDA  or D2 (data 2)
# ex) GPIO 8 = CEO  or D8 (data 8)
# ex) GPIO 9 = MISO or D9 (data 9)
sensor = adafruit_dht.DHT11(board.D4)


while True:
    try:
        # Print the values to the serial port
        temperature_c = sensor.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = sensor.humidity
        print("Temp={0:0.1f}ºC, Temp={1:0.1f}ºF, Humidity={2:0.1f}%".format(temperature_c, temperature_f, humidity))

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    
    except Exception as error:
        sensor.exit()
        raise error

    time.sleep(30.0)