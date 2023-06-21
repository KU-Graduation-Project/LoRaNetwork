from kafka import KafkaProducer

"ioLory에서 데이터 받아 user별로 카프카에 전달"

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
        if "-2" in data:
            isInfoSet = True
        if data == 'info_req':
            print("received:", data)
            while data != 'info_set':

                cur.execute("SELECT * FROM user")
                user_data = "info_ack" + str(cur.fetchall())
                encoded_user_data = user_data.encode('utf-8')
                print("sent:", encoded_user_data)
                serial_port.write(encoded_user_data)

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
##################################initial connection done

def stream_data():
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    if serial_port.readable():
        sensor_data = serial_port.readline()
        decoded_sensor_data = sensor_data.decode("utf-8")
        strings = decoded_sensor_data.split(",")
        topic = strings[1]
        kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                       value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        kafka_producer.send(topic, decoded_sensor_data)
        print('ioLory in KAFKA out - ' + decoded_sensor_data + ' to ' + topic)



device_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
'''
if __name__ == '__main__':
    # 컨슈머 멀티프로세싱
    pool = multiprocessing.Pool(processes=10)
    pool.map(connect, device_list)
'''

while True:
    print(serial_port.readline())

    stream_data()
    time.sleep(0.1)

client_socket.close()
