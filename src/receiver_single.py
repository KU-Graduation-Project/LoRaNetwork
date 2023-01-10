import threading
import serial
import time
import pandas as pd
import struct

#Making serial port
#port_name : Using port name
def make_port(port_name):
    ser = serial.Serial(
        port=port_name,
        baudrate=9600,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize= serial.EIGHTBITS
    )
    ser.isOpen()

    return ser

#Receiving Data, Thread 1, this function read byte data from serial port and save in datalist
#ser : serial port
#datalist : global memory for sharing data with other threads
#
def receive_data (ser, datalist) :
    threading.Timer(1, receive_data, [ser, byte_data]).start()

    if ser.readable() > 0:
        for i in range(len(datalist)) :
            datalist[i] = ser.read()

    print(datalist)
    #Test
    i = 5
    datalist[0] = i.to_bytes(4, 'big')
    datalist[1] = struct.pack('f', 0.5)
    datalist[2] = bytes('a', 'utf-8')

    return

def save_data (data, byte_data) :
    intData = int.from_bytes(byte_data[0], "big")
    floatData = struct.unpack('f', byte_data[1])
    charData =  byte_data[2].decode("utf-8")
    new_data = {
        'intData' : intData,
        'floatData' : floatData[0],
        'charData' : charData
    }
    # print(new_data)

    data = data.append(new_data, ignore_index= True)
    threading.Timer(1, save_data, [data, byte_data]).start()
    print(data)
    return data

# class repeatTimer(timer) :



#Running Part
#Setting Data,Port
ser = make_port('COM4')
data_ex = {
    'intData' : [10],
    'floatData' : [36.5],
    'charData' : ['h']
}
data = pd.DataFrame(data_ex, columns = ['intData', 'floatData', 'charData'])
y = 0.264
i = 184
c = 'g'
bi = i.to_bytes(4,'big')
by = struct.pack('f', y)
bc = bytes(c, 'utf-8')
byte_data = [bi, by, bc]

t1 = threading.Timer(1, receive_data, [ser, byte_data])
#receive -> save data로 바로 , receive&save 같이
#graph thread만
t2 = threading.Timer(1, save_data, [data, byte_data])

t1.start()
time.sleep(0.5)
t2.start()

time.sleep(5)
print(byte_data)


print("end")

