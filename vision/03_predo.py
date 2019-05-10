import os
import cv2

path = "./vision/data"
files = os.listdir(path) 
# print(files)

for f in files: 
    print(f)
    cnt = 0
    data_list = os.listdir(path+'/'+f)
    # print(data_list[:4])
    for data in data_list:
        data_file_path = path+'/'+f+'/'+data 
        
        # img = cv2.imread(data_file_path)
        # img_resize = cv2.resize(img, (300, 300))
        # cv2.imwrite(path+'/'+f+'/'+"{:04d}.jpg".format(cnt), img_resize)
        newname = path+'/'+f+'/'+"{:04d}.jpg".format(cnt)
        os.rename(data_file_path, newname)

        cnt += 1
    #     if cnt == 2:
    #         break
    # break





