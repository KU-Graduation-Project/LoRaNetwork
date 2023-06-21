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


# Running Port
serial_port = make_port('/dev/ttyUSB0')

isInfoSet = False
def info_req():
    info_msg = "info_req"
    msg = info_msg.encode('utf-8')
    print(msg)
    serial_port.write(msg)

# Monitor system request user info
for i in range(5):
    info_req()
    time.sleep(0.4)

# Monitor system receive user info
while True:
    #info_req()
    if serial_port.readable():
        if isInfoSet is True:
            break
        data = serial_port.readline()
        msg = data.decode('utf-8')
        print("received:", msg)
        #info_ack[('did', 'uid', 'name'), ('did', 'uid', 'name')]
        if "info_ack" in msg:
            if "[(" in msg:
                split_info = msg.split('), (')
                split_info[0] = split_info[0][10:]
                split_info[-1] = split_info[-1][:-2]
                for user in split_info:
                    print("user_info:", user)
                    strings = user.split(',', 3)
                    did = strings[0][1:-1]
                    uid = strings[1][2:-1]
                    name = strings[2][2:-1]
                    print("did:", did, " uid:", uid, " name:", name)
                    cur.execute("INSERT INTO user(did, uid, name) VALUES('"+did+"', '"+uid+"', '"+name+"')")
                    conn.commit()
                isInfoSet = True

          
client_socket, client_addr = server_socket.accept() #accept incoming client
while True:
    data = client_socket.recv(64)  # 클라이언트가 보낸 메시지  
    if not data:
            # if data is not received
            continue
    serial_port.write(data)
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    print(timestamp, " send :", data)

client_socket.close()
server_socket.close()

