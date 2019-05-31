import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
sys.path.append(r".\vision\vision_layout")

import cv2
import numpy as np
import config
import time

# minDist = 40
# param1  = 30
# param2  = 30
# minRadius = 16
# maxRadius = 19

def find_circles(img, minDist, param1, param2, minRadius, maxRadius):
    img_c = img.copy()

    gray=cv2.cvtColor(img_c,cv2.COLOR_BGR2GRAY)
    #霍夫变换圆检测
    #霍夫变换圆检测
    a,b,c,d,e = minDist, param1, param2, minRadius, maxRadius
    circles= cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,a,param1=b,param2=c,minRadius=d,maxRadius=e)
    
    #输出返回值，方便查看类型
    # print(circles)
    if type(circles) == None.__class__:
        return img_c, None

    #输出检测到圆的个数
    # print(len(circles[0]))
 
    #根据检测到圆的信息，画出每一个圆
    for circle in circles[0]:
        #圆的基本信息
        # print(circle[2])
        #坐标行列(就是圆心)
        x=int(circle[0])
        y=int(circle[1])
        #半径
        r=int(circle[2])
        #在原图用指定颜色圈出圆，参数设定为int所以圈画存在误差
        img_c = cv2.circle(img_c,(x,y),r,(0,0,255),1,8,0)
    #显示新图像
    # cv2.imshow('Result',img)
    return img_c, circles[0]


# 透射变换
def perTrans(img_src, points, is_show=False):
    ps_dst = np.float32([[0,0],[0,399],[99, 0],[99,399]])
    ps_src = np.float32(points)
    mat_pers = cv2.getPerspectiveTransform(ps_src, ps_dst)
    img_dst = cv2.warpPerspective(img_src, mat_pers, (100,400))
    if is_show:
        cv2.imshow('rst_image', img_dst)
    return img_dst