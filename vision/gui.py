# Python Tkinter Scale和LabeledScale用法 http://c.biancheng.net/view/2509.html
# python tkinter可以使用的颜色 - wjcaiyf的专栏 - CSDN博客 https://blog.csdn.net/wjciayf/article/details/79261005

import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

import time
import cv2
import numpy as np

import tkinter as tk
from tkinter import Frame
from PIL import Image
from PIL import ImageTk

from vision_layout import config
from vision_layout.utils import find_circles
from vision_layout.utils import perTrans

from vision.classify_chess.classify import Classify 

class GUI(Frame):
    
    def __init__(self, master, **kw):

        Frame.__init__(self, master, **kw)
        frame = Frame(master, height=675, width=1200, bg="Honeydew")
        frame.place(x=0, y=0)

        self.cam = cv2.VideoCapture(0)
        self.img = None
        self.__points_a = config.POS_STORE_A  
        self.__points_b = config.POS_STORE_B
        self.__points = []  
        self.__num = 0
        self.flag_get_points = False       # 设置标志位 需要标点
        self.flag_recognize_chess = False   # 设置标志位 识别棋子

        self.ident = Classify()

        # 图像_摄像头实时
        self.panel = tk.Label(frame)  # initialize image panel
        self.panel.place(x=150, y=10)
        
        self.panel_a = tk.Label(frame)  # initialize image panel
        self.panel_a.place(x=40, y=45)

        self.panel_b = tk.Label(frame)  # initialize image panel
        self.panel_b.place(x=800, y=45)

        # 按键_棋盘位置校准
        self.btn = tk.Button(root, text="位置校准", command=self.do_get_points)
        self.btn.place(x=50, y=550)

        self.btn2 = tk.Button(root, text="棋子识别", command=self.do_recognize_chess)
        self.btn2.place(x=250, y=550)

        # 识别结果显示
        self.var_r1 = tk.StringVar()
        self.var_r1.set('abc')
        self.var_r2 = tk.StringVar()
        self.var_r2.set('abc')
        self.lb1 = tk.Label(frame, text=self.var_r1.get(), bg='palegreen', font=('Arial', 10), width=80, height=2)
        self.lb1.place(x=400, y=550)
        self.lb2 = tk.Label(frame, text=self.var_r2.get(), bg='palegreen', font=('Arial', 10), width=80, height=2)
        self.lb2.place(x=400, y=600)

        # 找圆形 参数条 
        self.var_a = tk.IntVar()
        self.sc1 = tk.Scale(frame, 
                            label='a',                        # 设置标签内容
                            from_=1,                          # 设置最大值
                            to=100,                           # 设置最小值
                            orient=tk.HORIZONTAL,             # 设置水平方向
                            length=200,                       # 设置轨道的长度
                            width=10,                         # 设置轨道的宽度
                            showvalue=True,                   # 设置显示当前值
                            troughcolor='orangeRed',          # 设置轨道的背景色
                            variable=self.var_a,              # 设置绑定变量
                            sliderlength=12,                  # 设置滑块的长度
                            sliderrelief=tk.FLAT,             # 设置滑块的立体样式
                            tickinterval=10,                  # 设置指示刻度细分
                            resolution=1,                     # 设置步长
                            bg='LavenderBlush',               # 设置背景颜色
                            command=self.set_var_a)           # 设置绑定事件处理，函数或方法
        self.sc1.place(x=1000, y=50)
        self.sc1.set(40)
      

        self.var_b = tk.IntVar()
        self.sc2 = tk.Scale(frame, 
                            label='b',                        # 设置标签内容
                            from_=1,                          # 设置最大值
                            to=100,                           # 设置最小值
                            orient=tk.HORIZONTAL,             # 设置水平方向
                            length=200,                       # 设置轨道的长度
                            width=10,                         # 设置轨道的宽度
                            showvalue=True,                   # 设置显示当前值
                            troughcolor='orangeRed',          # 设置轨道的背景色
                            variable=self.var_b,              # 设置绑定变量
                            sliderlength=12,                  # 设置滑块的长度
                            sliderrelief=tk.FLAT,             # 设置滑块的立体样式
                            tickinterval=10,                  # 设置指示刻度细分
                            resolution=1,                     # 设置步长
                            bg='LavenderBlush',               # 设置背景颜色
                            command=self.set_var_b)           # 设置绑定事件处理，函数或方法
        self.sc2.place(x=1000, y=100)
        self.sc2.set(30)
        
        self.var_c = tk.IntVar()
        self.sc3 = tk.Scale(frame, 
                            label='c',                        # 设置标签内容
                            from_=1,                          # 设置最大值
                            to=100,                           # 设置最小值
                            orient=tk.HORIZONTAL,             # 设置水平方向
                            length=200,                       # 设置轨道的长度
                            width=10,                         # 设置轨道的宽度
                            showvalue=True,                   # 设置显示当前值
                            troughcolor='orangeRed',          # 设置轨道的背景色
                            variable=self.var_c,              # 设置绑定变量
                            sliderlength=12,                  # 设置滑块的长度
                            sliderrelief=tk.FLAT,             # 设置滑块的立体样式
                            tickinterval=10,                  # 设置指示刻度细分
                            resolution=1,                     # 设置步长
                            bg='LavenderBlush',               # 设置背景颜色
                            command=self.set_var_c)           # 设置绑定事件处理，函数或方法
        self.sc3.place(x=1000, y=150)
        self.sc3.set(30)

        self.var_d = tk.IntVar()
        self.sc4 = tk.Scale(frame, 
                            label='d',                        # 设置标签内容
                            from_=1,                          # 设置最大值
                            to=100,                           # 设置最小值
                            orient=tk.HORIZONTAL,             # 设置水平方向
                            length=200,                       # 设置轨道的长度
                            width=10,                         # 设置轨道的宽度
                            showvalue=True,                   # 设置显示当前值
                            troughcolor='orangeRed',          # 设置轨道的背景色
                            variable=self.var_d,              # 设置绑定变量
                            sliderlength=12,                  # 设置滑块的长度
                            sliderrelief=tk.FLAT,             # 设置滑块的立体样式
                            tickinterval=10,                  # 设置指示刻度细分
                            resolution=1,                     # 设置步长
                            bg='LavenderBlush',               # 设置背景颜色
                            command=self.set_var_d)           # 设置绑定事件处理，函数或方法
        self.sc4.place(x=1000, y=200)
        self.sc4.set(16)
        
        self.var_e = tk.IntVar()
        self.sc5 = tk.Scale(frame, 
                            label='e',                        # 设置标签内容
                            from_=1,                          # 设置最大值
                            to=100,                           # 设置最小值
                            orient=tk.HORIZONTAL,             # 设置水平方向
                            length=200,                       # 设置轨道的长度
                            width=10,                         # 设置轨道的宽度
                            showvalue=True,                   # 设置显示当前值
                            troughcolor='orangeRed',          # 设置轨道的背景色
                            variable=self.var_e,           # 设置绑定变量
                            sliderlength=12,                  # 设置滑块的长度
                            sliderrelief=tk.FLAT,             # 设置滑块的立体样式
                            tickinterval=10,                  # 设置指示刻度细分
                            resolution=1,                     # 设置步长
                            bg='LavenderBlush',               # 设置背景颜色
                            command=self.set_var_e)           # 设置绑定事件处理，函数或方法
        self.sc5.place(x=1000, y=250)
        self.sc5.set(19)

    def set_var_a(self, v):
        self.var_a.set(v)
    def set_var_b(self, v):
        self.var_b.set(v)
    def set_var_c(self, v):
        self.var_c.set(v)
    def set_var_d(self, v):
        self.var_d.set(v)
    def set_var_e(self, v):
        self.var_e.set(v)

    def on_mouse(self, event, x, y, flags, param):
        img2 = self.img.copy()
        if event == cv2.EVENT_LBUTTONDOWN:         #左键点击
            point = (x, y)
            self.__points.append(point)
            self.__num += 1
            # print(num)
            for p in self.__points:
                cv2.circle(img2, p, 2, (0,255,0), 5)
            cv2.imshow('image_get_4_points', img2)
            if self.__num == 4:
                print(self.__points)
                self.__num = 0
                perTrans(self.img, self.__points, is_show=True)
                
                # 存入四个点的坐标数据
                file_data = ''
                with open(r".\vision\vision_layout\config.py", "r", encoding='utf-8') as f:
                    if point[0] < 130:
                        self.__points_a = self.__points[:]
                        for line in f:
                            if 'POS_STORE_A' in line:
                                new_line = "POS_STORE_A = " + str(self.__points) + '\n'
                                line = new_line
                            file_data += line
                    elif point[0] < 550:
                        for line in f:
                            # print(line)
                            if 'POS_BOARD' in line:
                                new_line = "POS_BOARD = " + str(self.__points) + '\n'
                                line = new_line
                            file_data += line
                    else:
                        self.__points_b = self.__points[:]
                        for line in f:
                            # print(line)
                            if 'POS_STORE_B' in line:
                                new_line = "POS_STORE_B = " + str(self.__points) + '\n'
                                line = new_line
                            file_data += line
                with open(r".\vision\vision_layout\config.py", "w", encoding="utf-8") as f:
                    f.write(file_data)
                    print("ok")
                    f.close()
                
                self.__points.clear()

    def recognize_chess(self, img, circles_list, is_save=False):
        res = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for circle in circles_list:
            # 计算位置id
            x, y = int(circle[0]), int(circle[1])
            id_x = 1 if x > 50 else 0
            id_y = int(y//50) 

            img_sub = img[y-14:y+14, x-14:x+14, :]
            # print("img_sub", img_sub)
            # if len(img_sub) == 0:
            #     print("img_sub", img_sub)
            #     return res
            img_path = ".\\vision\\roc.jpg"
            cv2.imwrite(img_path, img_sub)

            ret, score = self.ident.chessidentify(img_path)
            if is_save:
                cv2.imwrite(".\\vision\\data\\"+str(ret)+"\\"+str(time.time())+".jpg", img_sub)

            # res[id_x*8 + id_y] = (ret, score)
            res[id_x*8 + id_y] = ret
        return res

    def do_recognize_chess(self):
        self.flag_recognize_chess = True

    def video_loop(self):
        success, self.img = self.cam.read()  # 从摄像头读取照片
        if success:
            cv2image = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGBA) # 转换颜色从BGR到RGBA
            current_image = Image.fromarray(cv2image)        # 将图像转换成Image对象
            imgtk = ImageTk.PhotoImage(image=current_image)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)

            # 棋盘位置校准
            if self.flag_get_points:
                cv2.namedWindow('image_get_4_points')
                cv2.setMouseCallback('image_get_4_points', self.on_mouse)
                # 如果没有点点就动态显示
                if len(self.__points) == 0:
                    cv2.imshow('image_get_4_points', self.img)
                cv2.waitKey(1)

            # 显示存子位置
            else:
                img_a = perTrans(self.img, self.__points_a)
                img_b = perTrans(self.img, self.__points_b)
                # cv2窗口显示
                # cv2.imshow('image_a', img_a)
                # cv2.imshow('image_b', img_b)
                # cv2.waitKey(1)
                img_a_c, circles_a = find_circles(img_a,
                                                  minDist=int(self.var_a.get()),
                                                  param1=int(self.var_b.get()),
                                                  param2=int(self.var_c.get()),
                                                  minRadius=int(self.var_d.get()),
                                                  maxRadius=int(self.var_e.get()))
                img_b_c, circles_b = find_circles(img_b,
                                                  minDist=int(self.var_a.get()),
                                                  param1=int(self.var_b.get()),
                                                  param2=int(self.var_c.get()),
                                                  minRadius=int(self.var_d.get()),
                                                  maxRadius=int(self.var_e.get()))
                if self.flag_recognize_chess:
                    self.flag_recognize_chess = False
                    t1 = time.time()
                    alist_a = self.recognize_chess(img_a, circles_a, is_save=True)
                    alist_b = self.recognize_chess(img_b, circles_b, is_save=True)
                    alist = alist_a + alist_b
                    print(alist)
                    print("use time:", time.time()-t1)
                    self.var_r1.set(str(alist_a))
                    self.lb1.config(text=self.var_r1.get())
                    self.var_r2.set(str(alist_b))
                    self.lb2.config(text=self.var_r2.get())

                # GUI窗口显示
                cv2image = cv2.cvtColor(img_a_c, cv2.COLOR_BGR2RGBA) # 转换颜色从BGR到RGBA
                current_image = Image.fromarray(cv2image)        # 将图像转换成Image对象
                imgtk = ImageTk.PhotoImage(image=current_image)
                self.panel_a.imgtk = imgtk
                self.panel_a.config(image=imgtk)
            
                cv2image = cv2.cvtColor(img_b_c, cv2.COLOR_BGR2RGBA) # 转换颜色从BGR到RGBA
                current_image = Image.fromarray(cv2image)        # 将图像转换成Image对象
                imgtk = ImageTk.PhotoImage(image=current_image)
                self.panel_b.imgtk = imgtk
                self.panel_b.config(image=imgtk)

            self.after(1, self.video_loop)

    # TODO@libing: 不点点或者四个点都点完，否则会有问题
    def do_get_points(self):
        self.flag_get_points = False if self.flag_get_points else True
        # print("flag_get_points:", self.flag_get_points)
        if not self.flag_get_points:
            cv2.destroyWindow('image_get_4_points')

    def start(self):
        self.video_loop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Vision GUI")
    root.geometry("1200x675")
    root.resizable(0,0) # 防止窗口大小调整
    app = GUI(root)
    app.start()
    root.mainloop()
