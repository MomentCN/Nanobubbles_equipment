# main.py -- put your code here!
import pyb
import sys
from pyb import UART

ONECYCLE2DIS = 10   #电机转动一周前进的距离单位：mm
DIV = 1000   #设置步数，电机转动一周前进10mm，需走DIV步
DISTANCE1 = 24   #设置第一阶段运动距离mm
DISTANCE2 = 10  #设置第二阶段运动的距离
UPDOWNSTEPS = 10    #设置加减速运动的步数

stepPin = pyb.Pin(pyb.Pin.board.X1, pyb.Pin.OUT_PP) #脉冲输出口设置为X1
dirPin = pyb.Pin(pyb.Pin.board.X2, pyb.Pin.OUT_PP)  #方向口设置为X2
enPin = pyb.Pin(pyb.Pin.board.X3, pyb.Pin.OUT_PP)   #使能口设置为X3

onestep = ONECYCLE2DIS / DIV #计算每步的前进距离，单位mm

uartRead = UART(1, 9600)

'''
#direction:方向1往下，0往上
'''
def testStepper():
    while True:
        stepPin.value(1)
        pyb.udelay(5000)
        stepPin.value(0)
        pyb.udelay(5000)

def stepper1mm(direction):
    steps = 1 / onestep
    dirPin.value(direction)
    pyb.udelay(20)
    while steps > 0:
        stepPin.value(1)
        pyb.udelay(500)
        stepPin.value(0)
        pyb.udelay(500)
        steps = steps - 1

def stepper1cm(direction):
    steps = 10 / onestep
    dirPin.value(direction)
    pyb.udelay(20)
    while steps > 0:
        stepPin.value(1)
        pyb.udelay(500)
        stepPin.value(0)
        pyb.udelay(500)
        steps = steps - 1

def runStepper1time(direction, upspeed, steps, halfperiod, downspeed):
    dirPin.value(direction)
    pyb.udelay(20)
    for i in upspeed:
        stepPin.value(1)
        pyb.udelay(i)
        stepPin.value(0)
        pyb.udelay(i)
    while steps > 0:
        stepPin.value(1)
        pyb.udelay(halfperiod)
        stepPin.value(0)
        pyb.udelay(halfperiod)
        steps = steps - 1
    for i in downspeed:
        stepPin.value(1)
        pyb.udelay(i)
        stepPin.value(0)
        pyb.udelay(i)

while True:
    if(uartRead.any()):
        order_head = ord(uartRead.read(1))          #读取命令头
        print(order_head)
        pyb.udelay(1000)
        if order_head == 0x55:                      #如果命令头正确即为0x55,继续读取后续命令
            order_code = ord(uartRead.read(1))      #读取命令内容
            print(order_code)
            if(order_code == 0x01):                 #上升1mm指令
                pyb.LED(4).on()
                stepper1mm(0)
                pyb.LED(4).off()
            elif(order_code == 0x02):               #下降1mm指令
                pyb.LED(4).on()
                stepper1mm(1)
                pyb.LED(4).off()
            elif(order_code == 0x03):               #上升1cm指令
                pyb.LED(4).on()
                stepper1cm(0)
                pyb.LED(4).off()
            elif(order_code == 0x04):               #下降1cm指令
                pyb.LED(4).on()
                stepper1cm(1)
                pyb.LED(4).off()
            elif(order_code == 0x05):               #运动设定指令
                stepperSpeed = ord(uartRead.read(1))                 #读取速度设定
                print(stepperSpeed)
                stepperTimes1 = ord(uartRead.read(1))                #读取次数设定低八位
                print(stepperTimes1)
                stepperTimes2 = ord(uartRead.read(1))                #读取速度设定高八位
                print(stepperTimes2)
                DISTANCE1 = ord(uartRead.read(1))                    #读取长运动距离设定
                print(DISTANCE1)
                DISTANCE2 = ord(uartRead.read(1))                    #读取短运动距离设定
                print(DISTANCE2)
                stepperTimes = stepperTimes2 * 256 + stepperTimes1   #计算总运动次数
                sumsteps1 = DISTANCE1 // onestep #第一阶段运动的总步数，既为脉冲的个数
                sumsteps2 = DISTANCE2 // onestep #第二阶段运动的总步数，既为脉冲的个数
                unispeedsteps1 = sumsteps1 - 2 * UPDOWNSTEPS         #计算第一阶段匀速运动的步数
                unispeedsteps2 = sumsteps2 - 2 * UPDOWNSTEPS         #计算第二阶段匀速运动的步数
                halfperiod = int(onestep * 1000 * 1000 / stepperSpeed // 2) #计算脉冲半周期
                upspeed = []     #加速脉冲间隔序列
                downspeed = []   #减速脉冲间隔序列
                for i in range(UPDOWNSTEPS):
                    upspeed.append((UPDOWNSTEPS-i) * halfperiod)
                for i in range(UPDOWNSTEPS):
                    downspeed.append((i + 1) * halfperiod)
                for i in range(stepperTimes):
                    ########发送剩余次数#########
                    remain_times = stepperTimes - i
                    order_send = 'remain_times.val=' + str(remain_times)
                    print(order_send)
                    uartRead.write(order_send)
                    uartRead.writechar(0xff)
                    uartRead.writechar(0xff)
                    uartRead.writechar(0xff)
                    ############end#############
                    ########执行运动设定#########
                    runStepper1time(1, upspeed, unispeedsteps1 , halfperiod, downspeed)
                    for j in range(10):
                        runStepper1time(0, upspeed, unispeedsteps2, halfperiod, downspeed)
                        runStepper1time(1, upspeed, unispeedsteps2, halfperiod, downspeed)
                    runStepper1time(0, upspeed, unispeedsteps1, halfperiod, downspeed)
                    ############end#############
                    while(uartRead.any()):
                        order_head = ord(uartRead.read(1))
                        print(order_head)
                        if order_head == 0x55:
                            order_code = ord(uartRead.read(1))
                            print(order_code)
                            if order_code == 0x06:
                                pyb.hard_reset()


