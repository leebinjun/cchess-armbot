import tkinter as tk
from tkinter import Frame
from robot import Armbot


class GUI(Frame):
    
    def __init__(self, master, **kw):


        Frame.__init__(self, master, **kw)
        frame = Frame(master)
        frame.pack()
        # 串口设置相关变量
        self.port = 'com3'
        self.baudrate = 9600
        # 输出框提示
        self.lab3 = tk.Label(frame, text='Message Show')
        self.lab3.grid (row=0, column=1, sticky=tk.W)
        # 输出框
        self.show = tk.Text(frame, width=90, height=40, wrap=tk.WORD)
        self.show.grid (row=1, column=1, rowspan=4, sticky=tk.W)
        # 输入框提示
        self.lab4 = tk.Label(frame, text='Hi, Input here!')
        self.lab4.grid (row=5, column=1, sticky=tk.W)
        # 输入框
        self.input = tk.Entry(frame, width=60)
        self.input.grid (row=6, column=1, rowspan=4, sticky=tk.W)
        # 输入按钮
        self.button1 = tk.Button(frame, text="Input", command=self.Submit)
        self.button1.grid (row=11, column=1, sticky=tk.E)
        # 串口开启按钮
        self.button2 = tk.Button(frame, text='Open Serial....', command=self.open)
        self.button2.grid (row=2, column=0, sticky=tk.W)
        # 串口关闭按钮
        self.button3 = tk.Button(frame, text='Close Serial....', command=self.close)
        self.button3.grid (row=3, column=0, sticky=tk.W)
        # 图像显示按钮
        self.button4 = tk.Button(frame, text='Display image', command=self.Display_image)
        self.button4.grid (row=4, column=0, sticky=tk.W)
        # 串口信息提示框
        self.showSerial = tk.Text(frame, width=30, height=1, wrap=tk.WORD)
        self.showSerial.grid (row=11, column=0, sticky=tk.W)

        # 添加菜单
        menubar = tk.Menu(master)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade (label='File', menu=filemenu)

        filemenu.add_separator ()
        filemenu.add_command (label='Exit', command=master.quit)
        master.config (menu=menubar)


        #串口初始化
        self.ser = Armbot(self.port)

    def Submit(self):
        context1 = self.input.get ()
        n = self.ser.write (context1)
        output = self.ser.read (n)
        print(output)
        self.show.delete (0.0, END)
        self.show.insert (0.0, output)

    def open(self):
        self.ser.open ()
        if self.ser.isOpen () == True:
            self.showSerial.delete (0.0, END)
            self.showSerial.insert (0.0, "Serial has been opend!")

    def close(self):
        self.ser.close ()
        if self.ser.isOpen () == False:
            self.showSerial.delete (0.0, END)
            self.showSerial.insert (0.0, "Serial has been closed!")
            thread.exit ()  # 关闭线程；

    def Display_image(self):
        COM_X = Check_Comx ()
        mSerial = MSerialPort (COM_X, 9600)
        thread.start_new_thread (mSerial.read_data, ())  # 调用thread模块中的start_new_thread()函数来产生新线程
        Y_lim = raw_input ('enter Y_lim: ')
        while True:
            i = 0
            time.sleep (1 / 30)
            mSerial.read_data ()
            plt.ion ()  # 开启matplotlib的交互模式
            plt.xlim (0, 50)  # 首先得设置一个x轴的区间 这个是必须的
            plt.ylim (-int (Y_lim), int (Y_lim))  # y轴区间
            data_list.append (mSerial.read_data ())

            i = i + 1
            if i > 50:  # 初始状态x轴最大为50
                plt.xlim (i - 50, i)  # 如果当前坐标x已经超过了50，将x的轴的范围右移。
            plt.plot (data_list)  # 将list传入plot画图
            plt.pause (0.01)  # 这个为停顿0.01s，能得到产生实时的效果
 




if __name__ == "__main__":
    root = tk.Tk()
    root.title("Serial GUI")
    root.geometry("900x630")
    app = GUI(root)
    root.mainloop ()


