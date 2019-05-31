import numpy as np
import cv2
import time
import tensorflow as tf
import os
import re
import matplotlib.pyplot as plt
from PIL import Image

class Classify():
    
    _instance = None
    
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Classify, cls).__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self, 
                 labels_path = r'./vision/vision_play/tmp/output_labels.txt',
                 graph_path = r'./vision/vision_play/tmp/output_graph.pb'):
        print("载入模型")
        print("start time:", time.time())
        self._lables = {}
        self._get_lables(labels_path)
        self._graph = tf.GraphDef()
        self._get_graph(graph_path)
        print("end time:", time.time())

    def _get_lables(self, labels_path = r'./vision/vision_play/tmp/output_labels.txt'):
        lines = tf.gfile.GFile(labels_path).readlines()
        #一行一行读取数据
        for uid,line in enumerate(lines) :
            #去掉换行符
            line=line.strip('\n')
            self._lables[uid] = line

    def _get_graph(self, graph_path = r'./vision/vision_play/tmp/output_graph.pb'):
        #创建一个图来存放google训练好的模型
        with tf.gfile.FastGFile(graph_path, 'rb') as f:
            self._graph.ParseFromString(f.read())
            tf.import_graph_def(self._graph, name='')

    def chessidentify(self, image_path, is_show = False):
        with tf.Session() as sess:
            
            # tensor_name_list = [tensor.name for tensor in tf.get_default_graph().as_graph_def().node]
            # print(tensor_name_list)

            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            #载入图片
            
            # inceptionV3
            # image_data = tf.gfile.FastGFile(image_path, 'rb').read()
            # predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data}) #图片格式是jpg格式
            # predictions = np.squeeze(predictions) #把结果转为1维数据
            
            # mobileNet
            image_data = tf.gfile.FastGFile(image_path, 'rb').read()
            image_data = sess.run(tf.expand_dims(tf.image.resize_images(
                tf.image.decode_jpeg(image_data),[128, 128],method=np.random.randint(0,3)),0))
            predictions = sess.run(softmax_tensor, {'input:0': image_data}) #图片格式是jpg格式
            predictions = np.squeeze(predictions) #把结果转为1维数据

            #排序
            top_k = predictions.argsort()[::-1]
            
            def id_to_string(node_id):
                if node_id not in self._lables:
                    return ''
                return self._lables[node_id]

            if is_show:
                #打印图片路径及名称
                print(image_path)
                #显示图片
                img=Image.open(image_path)
                plt.imshow(img)
                plt.axis('off')
                plt.show()

                for node_id in top_k:     
                    #获取分类名称
                    human_string = id_to_string(node_id)
                    #获取该分类的置信度
                    score = predictions[node_id]
                    print('%s (score = %.5f)' % (human_string, score))

            top1 = top_k[0]
            res = id_to_string(top1)
            score = predictions[top1]
            return res, score




if __name__ == '__main__':
   
    # img_path = r".\vision\test\test1557367386.131967.jpg"
    # ident = Classify()
    # ret, score = ident.chessidentify(img_path, is_show=True)
    # print("ret:", ret, score)


    ident = Classify()
    for root,dirs,files in os.walk('./vision/vision_play/test/'):
        for file in files:
            print(file)
            img_path = root+"/"+file
            print("start tiem:", time.time())
            ret, score = ident.chessidentify(img_path)
            print("end time:", time.time())
            print("ret:", ret, score)
