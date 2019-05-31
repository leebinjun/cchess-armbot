# 调整霍夫圆环检测参数
# trackbar参数范围待调整，否则会导致cv2.HoughCircles参数错误

from __future__ import print_function
import cv2 as cv
import cv2 as cv2
import argparse
import config
import numpy as np

min_value = 1
max_value = 50

minDist = 40
param1  = 30
param2  = 15
minRadius = 16
maxRadius = 18


param1_name = 'minDist'
param2_name = 'param1'
param3_name = 'param2'
param4_name = 'minRadius'
param5_name = 'maxRadius'

def on_param1_thresh_trackbar(val):
    global minDist
    minDist = max(val, 0)
    cv.setTrackbarPos(param1_name, window_trackbar_name, minDist)

def on_param2_thresh_trackbar(val):
    global param1
    param1 = max(val, 0)
    cv.setTrackbarPos(param2_name, window_trackbar_name, param1)

def on_param3_thresh_trackbar(val):
    global param2
    param2 = max(val, 0)
    cv.setTrackbarPos(param3_name, window_trackbar_name, param2)

def on_param4_thresh_trackbar(val):
    global minRadius
    global maxRadius
    minRadius = val
    minRadius = min(maxRadius-1, minRadius)
    cv.setTrackbarPos(param4_name, window_trackbar_name, minRadius)

def on_param5_thresh_trackbar(val):
    global minRadius
    global maxRadius
    maxRadius = val
    maxRadius = max(maxRadius, minRadius+1)
    cv.setTrackbarPos(param5_name, window_trackbar_name, maxRadius)

def perTrans(img_src, points):
    ps_dst = np.float32([[0,0],[0,399],[99, 0],[99,399]])
    ps_src = np.float32(points)
    mat_pers = cv2.getPerspectiveTransform(ps_src, ps_dst)
    img_dst = cv2.warpPerspective(img_src, mat_pers, (100,400))
    # cv2.imshow('rst_image', img_dst)
    return img_dst


parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
parser.add_argument('--camera', help='Camera devide number.', default=0, type=int)
args = parser.parse_args()

cap = cv.VideoCapture(args.camera)

window_trackbar_name = "Params"
cv.namedWindow(window_trackbar_name)
cv.createTrackbar(param1_name, window_trackbar_name, min_value, max_value, on_param1_thresh_trackbar)
cv.createTrackbar(param2_name, window_trackbar_name, min_value, max_value, on_param2_thresh_trackbar)
cv.createTrackbar(param3_name, window_trackbar_name, min_value, max_value, on_param3_thresh_trackbar)
cv.createTrackbar(param4_name, window_trackbar_name, min_value, max_value, on_param4_thresh_trackbar)
cv.createTrackbar(param5_name, window_trackbar_name, min_value, max_value, on_param5_thresh_trackbar)

points_a = config.POS_STORE_A

while True:
    ret, frame = cap.read()
    if frame is None:
        break

    ret, img = cap.read()
    img = perTrans(img, points_a)
    cv2.imshow('img',img)
    key = cv.waitKey(30)
 
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    #霍夫变换圆检测
    a,b,c,d,e = minDist, param1, param2, minRadius, maxRadius
    circles= cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,a,param1=b,param2=c,minRadius=d,maxRadius=e)
    
    #输出返回值，方便查看类型
    print(circles)
    if type(circles) == None.__class__:
        continue

    #输出检测到圆的个数
    print(len(circles[0]))
 
    #根据检测到圆的信息，画出每一个圆
    for circle in circles[0]:
        #圆的基本信息
        print(circle[2])
        #坐标行列(就是圆心)
        x=int(circle[0])
        y=int(circle[1])
        #半径
        r=int(circle[2])
        #在原图用指定颜色圈出圆，参数设定为int所以圈画存在误差
        img=cv2.circle(img,(x,y),r,(0,0,255),1,8,0)
    #显示新图像
    cv2.imshow('Result',img)
 
    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break

cv2.destroyAllWindows()
        



