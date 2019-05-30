# 点点，截取象棋棋盘
# 点击顺序： 左上 左下 右上 右下

import time
import numpy as np
import cv2
import config

def perTrans(img, points):
    dst = np.float32([[0,0],[0,399],[99, 0],[99,399]])
    src = np.float32(points)
    M = cv2.getPerspectiveTransform(src, dst)
    T = cv2.warpPerspective(img, M, (100,400))
    ROI = np.zeros((400,100,3),np.uint8)
    ROI[:,:] = T
    cv2.imshow('rst_image', ROI)
    # return ROI

global img
global point
points = config.POS_STORE_A
num = 0

def on_mouse(event, x, y, flags, param):
    global img, point, points, num
    img2 = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:         #左键点击
        point = (x, y)
        points.append(point)
        num += 1
        print(num)
        cv2.circle(img2, point, 10, (0,255,0), 5)
        cv2.imshow('image', img2)
        if num == 4:
            print(points)
            num = 0
            perTrans( img, points)
            
            file_data = ''
            with open(r".\vision_layout\config.py", "r", encoding='utf-8') as f:
                for line in f:
                    # print(line)
                    if 'alist' in line:
                        new_line = "alist = " + str(points) + '\n'
                        line = new_line
                    file_data += line
            with open(r".\vision_layout\config.py", "w", encoding="utf-8") as f:
                f.write(file_data)
                print("ok")
                f.close()
            
            points.clear()

def main():
    global img

    cap = cv2.VideoCapture(0)
    ret,img = cap.read()
    perTrans( img, points)
    points.clear()
    while ret is True:
        
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', on_mouse)
        cv2.imshow('image', img)
        ret, img = cap.read()
        
        ch = cv2.waitKey(5)
        if ch == ord('q') :
            break
        if ch == ord('s') :
            print("save photo")
            cv2.imwrite(r".\vision" + '\\' + str(time.time())+'.jpg', img)
            cv2.imwrite(r".\vision" + '\\' + str(time.time())+'.jpg', img_trans)
        

if __name__ == '__main__':
    main()

'''
    img = cv2.imread(r".\vision\vision_layout\test1558857706.1279004.jpg", 1)
    # (h, w, c) = img.shape
    cv2.imshow("o", img)
    # img_dst = cv2.resize(img, (int(w/5), int(h/1)))
    # cv2.imshow("d", img_dst)
    # cv2.waitKey(0)

    height, width, _ = img.shape  # (height, width, mode)
    # src 3p -> dst 3p
    matSrc = np.float32([[0,0], [0,height-1], [width-1, 0]])
    matDst = np.float32([[50,50], [300,height-200], [width-300, 100]])
    # 组合矩阵
    matAffine = cv2.getAffineTransform(matSrc, matDst)
    print(matAffine)
    dstImage = cv2.warpAffine(img, matAffine, (width, height))
    cv2.imshow("img", dstImage)

    matRotate = cv2.getRotationMatrix2D((int(width/2), int(height/2)), 45, 0.5)
    print(matRotate)
    dstImage = cv2.warpAffine(img, matRotate, (width, height))
    cv2.imshow("img2", dstImage)
    cv2.waitKey(0)

'''