
## 模型

01_vision_play中的是retrain的模型，识别速度慢。  
03_classify_chess中的是最终的模型，v1是demo版本(14x750)，v2增加了模糊的数据(14x1010)进行训练。

## GUI

gui.py是视觉位置调整脚本，可以校准位置和调整棋子定位参数。  
gui_test.py是主棋盘的显示的另一版本，功能和gui.py相同。

摄像头采用了默认分辨率640*480。

## 目录

CCHESS-ARMBOT  
└─vision  
    │  classify.py  Classify棋子识别类  
    |      chessidentify()          : 识别单个棋子   
    |      recognize_chess_list()   : 识别存子区域棋子   
    |      recognize_chess_list_t() : 识别棋盘区域棋子  
    │  config_v.py  参数表：存储棋盘位置信息和找圆参数  
    │  gui.py  棋盘和棋子定位参数调整界面   
    │  utils.py  引用的函数   
    │      find_circles()   : 找圆  
    │      perTrans()       : 存子区域投射变换   
    │      perTrans_chess() : 棋盘区域投射变换  
    ├─03_classify_chess   
    │  │  predo.py 数据准备    
    │  │  model.py 模型   
    │  │  train.py 训练   
    │  └─ test.py  测试   
    └─01_vision_play  
       │  00_camtest.py          打开摄像头    
       │  01_get_chessboard.py   投射变换得到棋盘  
       │  02_circle_params.py    调整霍夫圆环检测参数   
       │  03_prepare_data.py     找圆截图准备原始数据   
       │  04_predo.py            数据文件重命名  
       │  05_retrain_old.py      模型retrain  
       │  06_label_image_old.py  模型测试  
       │  07_class_test.py       模型测试_棋子  
       │  08_class_test2.py      模型测试_棋盘  
       └─ classify.py            classify类   
       
