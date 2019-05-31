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

def main():
    ident = Classify()
    
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
            print(alist_ret)

        if ch == ord('s') :
            print("save photo")
            cv2.imwrite('test'+str(time.time())+'.jpg', img)
            
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()










