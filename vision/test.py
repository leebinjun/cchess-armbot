import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

import time
import cv2
import numpy as np

import tkinter as tk
from tkinter import Frame
from PIL import Image
from PIL import ImageTk

from vision.classify import Classify

import config_v

from game.utils import board_to_situation


def main():
    ident = Classify()
    
    cap = cv2.VideoCapture(0)
    ret,img = cap.read()
    while ret is True:
        cv2.imshow("test",img)
        ret, img = cap.read() 
        ch = cv2.waitKey(1)

        if ch == ord('w'):
            t1 = time.time()
            ret_chess = ident.recognize_chess_list_t(img)
            print(f"use tiem: {time.time() - t1}")
            print(ret_chess)
            fen = board_to_situation(ret_chess)
            print(f"fen: {fen}")

        if ch == ord('a') :
            alist_ret = ident.recognize_chess_list(img)
            if True:
                print("ret:")
                print(alist_ret[:8])
                print(alist_ret[8:16])
                print(alist_ret[16:24])
                print(alist_ret[24:])

        if ch == ord('s') :
            print("save photo")
            cv2.imwrite('test'+str(time.time())+'.jpg', img)

        if ch == ord('q') :
            break
            
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

