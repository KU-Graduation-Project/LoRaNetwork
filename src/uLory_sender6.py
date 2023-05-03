import json
import time
from datetime import datetime
from random import randint

import serial
import struct

# uLory sender(COM4/COM6)
# byte_size : data size
def make_port(port_name, baud_rate, byte_size):
    if byte_size == 8:
        bs = serial.EIGHTBITS

    ser = serial.Serial(
        port=port_name,
        baudrate=baud_rate,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        timeout=0.02
    )

    ser.isOpen()
    print('sender port open')

    return ser

def send_data(data):
    serial_port.write(data)

## Running port
serial_port = make_port('COM6', 9600, 8)


while True:
    deviceId = "2897"
    randNumber = randint(-360, 360)
    randNumber1 = randint(90, 120)
    randNumber2 = randint(90, 120)
    randNumber3 = randint(35, 38)
    # randNumber = 4
    now = datetime.now()
    timestamp = now.strftime('%H:%M:%S')
    data = bytearray(str(deviceId)+" "+str(timestamp)+" "+ str(randNumber)+" "+ str(randNumber)+" "+str(randNumber)
                                     +" "+str(randNumber)+" "+ str(randNumber)+" "+str(randNumber)+" "+str(randNumber1)+" "+str(randNumber2)+" "+str(randNumber3), encoding='utf-8')

    #ax,ay,az,gx,gy,gz,heartrate,resp,temp
    send_data(data)
    print(timestamp, " / ", data)
    time.sleep(2)

