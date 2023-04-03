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
conn = sqlite3.connect("////home/pi/Downloads/marin/src/sensordata")
# if no sensordata.db make sensordata.db
global cur
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS sensor_data(ID INTEGER PRIMARY KEY AUTOINCREMENT, data text)')

conn.commit()
    
    
#make_db()


def receive_data(serial_port):
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    if serial_port.readable():
        data = serial_port.readline()
        save_data(data)
        print("receive data: ", timestamp, " / ", data)
    return



def save_data(bytedata):
    data = bytedata.decode('utf-8')
    
    if(len(data)>10):
        null_data = None
        cur.execute("INSERT INTO sensor_data VALUES(?,?)", (null_data, data))
        conn.commit()



while True:
    if serial_port.readable():
        data = serial_port.readline()
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        save_data(data)
        print("receive data: ", timestamp, " / ", data)
    '''
    receive_data(serial_port)
    time.sleep(0.1)
    '''

