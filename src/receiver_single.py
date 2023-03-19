import json
import threading
import time
from datetime import datetime

import serial
import struct


# ioLory receiver(COM5)
# Making serial port
# port_name : Using port name
def make_port(port_name):
    ser = serial.Serial(
        port=port_name,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        timeout=0.05
    )
    ser.isOpen()
    print('receiver open')

    return ser


# Receiving Data, Thread 1, this function read byte data from serial port and save in datalist
# ser : serial port
# datalist : global memory for sharing data with other threads

def receive_data(serial_port):
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    if serial_port.readable():
        res = serial_port.readline()
        if res == b'{"set": "initial set"}':
            set_tick()
        print("receive data: ", timestamp, " / ", res)
    return


def save_data(data, byte_data):
    intData = int.from_bytes(byte_data[0], "big")
    floatData = struct.unpack('f', byte_data[1])
    charData = byte_data[2].decode("utf-8")
    new_data = {
        'intData': intData,
        'floatData': floatData[0],
        'charData': charData
    }

    data = data.append(new_data, ignore_index=True)
    threading.Timer(1, save_data, [data, byte_data]).start()
    # print(data)
    return data


def set_tick():
    tick_data = bytearray(json.dumps({"tick": tick}), encoding='utf-8')
    serial_port.write(tick_data)


# Running Port
serial_port = make_port('COM5')
tick = 1

while True:
    # ser.write(b'check serial data')
    # print(serial_port.readline())
    receive_data(serial_port)
    if tick == 9:
        tick == 1
    else:
        tick += 1
    time.sleep(0.1)
