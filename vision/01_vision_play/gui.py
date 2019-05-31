# Python Tkinter Scale和LabeledScale用法 http://c.biancheng.net/view/2509.html
# python tkinter可以使用的颜色 - wjcaiyf的专栏 - CSDN博客 https://blog.csdn.net/wjciayf/article/details/79261005

import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

import tkinter as tk
from tkinter import Frame
from classify import Classify
import config

class GUI(Frame):
    
    def __init__(self, master, **kw):
        Frame.__init__(self, master, **kw)
        frame = Frame(master, height=692+10, width=803+20, bg="Chocolate")
        frame.place(x=(720-692-10)/2, y=(840-803-10)/2)


        # # 串口设置相关变量
        # self.armbot = Armbot()

        # # 创建画布，放置机械臂背景图
        # self.ca = tk.Canvas(frame, 
        #                     background='white',
        #                     width=803,
        #                     height=692)
        # self.bm = tk.PhotoImage(file="./images/armbot.gif")
        # self.ca.place(x=(720-692-10)/2, y=(840-803-10)/2, width=803, height=692)
        # self.ca.create_image(803/2 + 1, 692/2 + 1, image=self.bm)

        # # 创建滑动条，速度
        # self.scs = tk.Scale(frame, 
        #                     label='speed',                    # 设置标签内容
        #                     from_=500,                        # 设置最大值
        #                     to=9999,                          # 设置最小值
        #                     orient=tk.HORIZONTAL,             # 设置水平方向
        #                     length=200,                       # 设置轨道的长度
        #                     width=10,                         # 设置轨道的宽度
        #                     showvalue=True,                   # 设置显示当前值
        #                     troughcolor='crimson',            # 设置轨道的背景色
        #                     variable=self.armbot.speed,       # 设置绑定变量
        #                     sliderlength=12,                  # 设置滑块的长度
        #                     sliderrelief=tk.FLAT,             # 设置滑块的立体样式
        #                     tickinterval=5000,                # 设置指示刻度细分
        #                     resolution=50,                    # 设置步长
        #                     bg='Lavenderblush',               # 设置背景颜色
        #                     command=self.set_speed)           # 设置绑定事件处理，函数或方法
        # self.scs.place(x=50, y=50)
        # self.scs.set(self.armbot.speed)

        # # 创建滑动条，舵机1
        # self.servo1_v = config.INIT_POS[1]
        # self.sc1 = tk.Scale(frame, 
        #                     label='servo1',                   # 设置标签内容
        #                     from_=500,                        # 设置最大值
        #                     to=2000,                          # 设置最小值
        #                     orient=tk.HORIZONTAL,             # 设置水平方向
        #                     length=200,                       # 设置轨道的长度
        #                     width=10,                         # 设置轨道的宽度
        #                     showvalue=True,                   # 设置显示当前值
        #                     troughcolor='blue',               # 设置轨道的背景色
        #                     variable=self.servo1_v,           # 设置绑定变量
        #                     sliderlength=12,                  # 设置滑块的长度
        #                     sliderrelief=tk.FLAT,             # 设置滑块的立体样式
        #                     tickinterval=1500/3,              # 设置指示刻度细分
        #                     resolution=1,                     # 设置步长
        #                     bg='LightCyan',                   # 设置背景颜色
        #                     command=self.servo1_to_pos)       # 设置绑定事件处理，函数或方法
        # self.sc1.place(x=255, y=600)
        # self.sc1.set(self.servo1_v)

        # # 创建滑动条，舵机2
        # self.servo2_v = config.INIT_POS[2]
        # self.sc2 = tk.Scale(frame, 
        #                     label='servo2',                   # 设置标签内容
        #                     from_=1800,                       # 设置最大值
        #                     to=2200,                          # 设置最小值
        #                     orient=tk.HORIZONTAL,             # 设置水平方向
        #                     length=200,                       # 设置轨道的长度
        #                     width=10,                         # 设置轨道的宽度
        #                     showvalue=True,                   # 设置显示当前值
        #                     troughcolor='gold',               # 设置轨道的背景色
        #                     variable=self.servo2_v,           # 设置绑定变量
        #                     sliderlength=12,                  # 设置滑块的长度
        #                     sliderrelief=tk.FLAT,             # 设置滑块的立体样式
        #                     tickinterval=400/4,               # 设置指示刻度细分
        #                     resolution=1,                     # 设置步长
        #                     bg='lightyellow',                 # 设置背景颜色
        #                     command=self.servo2_to_pos)       # 设置绑定事件处理，函数或方法
        # self.sc2.place(x=115, y=310)
        # self.sc2.set(self.servo2_v)
        
        # # 创建滑动条，舵机3
        # self.servo3_v = config.INIT_POS[3]
        # self.sc3 = tk.Scale(frame, 
        #                     label='servo3',                   # 设置标签内容
        #                     from_=700,                        # 设置最大值
        #                     to=1600,                          # 设置最小值
        #                     orient=tk.HORIZONTAL,             # 设置水平方向
        #                     length=200,                       # 设置轨道的长度
        #                     width=10,                         # 设置轨道的宽度
        #                     showvalue=True,                   # 设置显示当前值
        #                     troughcolor='orangeRed',          # 设置轨道的背景色
        #                     variable=self.servo3_v,           # 设置绑定变量
        #                     sliderlength=12,                  # 设置滑块的长度
        #                     sliderrelief=tk.FLAT,             # 设置滑块的立体样式
        #                     tickinterval=900/3,               # 设置指示刻度细分
        #                     resolution=1,                     # 设置步长
        #                     bg='LavenderBlush',               # 设置背景颜色
        #                     command=self.servo3_to_pos)       # 设置绑定事件处理，函数或方法
        # self.sc3.place(x=600, y=260)
        # self.sc3.set(self.servo3_v)

        # # 创建单选钮，气泵
        # self.var = tk.StringVar()
        # self.var.set('Stop')
        # self.label = tk.Label(frame, text="AIR PUMP: "+self.var.get(), bg='palegreen', font=('Arial', 10), width=25, height=2)
        # self.label2 = tk.Label(frame, text=" ", bg='palegreen', font=('Arial', 10), width=25, height=2)
        # self.label.place(x=550, y=545)
        # self.label2.place(x=550, y=545+35)
        
        # self.r1 = tk.Radiobutton(frame, text='Suck', variable=self.var, value='Suck', bg='forestgreen', command=self.airpump)
        # self.r2 = tk.Radiobutton(frame, text='Blow', variable=self.var, value='Blow', bg='forestgreen', command=self.airpump)
        # self.r3 = tk.Radiobutton(frame, text='Stop', variable=self.var, value='Stop', bg='forestgreen', command=self.airpump)
        # self.r1.place(x=555, y=580)
        # self.r2.place(x=625, y=580)
        # self.r3.place(x=695, y=580)


        # 添加菜单
        menubar = tk.Menu(master)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade (label='File', menu=filemenu)

        filemenu.add_separator ()
        filemenu.add_command (label='Exit', command=master.quit)
        master.config (menu=menubar)

    # def airpump(self):
    #     self.label.config(text="AIR PUMP: "+self.var.get())
    #     if self.var.get() == "Suck":
    #         # print("Suck")
    #         self.armbot.go_air_pump(signal=config.PUMP_SUCK)
    #     elif self.var.get() == "Blow":
    #         self.armbot.go_air_pump(signal=config.PUMP_BLOW)
    #     elif self.var.get() == "Stop":
    #         self.armbot.go_air_pump(signal=config.PUMP_STOP)

    # def set_speed(self, v):
    #     print("speed set ", v)
    #     self.armbot.speed = v

    # def servo1_to_pos(self, value1):
    #     print("servo1 to ", value1)
    #     self.armbot.one_servo_to_pos(servo_id=1, servo_pos=int(value1))

    # def servo2_to_pos(self, value2):
    #     print("servo2 to ", value2)
    #     self.armbot.one_servo_to_pos(servo_id=2, servo_pos=int(value2))

    # def servo3_to_pos(self, value3):
    #     print("servo3 to ", value3)
    #     self.armbot.one_servo_to_pos(servo_id=3, servo_pos=int(value3))



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Serial GUI")
    root.geometry("840x730")
    app = GUI(root)
    root.mainloop()



