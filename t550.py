#!/usr/bin/python3
from __future__ import print_function
import serial, time
import os
import paho.mqtt.client as paho
import json

ser = serial.Serial(os.environ['ULTRAHEAT_USB_DEVICE'], baudrate=300, bytesize=7, parity="E", stopbits=1, timeout=2, xonxoff=0, rtscts=0)

#send init message
packet = bytearray()
for i in range(0, 40):
    packet.append(0x00)
print(len(packet))
ser.write(packet)

#send request message
ser.write("/?!\x0D\x0A".encode())
ser.flush();
time.sleep(.5)

#send read identification message
print(ser.readline())

#change baudrate
ser.baudrate=2400

meter_total_kwh = 0

try:
    #read data message
    while True:
        response = ser.readline().decode()
        print(response, end="")
        if "6.8(" in response:
            value, unit = response.split("(")[1].split(")")[0].split("*")
            if unit == "kWh":
                meter_total_kwh = int(value)
            elif unit == "MWh":
                meter_total_kwh = int(float(value) * 1000)
            else:
                print("Unknown unit!")
                break
        if "!" in response:
            break
finally:
    ser.close()

print("meter_total_kwh: " + str(meter_total_kwh))
client=paho.Client("ultraheat")
client.connect(os.environ['ULTRAHEAT_MQTT_BROKER'])
data = '{"total_kwh": ' + str(meter_total_kwh) + '}'
print(data)
if meter_total_kwh != 0:
    client.publish("ultraheat/district_heating_meter", data)
client.disconnect()
