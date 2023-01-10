##Read File 
import serial
import time
import threading
import os

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

class multiReceive:
    def __init__(self):
        self.nport = 0
        self.serial_array = []
    
    def add_port(self, ser):
        self.serial_array.append(ser)
        self.nport += 1
    
    def send(self):
        end = True
        while(end) :
            for ser in self.serial_array:
                if ser.inWaiting() :
                    self.out += ser.read(1)
                
                if self.out == 'Q' :
                    end = False
                    break
                    
ser1 = make_port('COM4')
ser2 = make_port('COM5')

mr = multiReceive()
mr.add_port(ser1)
mr.add_port(ser2)

receive_thread = threading.Thread( target=mr.send )
receive_thread.start()

