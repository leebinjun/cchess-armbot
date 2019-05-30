import cv2
import numpy as np
import config
import time

minDist = 40
param1  = 30
param2  = 22
minRadius = 16
maxRadius = 18

def perTrans(img_src, points):
    ps_dst = np.float32([[0,0],[0,399],[99, 0],[99,399]])
    ps_src = np.float32(points)
    mat_pers = cv2.getPerspectiveTransform(ps_src, ps_dst)
    img_dst = cv2.warpPerspective(img_src, mat_pers, (100,400))
    # cv2.imshow('rst_image', img_dst)
    return img_dst

def find_circles(img):
    
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #霍夫变换圆检测
    a,b,c,d,e = minDist, param1, param2, minRadius, maxRadius
    circles= cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,a,param1=b,param2=c,minRadius=d,maxRadius=e)
    
    #输出返回值，方便查看类型
    print(circles)
    if type(circles) == None.__class__:
        return img

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
    # cv2.imshow('Result',img)
    return img


def main():

    cap = cv2.VideoCapture(0)
    ret,img = cap.read()

    # get 4 points
    points_a = config.POS_STORE_A
    points_b = config.POS_STORE_B
    
    while ret is True:
        cv2.namedWindow('image')
        cv2.imshow('image', img)
        img_a = perTrans(img, points_a)
        img_b = perTrans(img, points_b)
        img_a = find_circles(img_a)
        img_b = find_circles(img_b)
        cv2.imshow('image_a', img_a)
        cv2.imshow('image_b', img_b)
        
        ret, img = cap.read()
        ch = cv2.waitKey(5)
        if ch == ord('q') :
            break
        if ch == ord('s') :
            print("save photo")
            cv2.imwrite(r".\vision\vision_layout" + '\\' + str(time.time())+'.jpg', img_b)
            cv2.imwrite(r".\vision\vision_layout" + '\\' + str(time.time())+'.jpg', img_a)
        

if __name__ == '__main__':
    main()
