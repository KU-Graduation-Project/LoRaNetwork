import time
import serial
import numpy as np
import threading
import struct

# uLory sender(COM4)
# portName : COM4
# byte_size : data size
def make_port(port_name, rate, byte_size):
    if byte_size == 8:
        bs = serial.EIGHTBITS

    ser = serial.Serial(
        port=port_name,
        baudrate=9600,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize= serial.EIGHTBITS
    )

    ser.isOpen()
    print('port open')

    return ser

def send_data(datalist, receive_port) :
    if receive_port.isOpen() :
        for data in datalist :
            receive_port.write(data)
            print(data)

#draw graph main 참고 하여 import 후 작성
def draw_graph(a) :
    print("graph: "+a)
    return


## Running port
serial_port = make_port('COM4', 9600, 8)
receive_port = make_port('COM3', 9600, 8)

#Make Data

#send_data
while True :
    y = 0.755
    i = 1
    c = 'e'
    bi = i.to_bytes(4, 'big')
    by = struct.pack('f', y)
    bc = bytes(c, 'utf-8')
    data = [bi, by, bc]
    send_data(data, receive_port)
    time.sleep(3)


#receiving_thread = threading.Thread(target=receive_data, args=(receive_port, arr))
receiving_thread = threading.Thread(target=draw_graph, args=(receive_port, arr))
receiving_thread.start()
threading.Timer(3, receive_data, [receive_port, arr])