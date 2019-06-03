import sys,os
sys.path.append(r".\vision")

from PIL import Image
from matplotlib.pylab import *
import numpy as np
import argparse
import tensorflow as tf
import time

import cv2
import config_v
from utils import find_circles
from utils import perTrans
from utils import perTrans_chess
 
w = 28
h = 28
c = 3

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

class Classify():
    
    _instance = None
    classes = ['71','40','51','70','31','11','21','30','50','60','10','61','20','41']
    
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Classify, cls).__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self, model_dir = './vision/03_classify_chess/model/model.ckpt', is_show=False):
        if is_show:
            print("载入模型")
            print("start time:", time.time())
        # Restore model
        self.saver = tf.train.import_meta_graph(model_dir+".meta")
        self.model_dir = model_dir
        self.sess = tf.Session() 
        self.saver.restore(self.sess, self.model_dir)
        if is_show:
            print("end time:", time.time())

    # 输入棋子（28*28）照片，输出棋子类型
    def chessidentify(self, filename, is_show = False):
        # with tf.Session() as sess:
        # self.saver.restore(sess, self.model_dir)
        x = tf.get_default_graph().get_tensor_by_name("images:0")
        keep_prob = tf.get_default_graph().get_tensor_by_name("keep_prob:0")
        y = tf.get_default_graph().get_tensor_by_name("fc2/output:0")

        # Read image
        pil_im = array(Image.open(filename).convert('RGB').resize((w,h)),dtype=float32)
        #pil_im = (255-pil_im)/255.0
        pil_im = pil_im.reshape((1,w*h*c))
    
        time1 = time.time()
        # print("pil_im:", pil_im)
        prediction = self.sess.run(y, feed_dict={x:pil_im, keep_prob: 1.0})
        index = np.argmax(prediction)
        time2 = time.time()
        if is_show:
            print("The classes is: %s. (the probability is %g)" % (self.classes[index], prediction[0][index]))
            
            print("Using time %g" % (time2-time1))

        return self.classes[index], prediction[0][index]

    # 输入透射变换后图像，识别存子区域棋子放置情况
    def recognize_chess(self, img, circles_list, is_save=False):
        res = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for circle in circles_list:
            # 计算位置id
            x, y = int(circle[0]), int(circle[1])
            id_x = 1 if x > 50 else 0
            id_y = int(y//50) 

            img_sub = img[y-14:y+14, x-14:x+14, :]
            # print("img_sub", img_sub)
            # if len(img_sub) == 0:
            #     print("img_sub", img_sub)
            #     return res
            img_path = ".\\vision\\roc.jpg"
            cv2.imwrite(img_path, img_sub)

            ret, score = self.chessidentify(img_path)
            if is_save:
                cv2.imwrite(".\\vision\\data\\"+str(ret)+"\\"+str(time.time())+".jpg", img_sub)

            # res[id_x*8 + id_y] = (ret, score)
            res[id_x*8 + id_y] = ret
        return res

    # 输入摄像头拍摄的原始图片，识别存子区域棋子放置情况
    def recognize_chess_list(self, img, is_save=False, is_show=False):
        
        points_a = config_v.POS_STORE_A  
        points_b = config_v.POS_STORE_B

        img_a = perTrans(img, points_a)
        img_b = perTrans(img, points_b)
        if is_show:
            cv2.imshow('image_a', img_a)
            cv2.imshow('image_b', img_b)
            cv2.waitKey(1)

        _, circles_a = find_circles(img_a, config_v.minDist, config_v.param1, config_v.param2, config_v.minRadius, config_v.maxRadius)
        _, circles_b = find_circles(img_b, config_v.minDist, config_v.param1, config_v.param2, config_v.minRadius, config_v.maxRadius)

        alist_a = self.recognize_chess(img_a, circles_a, is_save=is_save)
        alist_b = self.recognize_chess(img_b, circles_b, is_save=is_save)
        alist = alist_a + alist_b

        return alist

    # 输入透射变换后图像，识别棋盘区域棋子放置情况
    def recognize_chess_t(self, img, circles_list, is_save=False):
        res = np.zeros(90, dtype=np.int8).reshape(10, 9) 
        for circle in circles_list:
            # 计算位置id
            x, y = int(circle[0]), int(circle[1])
            id_x = int(x//50)
            id_y = int(y//50) 

            img_sub = img[y-14:y+14, x-14:x+14, :]
            # print("img_sub", img_sub)
            # if len(img_sub) == 0:
            #     print("img_sub", img_sub)
            #     return res
            img_path = ".\\vision\\roc.jpg"
            cv2.imwrite(img_path, img_sub)

            ret, score = self.chessidentify(img_path)
            if is_save:
                cv2.imwrite(".\\vision\\data\\"+str(ret)+"\\"+str(time.time())+".jpg", img_sub)

            # res[id_x*8 + id_y] = (ret, score)
            res[id_y][id_x] = ret
        return res


    # 输入摄像头拍摄的原始图片，识别存子区域棋子放置情况
    def recognize_chess_list_t(self, img, is_save=False, is_show=False):
        points = config_v.POS_BOARD
        img_t = perTrans_chess(img, points)
        if is_show:
            cv2.imshow('image_a', img_a)
            cv2.imshow('image_b', img_b)
            cv2.waitKey(1)

        _, circles_t = find_circles(img_t, config_v.minDist, config_v.param1, config_v.param2, config_v.minRadius, config_v.maxRadius)
        
        ret_chess = self.recognize_chess_t(img_t, circles_t, is_save=is_save)
        # print(ret_chess)
        return ret_chess
        



if __name__ == '__main__':
    img_list = [r".\vision\03_classify_chess\data\10\0005.jpg",
                r".\vision\03_classify_chess\data\11\0005.jpg",
                r".\vision\03_classify_chess\data\20\0005.jpg",
                r".\vision\03_classify_chess\data\21\0005.jpg",
                r".\vision\03_classify_chess\data\30\0005.jpg",
                r".\vision\03_classify_chess\data\31\0005.jpg",
                r".\vision\03_classify_chess\data\40\0005.jpg",
                r".\vision\03_classify_chess\data\41\0005.jpg",
                r".\vision\03_classify_chess\data\50\0005.jpg",
                r".\vision\03_classify_chess\data\51\0005.jpg",
                r".\vision\03_classify_chess\data\60\0005.jpg",
                r".\vision\03_classify_chess\data\61\0005.jpg",
                r".\vision\03_classify_chess\data\70\0005.jpg",
                r".\vision\03_classify_chess\data\71\0005.jpg"]
    ident = Classify()
    for img_path in img_list:
        ret, score = ident.chessidentify(img_path)
        print("ret:", ret, score)
    
    img_filepath = r"C:\Users\Administrator\Desktop\cchess-armbot\test1559289739.3877587.jpg"
    img = cv2.imread(img_filepath, 1)
    ret = ident.recognize_chess_list(img)
    print(ret)
    # ident = Classify()
    # for root,dirs,files in os.walk('./vision/classify_chess/data/'):
    #     for file in files:
    #         print(file)
    #         img_path = root+"/"+file
    #         ret, score = ident.chessidentify(img_path)
    #         print("ret:", ret, score)


