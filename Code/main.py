# Untitled - By: feng_ - 周五 11月 16 2018
import pyb
from pyb import UART
from command import Command
from myuart import Myuart

my_command = Command()
to_screen = Myuart()
to_ctrlboard = Myuart()

#读取要控制电机的
while True:
    #读取一个命令       
    if(to_screen.getbufferlen()):                              #如果串口有数据，进行下一步
        order_head = ord(to_screen.read1char())                #读取命令头
        print(order_head)
        if order_head == 0x55:                                 #如果命令头正确即为0x55,继续读取后续命令
            order_code = ord(to_screen.read1char())            #读取命令内容
            print(order_code)
            if order_code == 0x08:
                stepper_No = ord(to_screen.read1char())
                if stepper_No == 0x01:
                    to_ctrlboard.uartdef(1)
                elif stepper_No == 0x02:
                    to_ctrlboard.uartdef(2)
                elif stepper_No == 0x03:
                    to_ctrlboard.uartdef(3)
                else:
                    to_screen.sendstring(my_command.to_page_order_error)
                    to_screen.sendlist(my_command.screen_order_end)
                    continue
                to_screen.sendstring(my_command.to_page_run_stepper)
                to_screen.sendlist(my_command.screen_order_end)
            elif order_code == 0x01:
                to_ctrlboard.sendlist(my_command.up1mm)
            elif order_code == 0x02:
                to_ctrlboard.sendlist(my_command.down1mm)
            elif order_code == 0x03:
                to_ctrlboard.sendlist(my_command.up1cm)
            elif order_code == 0x04:
                to_ctrlboard.sendlist(my_command.down1cm)
            elif order_code == 0x05:
                my_command.start_stepper[2] = to_screen.read1char()
                my_command.start_stepper[3] = to_screen.read1char()
                my_command.start_stepper[4] = to_screen.read1char()
                my_command.start_stepper[5] = to_screen.read1char()
                my_command.start_stepper[6] = to_screen.read1char()
                to_ctrlboard.sendlist(my_command.start_stepper)
            elif order_code == 0x06:
                to_ctrlboard.sendlist(my_command.stop_stepper)
            elif order_code == 0x09:
                to_ctrlboard.sendlist(my_command.getremaintimes)
                delay(10)
                while (to_ctrlboard.getbufferlen()):
                    if(ord(to_ctrlboard.read1char()) == 0x55):
                        to_screen.sendstring(my_command.to_page_running_state)
                        to_screen.sendlist(my_command.screen_order_end)
                        remain_times = 'remain_times.val=' + str(to_ctrlboard.read1char)
                        to_screen.sendstring(remain_times)
                        to_screen.sendlist(my_command.screen_order_end)
            else:
                to_screen.sendstring(my_command.to_page_order_error)
                to_screen.senddata(my_command.screen_order_end)
                continue
    
to_screen.readall()

#读取控制参数
while True:
    if(to_screen.getbufferlen()):                              #如果串口有数据，进行下一步
        order_head = ord(to_screen.read1char())                #读取命令头
        print(order_head)
        if order_head == 0x55:                                 #如果命令头正确即为0x55,继续读取后续命令
            order_code = ord(to_screen.read1char())            #读取命令内容
            print(order_code)
            if code_order == 1:
                to_ctrlboard.sendlist(my_command.up1mm)
            elif code_order == 2:
                to_ctrlboard.sendlist(my_command.down1mm)
            elif code_order == 3:
                to_ctrlboard.sendlist(my_command.up1cm)
            elif code_order == 4:
                to_ctrlboard.sendlist(my_command.down1cm)
            else:
                    to_screen.sendstring(my_command.to_page_order_error)
                    to_screen.senddata(my_command.screen_order_end)
                    continue
            else:
                to_screen.sendstring(my_command.to_page_order_error)
                to_screen.senddata(my_command.screen_order_end)
                continue

'''
DISTANCELONG = 28
DISTANCESHORT = 10
speed = 30
cycles = 100
my_command = Command()
to_screen = Myuart()
to_screen.uartdef(0)

#print(my_command.up1mm)

#选择要控制电机
while True:
    stepper_num = int(input('请输入要控制的电机编号（1、2、3）：'))
    if(stepper_num != 1 and stepper_num !=2 and stepper_num !=3):
        print('电机编号输入错误，请重新输入!')
        continue
    else:
        break

to_ctrlboard = Myuart()
to_ctrlboard.uartdef(stepper_num)

#改变电机位置
fine_tuning = input('是否进行电机位置调整（y/n）：')
if fine_tuning == 'y':
    print('1:上移1mm\n2:下移1mm\n3:上移1cm\n4:下移1cm\n5:退出\n')
    while True:
        code_order = int(input('请输入指令：'))
        if code_order == 1:
            to_ctrlboard.senddata(my_command.up1mm)
        elif code_order == 2:
            to_ctrlboard.senddata(my_command.down1mm)
        elif code_order == 3:
            to_ctrlboard.senddata(my_command.up1cm)
        elif code_order == 4:
            to_ctrlboard.senddata(my_command.down1cm)
        elif code_order == 5:
            break
        else:
            print('指令错误！')

#改变运动模式
mode_change = input('是否改变运动模式（y/n)：')
if mode_change == 'y':
    while True:
        DISTANCELONG = int(input('请输入第一阶段运动的距离（mm）：'))
        DISTANCESHORT = int(input('请输入第二阶段运动的距离（mm）：'))
        if DISTANCESHORT > DISTANCELONG:
            print('第二阶段的距离应小于第一阶段！')
            continue
        else:
            break


#输入运行速度
while True:
    speed = int(input('请输入运动速度（1-50mm/s:）'))
    if(speed <= 0 or speed > 60):
        continue
    else:
        break
#输入运行次数
while True:
    cycles = int(input('请输入运行次数（1-500）：'))
    if(cycles <= 0 or cycles >500):
        continue
    else:
        break

my_command.start_stepper[2] = speed
if(cycles <= 255):
    my_command.start_stepper[4] = 0
    my_command.start_stepper[3] = cycles
else:
    my_command.start_stepper[4] = 1
    my_command.start_stepper[3] = cycles - 256
my_command.start_stepper[5] = DISTANCELONG
my_command.start_stepper[6] = DISTANCESHORT

to_ctrlboard.senddata(my_command.start_stepper)
'''