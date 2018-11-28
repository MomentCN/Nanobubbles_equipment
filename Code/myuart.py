import pyb
from pyb import UART

class Myuart: 

    myserial = UART(1, 9600)

    def __init__(self):
        self.myserial = UART(1, 9600)
    
    def uartdef(self, No):
        if(No == 1):
            self.myserial = UART(4, 9600)
        elif(No == 2):
            self.myserial = UART(2, 9600)
        elif(No == 3):
            self.myserial = UART(3, 9600)
        elif(No == 0):
            self.myserial = UART(1, 9600)
        else:
            print('电机编号错误！')
    
    def sendlist(self, data):
        for char in data:
            self.myserial.writechar(char)
    
    def sendstring(self, data):
        self.myserial.write(data)

    def send1char(self, data)
        self.writechar(data)

    def getbufferlen(self):
        bufferlen = self.myserial.any()
        return bufferlen
    
    def read1char(self):
        tempchar = self.myserial.read(1)
        return tempchar

    def readall(self):
        tempdata = self.myserial.readall()
        return tempdata