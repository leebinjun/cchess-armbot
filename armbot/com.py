'''
1 通信参数
USB转串口(TTL电平)   COM3   波特率9600, 8位数据位, 1位停止位, 无校验位

2 命令格式
命令                                   功能             说明
#STOP\r\n                       |  停止当前动作   |  停止当前所有动作    
#1P1500T100\r\n                 |  控制单个舵机   |  数据 1 是舵机的通道
                                                    数据 1500 是舵机的位置，范围是 500-2500
                                                    数据 100 是执行的时间，表示速度，范围是 100-9999
#1P15001P15001P1500T100\r\n     |  控制多个舵机   |  该命令是同时执行的，也就是所有的舵机都是一起动的

3 注意
\r\n是命令的结束符，必须得有。
所有命令中都不含空格。
\r\n 是 2 个字符，是回车符和换行符，是十六进制数 0x0D 和 0x0A，是 Chr(13) 和 Chr(10) 。
舵机驱动分辨率：0.5us , 0.045 度。

'''
import serial
import threading
import time

class ComThread(object):
    def __init__(self):
    #构造串口的属性
        self.l_serial = None
        self.alive = False
        self.waitEnd = None
        self.port = None
        self.ID = None
        self.data = None

    #查看可用的串口
    def Check_Comx(self):
        import serial.tools.list_ports
        comlist = list(serial.tools.list_ports.comports())
        if len(comlist) <= 0:
            print("Wrong：Not Found Com, Please Check The Connection.")
            return 0
        else:
            return comlist 

   #定义串口等待的函数
    def waiting(self):
        if not self.waitEnd is None:
            self.waitEnd.wait()

    def SetStopEvent(self):
        if not self.waitEnd is None:
            self.waitEnd.set()
        self.alive = False
        # self.stop()

    #启动串口的函数
    def start(self):
        self.l_serial = serial.Serial()
        self.l_serial.port = self.port
        self.l_serial.baudrate = 9600
        #设置等待时间，若超出这停止等待
        self.l_serial.timeout = 2
        self.l_serial.open()
        #判断串口是否已经打开
        if self.l_serial.isOpen() is not True:
            print("serial init failed.")
            exit()
            
    def get_ok(self):
        data = ''
        data = data.encode('utf-8')                        #由于串口使用的是字节，故而要进行转码，否则串口会不识别
        n = self.l_serial.inWaiting()                      #获取接收到的数据长度
        if n: 
            #读取数据并将数据存入data
            data = data + self.l_serial.read(n)
            #输出接收到的数据
            print('get data from serial port:', data)
            return data
        else:
            return None
    
    

if __name__ == "__main__":
    
    myserial = ComThread()
    alist = myserial.Check_Comx()
    print(alist)
    for i in alist:
        print(str(i))

# 复位
#1P1500#2P1500#3P1500#4P1500T1000\r\n



# 按键确认位置
# BB BB 1F 0A 50 01 | 01 00 EC 49 | 01 00 B4 40 | 00 00 94 25 | 01 00 34 41 00 00 43 46 00 00 33 12 00 00 0B 26 4C 

# 空闲未连接状态,
# 发送 BB BB 03 00 01 01 FE, 连接机械臂

# 空闲连接状态,
# 发送 BB BB 03 00 01 00 FF, 断开机械臂连接


# 吸气    BB BB 03 BF 04 01 3C
# 停     BB BB 03 BF 04 00 3D
# 吹气   BB BB 03 BF 04 02 3B
# 速率  
# BB BB 06 42 03 00 00 01 00 BA
# 回零
# BB BB 02 79 04 83
# 任务结束
# BB BB 03 41 03 05 B7
# 任务开始
# BB BB 03 41 03 01 BB


# 连接机械臂
# BB BB 03 00 01 01 FE
# 任务开始
# BB BB 03 41 03 01 BB
# 速率  
# BB BB 06 42 03 00 00 01 00 BA
# 回零(定义在按键位置，门型运动)
# BB BB 12 48 04 00 00 32 00 01 00 EC 49 01 00 B4 40 00 00 94 25 9E
# ptp运动(不好用)
# door运动
# BB BB 12 48 04 00 00 1E 00 00 00 64 00 01 01 90 00 00 00 91 00 0F
# 气泵
# 吸气   BB BB 03 BF 04 01 3C
# 停     BB BB 03 BF 04 00 3D
# 吹气   BB BB 03 BF 04 02 3B
# 任务结束
# BB BB 03 41 03 05 B7
# 断开机械臂连接
# BB BB 03 00 01 00 FF
