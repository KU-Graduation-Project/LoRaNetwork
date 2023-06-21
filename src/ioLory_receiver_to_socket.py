import json
import threading
import time
from datetime import datetime
import websocket

import serial
import struct

import mysql.connector


# ioLory receiver(COM5)
# Making serial port
# port_name : Using port namepi
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
serial_port = make_port('COM4')

# open socket client
# send data to web
Host = '127.0.0.1'
Port = 8080

client_socket = websocket.WebSocket()
client_socket.connect('ws://localhost:8080')

conn = mysql.connector.connect(host='localhost',
                               database='oceanlab',
                               user='root',
                               password='12341234')
cur = conn.cursor()


# Receiving Data, Thread 1, this function read byte data from serial port and save in datalist
# ser : serial port
# datalist : global memory for sharing data with other threads

def receive_data(serial_port):
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    if serial_port.readable():
        res = serial_port.readline()
        print("receive data: ", timestamp, " / ", res)
        client_socket.send(res)
    return


isInfoSet = False


# get user info from db
# send back to uLory sender
def send_user_info():
    global isInfoSet
    if serial_port.readable():
        res = serial_port.readline()
        data = res.decode('utf-8')
        if "-" in data:
            print("userinfo break:", data)
            isInfoSet = True
        if data == 'info_req':
            print("received:", data)

            cur.execute("SELECT * FROM user")
            user_info = "info_ack" + str(cur.fetchall())
            encoded_user_info = user_info.encode('utf-8')
            print("sent:", encoded_user_info)
            serial_port.write(encoded_user_info)

            '''
            user_info = "info_ack[('1', '01', 'one'), ('2', '02', 'two'), ('5', '05', 'five'), ('6', '06', 'six')]"
            encoded_user_info = user_info.encode()
            print("sent:", encoded_user_info)
            serial_port.write(encoded_user_info)
            '''
            if serial_port.readable():
                res = serial_port.readline()
                data = res.decode()
                print('received:', data)


while True:
    if isInfoSet is False:
        send_user_info()
    if isInfoSet is True:
        break

while True:
    print(serial_port.readline())

    receive_data(serial_port)
    time.sleep(0.1)

client_socket.close()