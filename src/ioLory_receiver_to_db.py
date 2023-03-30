import json
import threading
import time
from datetime import datetime
import socket

import serial
import struct
import sqlite3


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

# Running Port
serial_port = make_port('/dev/ttyUSB0')

def make_db():
    conn = sqlite3.connect("////home/pi/Downloads/marin/src/sensordata")
    # if no sensordata.db make sensordata.db
    global cur
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS sensor_data(ID INTEGER PRIMARY KEY AUTOINCREMENT, data json)')
    conn.commit()

make_db()


def receive_data(serial_port):
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    if serial_port.readable():
        data = serial_port.readline()
        save_data(data)
        print("receive data: ", timestamp, " / ", data)
    return


def save_data(jsondata):
    data = jsondata.decode('utf-8')
    decoded_data = json.dumps(data)
    null_data = None
    
    cur.execute("INSERT INTO sensor_data(ID, data) VALUES(NULL,'"+decoded_data+"')")
    return



while True:
    receive_data(serial_port)
    time.sleep(0.1)

