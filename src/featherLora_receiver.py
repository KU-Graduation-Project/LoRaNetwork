import json
import threading
import time
from datetime import datetime
import socket

import serial
import struct
import sqlite3


# feather M0 LoRa receiver(COM7)
# receive data from feather M0 transmitter and save it to db/send it to ulory socket
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
serial_port = make_port('/dev/ttyACM1')


# open socket client
Host = '127.0.0.1'
Port = 9999
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((Host, Port))


conn = sqlite3.connect("////home/pi/Downloads/marin/src/oceanlab")
# if no sensordata.db make sensordata.db
global cur
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS sensor_data(ID INTEGER PRIMARY KEY AUTOINCREMENT, data text)')

conn.commit()



def receive_data(serial_port):
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    if serial_port.readable():
        data = serial_port.readline()[:-4]  #remove '/r/n'
        print("receive data: ", timestamp, " / ", data)
        save_data(data)
    return



def save_data(bytedata):
    data = bytedata.decode('utf-8')
    
    if(len(data)>4):
        null_data = None
        strings = data.split(',', 2)
        did = strings[1]
        
        cur.execute("SELECT uid FROM user WHERE did = '%s'" % did)
        data = data +","+ str(cur.fetchall())[3:-4]
        cur.execute("SELECT name FROM user WHERE did = '%s'" % did)
        data = data +","+ str(cur.fetchall())[3:-4]
        
        client_socket.sendall(data.encode('utf-8'))
        cur.execute("INSERT INTO sensor_data VALUES(?,?)", (null_data, data))
        conn.commit()



while True:
    receive_data(serial_port)
    time.sleep(0.1)

client_socket.close()

