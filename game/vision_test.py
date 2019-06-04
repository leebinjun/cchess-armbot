import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

import time
import cv2
import numpy as np

from vision.classify import Classify


if __name__ == "__main__":

    ident = Classify()
    chessai = StrategyAlphaZero()

    cap = cv2.VideoCapture(0)
    ret,img = cap.read()
    
    
    while ret is True:
        cv2.imshow("test",img)
        ret, img = cap.read() 
        ch = cv2.waitKey(1)
        
        if ch == ord('q') :
            break

        if ch == ord('r') :
            t1 = time.time()
            ret_chess = ident.recognize_chess_list_t(img, is_save=True)
            print(f"use tiem: {time.time() - t1}", end='')
            print(ret_chess)
        

    cv2.destroyAllWindows()