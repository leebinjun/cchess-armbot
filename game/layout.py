import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

import time
import cv2
import numpy as np

import tkinter as tk
from tkinter import Frame
from PIL import Image
from PIL import ImageTk

from armbot.robot import Armbot
from vision.classify import Classify

from armbot import config_a


def do_layout(armbot: Armbot, ret_list: list):
    from collections import defaultdict
    dict_v = defaultdict(list)
    for i, v in enumerate(ret_list):
        dict_v[v].append(i)
    print(dict_v)
    for idx in dict_v:
        for i, v in enumerate(dict_v[idx]):
            x_last, y_last = config_a.POS_STORE_LIST[v]
            x_new, y_new = config_a.POS_INIT_DICT[idx][i]
            print(f"move: idx:{idx}, ({x_last},{y_last}) to ({x_new}, {y_new})")
            alist = [x_new, y_new, x_last, y_last]
            armbot.move(alist)
            a = input()
            

def main():
    ident = Classify()
    armbot = Armbot()
    armbot.go_ready()
    
    cap = cv2.VideoCapture(0)
    ret,img = cap.read()
    while ret is True:
        cv2.imshow("test",img)
        ret, img = cap.read() 
        ch = cv2.waitKey(1)
        if ch == ord('q') :
            break
        if ch == ord('a') :
            alist_ret = ident.recognize_chess_list(img)
            if True:
                print("ret:")
                print(alist_ret[:8])
                print(alist_ret[8:16])
                print(alist_ret[16:24])
                print(alist_ret[24:])
            do_layout( armbot, alist_ret)


        if ch == ord('s') :
            print("save photo")
            cv2.imwrite('test'+str(time.time())+'.jpg', img)
            
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()










