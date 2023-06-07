import json
import threading
import time
from datetime import datetime
import socket

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


# open socket client
# send data to web
Host = '127.0.0.1'
Port = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((Host, Port))

# Running Port
serial_port = make_port('COM4')

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
        client_socket.sendall(res)
    return


isConnected = False


# uLory(Raspberry Pi)-ioLory(Monitor system) initial connect
# ioLory DID must be set as uLory sender
def conn_ack():
    global isConnected
    if serial_port.readable():
        res = serial_port.readline()
        data = res.decode()

        if data == 'conn_req':
            print("received:", data)
            ack_msg = 'conn_ack'
            msg = ack_msg.encode('utf-8')
            while data != 'info_req':
                print("sent:", msg)
                time.sleep(0.6)
                serial_port.write(msg)
                if serial_port.readable():
                    res = serial_port.readline()
                    data = res.decode()
            isConnected = True


while True:
    if isConnected is False:
        conn_ack()
    if isConnected is True:
        print("conn_ack break")
        break

isInfoSet = False


# get user info from db
# send back to uLory sender
def send_user_info():
    global isInfoSet
    if serial_port.readable():
        res = serial_port.readline()
        data = res.decode('utf-8')
        if "-2, " in data:
            isInfoSet = True
        if data == 'info_req':
            print("received:", data)
            while data != 'info_set':

                cur.execute("SELECT * FROM user")
                user_data = "info_ack" + str(cur.fetchall())
                encoded_user_data = user_data.encode('utf-8')
                print("sent:", encoded_user_data)
                serial_port.write(encoded_user_data)

                '''
                # user_info = "{{1, 01, one}, {2, 02, two}, {3, 03, three}, {4, 04, four}, {5, 05, five}, {6, 06, six}, {7, 07, seven}, {8, 08, eight}, {9, 09, nine}}"
                user_info = "info_ack{{1, 01, one}, {2, 02, two}, {3, 03, three}, {4, 04, four}, {5, 05, five}, {6, 06, six}}"
                encoded_user_info = user_info.encode()
                serial_port.write(encoded_user_info)
                '''
                if serial_port.readable():
                    res = serial_port.readline()
                    data = res.decode()
                    print('received:', data)
                time.sleep(1)


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