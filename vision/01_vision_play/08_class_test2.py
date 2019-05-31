# ident.chessidentify_1(img_sub) ->[[2]] 识别棋子类别， 准确率有待提升
# ident.chessidentify_2(img_sub) ->[[1]] 识别棋子红黑
# board 为红棋局面

import time
import numpy as np
import cv2
import argparse
from classify import Classify

board = np.array([[1, 2, 3, 4, 5, 4, 3, 2, 1],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 6, 0, 0, 0, 0, 0, 6, 0],
                  [7, 0, 7, 0, 7, 0, 7, 0, 7],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype = np.int16)


def perTrans(img, points = [(125, 448), (130, 25), (513, 452), (513, 23)]):
    # points: U L D R 4 points
    dst = np.float32([[0,0],[0,439],[439,0],[439,439]])
    src = np.float32(points)
    M = cv2.getPerspectiveTransform(src, dst)
    T = cv2.warpPerspective(img,M,(440,440))
    ROI = np.zeros((440,440,3),np.uint8)
    ROI[0:,0:440] = T
    return ROI



if __name__ == '__main__':
    
    ident = Classify()

    cap = cv2.VideoCapture(0)
    ret,img = cap.read()
    
    
    # 初始化board
    while ret is True:
        ret,img = cap.read()
        image = perTrans(img)
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #霍夫变换圆检测
        circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 20,
                                param1=20, param2=25, minRadius=14, maxRadius=16)
        # #输出返回值，方便查看类型
        # print(circles)
        if type(circles) == None.__class__:
            continue
            
        img_circle = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # 更新current_board
        for circle in circles[0]:
            # 计算位置id
            x, y, r= int(circle[0]), int(circle[1]), int(circle[2])
            id_x = x // 50
            id_y = (4 - (y-230)//40) if y > 220 else (9 - (y-10)//40)
            id_x, id_y = id_x, 9-id_y

            img_sub = image[y-12:y+12, x-12:x+12, :]
            cv2.imwrite(r".\vision\roc.jpg", img_sub)
            img_path = r".\vision\roc.jpg"

            ret, score = ident.chessidentify(img_path)
            
            board[id_y][id_x] = ret

            img_circle = cv2.circle(img_circle, (x,y), r, (0,0,255), 1, 8, 0)

        cv2.imshow('circle', img_circle)
        
        key = cv2.waitKey(2)
        if key == ord('q') or key == 27:
            break
        
        print("board:")
        print(board)
        # cv2.imshow('sub',img_sub)
        ret, img = cap.read()


    cv2.destroyAllWindows()
