import json
import time
from datetime import datetime
from random import randint

import serial
import struct

# uLory sender(COM4/COM6)
# byte_size : data size
def make_port(port_name, baud_rate, byte_size):
    if byte_size == 8:
        bs = serial.EIGHTBITS

    ser = serial.Serial(
        port=port_name,
        baudrate=baud_rate,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        timeout=0.02
    )

    ser.isOpen()
    print('sender port open')

    return ser

def send_data(data):
    serial_port.write(data)

## Running port
serial_port = make_port('COM4', 9600, 8)

'''
while True:
    jsondata = bytearray(json.dumps({"set": "initial set"}), encoding='utf-8')
    send_data(jsondata)
    #time.sleep(1)
    res = serial_port.readline()
    print(" / ", res)
    if res == b'{"tick": "4"}':
        break
'''

while True:
    user = "user4"
    #randNumber = randint(0, 360)
    randNumber = 4
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    jsondata = bytearray(json.dumps({"user": user, "timestamp": str(timestamp), "data": randNumber}), encoding='utf-8')
    send_data(jsondata)
    print("data sent: ", timestamp, " / ", randNumber)
    time.sleep(2)

