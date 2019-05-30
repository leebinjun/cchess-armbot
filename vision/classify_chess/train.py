from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
 
import tensorflow as tf
import argparse
import sys
import model
import read_image
import numpy as np
 
w = 28
h = 28
c = 3
n_class = 14 

def main(args):
    lr = args.learning_rate
    batch_size = args.batch_size
    epoches = args.epoches
    keep_prob_value = args.keep_prob
    train(lr,batch_size, epoches, keep_prob_value)
    
 
def train(lr, batch_size, epoches, keep_prob_value):
    # 下载图片
    path = './data/'
    x_train, y_train, x_val, y_val = read_image.read_img(path)
    
    x = tf.placeholder(tf.float32, [None, w*h*c], name="images")
    y_ = tf.placeholder(tf.float32, [None, n_class], name="labels")
    keep_prob = tf.placeholder(tf.float32,name="keep_prob")
    y = model.model(x, keep_prob)
    
    # Cost function
    cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_*tf.log(y+ 1e-10),
                                                  reduction_indices=[1]),name="corss_entropy")
 
    train_step = tf.train.AdamOptimizer(lr).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name="accuracy")
    saver = tf.train.Saver()
 
    # Start training
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for i in range(epoches):
            iters = np.int32(len(x_train)/batch_size)+1
            for j in range(iters):
                if j==iters-1:
                    batch0 = x_train[j*batch_size:]
                    batch1 = y_train[j*batch_size:]
                else:
                    batch0 = x_train[j*batch_size:(j+1)*batch_size]
                    batch1 = y_train[j*batch_size:(j+1)*batch_size]
                sess.run(train_step, feed_dict={x:batch0, y_:batch1,
                                                keep_prob:keep_prob_value})
            if i%5==0:
                train_accuracy = sess.run(accuracy,
                                            feed_dict={x:batch0, y_:batch1,
                                            keep_prob: keep_prob_value})
                print("step %d, training accuracy %g" % (i, train_accuracy))

                # Save model
                saver_path = saver.save(sess,"./model/model.ckpt")
                print("Model saved in file:", saver_path)
                
        test_accuracy = sess.run(accuracy, feed_dict={x:x_val,
                                                      y_:y_val,
                                                      keep_prob: 1.0})
        print("test accuracy %g" % test_accuracy)
    
 
def parse_arguments(argv):
    parser = argparse.ArgumentParser()
 
    parser.add_argument('--learning_rate', type=float,
                        help="learning rate", default=1e-4)
    parser.add_argument('--batch_size', type=float,
                        help="batch_size", default=100)
    parser.add_argument('--epoches', type=float,
                        help="max iterations", default=4500)
    parser.add_argument('--keep_prob', type=float,
                        help="keep prob", default=0.2)
    return parser.parse_args(argv)
 
if __name__=="__main__":
    main(parse_arguments(sys.argv[1:]))
    
