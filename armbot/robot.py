#coding=utf-8
import sys
import time
sys.path.append(r".\armbot")

from com import ComThread
from model import model_pre, model_solve
import config

class Armbot(ComThread):

    _instance = None
    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = ComThread.__new__(cls, *args, **kw)
        return cls._instance
    
    def __init__(self, port = 'COM6'):
        super(Armbot, self).__init__()
        self.port = port
        self.dict_servo = {1:1467, 2:1500, 3:1400, 4:1500, 5:1500}
        self.speed = config.SPEEDRATE
        self.start()

    # servo
    def reset_all_servo(self):
        print("reset all servos.")
        d=bytes.fromhex('23 31 50 32 30 30 30 23 32 50 32 30 30 30 23 33 50 31 35 30 30 23 34 50 31 32 30 30 23 35 50 31 35 30 30 54 31 30 30 30 0D 0A')
        self.l_serial.write(d)
        return self.get_ok()
    
    def one_servo_to_pos(self, servo_id, servo_pos):
        print("servo %d get to position %d" % (servo_id, servo_pos))
        d = '#' + str(servo_id) + 'P' + str(servo_pos) + 'T' + str(self.speed) + '\r\n'
        print("command: ", d)
        self.l_serial.write(d.encode())
        return self.get_ok()

    def servos_to_pos(self, dict_servo):
        d = ''
        for i in range(1,6):
            print("servo %d get to position %d" % (i, dict_servo[i]))
            d += '#' + str(i) + 'P' + str(dict_servo[i]) 
        d += 'T' + str(self.speed) + '\r\n'
        print("command: ", d)
        self.l_serial.write(d.encode())
        return self.get_ok()

    # go
    def go_air_pump(self, signal = 0):
        print("go_air_pump")
        if signal == 0: # 停止
            d = '#4P1200#5P1500T' + str(self.speed) + '\r\n'
        if signal == 1: # 吸气
            d = '#4P1800#5P1200T' + str(self.speed) + '\r\n'
        if signal == 2: # 吹气
            d = '#4P1800#5P1800T' + str(self.speed) + '\r\n'
        print("d:", d)
        self.l_serial.write(d.encode())
        return self.get_ok()
    
    def go_ready(self):
        d = '#1P2000#2P2000#3P1500T' + str(self.speed) + '\r\n'
        print("d:", d)
        self.l_serial.write(d.encode())
        return self.get_ok()

    def go_to_pos(self, x, y, z):
        dl, theta1 = model_pre(x, y)
        s1 = int(1467 + theta1*75/9)
        theta3, theta2 = model_solve(dl, dh=z)
        if theta3 == 0:
            print('no ans!!!')
            return 0
        s3 = int(1400 - (theta3-90)*100/9)
        s2 = int(1500 + (theta2-180)*100/9)
        d = '#1P' + str(s1) + '#2P' + str(s2) + '#3P' + str(s3) + 'T' + str(self.speed) + '\r\n'
        print("d:", d)
        self.l_serial.write(d.encode())
        time.sleep(0.5)
        return self.get_ok() 

    # 机械臂走子：吃子 拿子 落子
    def move(self, alist = None, capture = False, capture_pos = None, isShow = False):
        # 计算新旧位置
        [new_x, new_y, last_x, last_y] = alist
        
        # # 吃子的情况
        # if capture:
        #     idx = self.pieceboard_id
        #     self.pieceboard_id += 1
        #     (x, y) = config.CHESSBOARD[new_id]
        #     pos = (x, y, 135)
        #     self.go_door_move( 30, pos)
        #     self.isMoveOver(x, y, 135, 1)
        #     self.go_air_pump(config.PUMP_SUCK)
        #     time.sleep(0.5)
        #     (x, y) = config.PIECEBOARD[idx]
        #     pos = (x, y, 132)
        #     self.go_door_move( 30, pos)
        #     self.isMoveOver(x, y, 132, 1)
        #     self.go_air_pump(config.PUMP_STOP)

        self.go_to_pos(last_x, last_y, z=10)
        time.sleep(0.5)
        self.go_to_pos(last_x, last_y, z=-2)
        time.sleep(1)
        self.go_air_pump(signal=1)
        time.sleep(1)
        self.go_to_pos(last_x, last_y, z=10)
        time.sleep(0.5)
        self.go_to_pos(new_x, new_y, z=10)
        time.sleep(1)
        self.go_air_pump(signal=2)
        time.sleep(1)
        self.go_air_pump(signal=0)
        self.go_ready()
        if isShow:
            print("move done.")


if __name__ == '__main__':
    myarm = Armbot()
    temp_a = 0
    while(temp_a != 99):
        temp_a = int(input('input the action:'))
        if temp_a == 1:
            myarm.reset_all_servo()
        elif temp_a == 5:
            input_x = int(input('input the id:'))
            input_y = int(input('input the pos:'))
            myarm2 = Armbot()
            # print(id(myarm))
            # print(id(myarm2))
            myarm2.one_servo_to_pos(input_x, input_y)
        elif temp_a == 6:
            input_s = int(input('input the signal:'))
            myarm.go_air_pump(input_s)
        elif temp_a == 7:
            input_x = int(input('input the x:'))
            input_y = int(input('input the y:'))
            input_z = int(input('input the z:'))
            myarm.go_to_pos(input_x, input_y, input_z)
            
        elif temp_a == 9:
            input_last_x = float(input('input the last_x:'))
            input_last_y = float(input('input the last_y:'))
            input_new_x = int(input('input the new_x:'))
            input_new_y = int(input('input the new_y:'))
            alist = [input_new_x, input_new_y, input_last_x, input_last_y]
            myarm.move(alist)


