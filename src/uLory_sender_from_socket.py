import socket
from datetime import datetime

import serial
import struct
import sqlite3
import time

# uLory sender(COM4/COM6)
# byte_size : data size

Host = '127.0.0.1'
Port = 9999
ADDR = (Host, Port)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)  # address binding
server_socket.listen()  # ready to accept client

conn = sqlite3.connect("////home/pi/Downloads/marin/src/oceanlab")
global cur
cur = conn.cursor()

def make_port(port_name):
    ser = serial.Serial(
        port=port_name,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        timeout=0.5
    )

    ser.isOpen()
    print('uLory sender port open')

    return ser

def send_data(data):
    serial_port.write(data)


# Running Port
serial_port = make_port('/dev/ttyUSB0')


def conn_req():
    conn_msg = "conn_req"
    msg = conn_msg.encode('utf-8')
    print("send:",msg)
    serial_port.write(msg)
    time.sleep(0.5)


# Monitor system request connect
while True:
    conn_req()
    if serial_port.readable():
        data = serial_port.readline()
        print("received:", data)
        msg = data.decode('utf-8')
        if "conn_ack" in msg:
            break

isInfoSet = False
def info_req():
    info_msg = "info_req"
    msg = info_msg.encode('utf-8')
    print(msg)
    serial_port.write(msg)


# Monitor system request user info
while True:
    info_req()
    if serial_port.readable():
        data = serial_port.readline()
        msg = data.decode('utf-8')
        print("received:", msg)
        #info_ack[('did', 'uid', 'name'), ('did', 'uid', 'name')]
        if "info_ack" in msg:
            if "[(" in msg:
                split_info = msg.split('), (')
                split_info[0] = split_info[0][2:]
                split_info[-1] = split_info[-1][:-2]
                for user in split_info:
                    print("user_info:", user)
                    strings = user.split(',', 3)
                    did = strings[0][2:-1]
                    uid = strings[1][2:-1]
                    name = strings[2][2:-1]
                    print("did:", did, ", uid:", uid, ", name:", name)
                    cur.execute("INSERT INTO user(did, uid, name) VALUES('"+did+"', '"+uid+"', '"+name+"')")
                    conn.commit()
                isInfoSet = True
                while msg != 'info_set_complete':
                    info_res = "info_set"
                    res = info_res.encode('utf-8')
                    serial_port.write(res)
                    print(res)
                    time.sleep(0.6)
                    
                    data = serial_port.readline()
                    print("received:", data)
                    msg = data.decode('utf-8')
                break
    if isInfoSet is True:
        break
          
client_socket, client_addr = server_socket.accept() #accept incoming client
while True:
    data = client_socket.recv(64)  # 클라이언트가 보낸 메시지  
    if not data:
            # if data is not received
            continue
    send_data(data)
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    print(timestamp, " received :", data)
    #time.sleep(0.5)

client_socket.close()
server_socket.close()

