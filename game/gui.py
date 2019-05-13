# import tkinter as tk

# window = tk.Tk()
# window.title('hello')
# window.geometry('200x100')

# label = tk.Label(window, text='hey', bg='green', font=('Arial', 12))
# label.width = 15
# label.height = 2
# label.pack()

# window.mainloop() 



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
 
