import json
import threading
import time
from datetime import datetime
import socket

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

# open socket client
# send data to web
Host = '127.0.0.1'
Port = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((Host, Port))


# Running Port
serial_port = make_port('COM5')

# Receiving Data, Thread 1, this function read byte data from serial port and save in datalist
# ser : serial port
# datalist : global memory for sharing data with other threads

def receive_data(serial_port):
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    if serial_port.readable():
        res = serial_port.readline()
        print("receive data: ", timestamp, " / ", res)
        client_socket.sendall(res)
    return


while True:
    # ser.write(b'check serial data')
    # print(serial_port.readline())

    receive_data(serial_port)
    time.sleep(0.1)


client_socket.close()