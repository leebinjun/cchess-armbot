import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

import time
import cv2
import numpy as np

from armbot.robot import Armbot
from vision.classify import Classify
from strategy.alphazero.cchess_alphazero.mytest2 import StrategyAlphaZero


# 由局面board生成ucci通信局面描述字符串
def board_to_situation(board: np.int8):
    adict = {1:'r', 2:'n', 5:'b', 4:'a', 7:'k', 3:'c', 6:'p', 0:'0'}
    
    import pprint
    print("board:")
    pprint.pprint(board)
    situation = []

    for i in range(10):
        count = 0
        for j in range(9):
            if board[i][j] != 0:
                if count != 0:
                    situation.append(str(count))
                    idx = adict[board[i][j]//10] if board[i][j]%10 else adict[board[i][j]//10].upper()
                    situation.append(idx)
                    count = 0
                else:
                    idx = adict[board[i][j]//10] if board[i][j]%10 else adict[board[i][j]//10].upper()
                    situation.append(idx)
            else:
                count += 1
        if count != 0:
            situation.append(str(count))
        situation.append("/")
    situation = situation[:-1]
    # situation.reverse()
    res = "".join(situation)
    # print(res)
    return res

# 由策略更新局面，得到机械臂运动目标
def update_board( move, board: np.int8, isShow = False):
    
    new_y  = ord(move[2]) - ord('a')
    new_x  = 9 - int(move[3])
    last_y = ord(move[0]) - ord('a') 
    last_x = 9 - int(move[1])            

    flag_capture = False
    # 判读是否吃子
    if board[new_x][new_y] != 0:
        flag_capture = True

    return [new_y, new_x, last_y, last_x], flag_capture


def rlist_to_nlist(alist: list):
    adict = {1:'r', 2:'n', 5:'b', 4:'a', 7:'k', 3:'c', 6:'p', 0:'0'}
    
    import pprint
    print("board:")
    pprint.pprint(alist)
    nlist = []

    for i in alist:
        idx = int(i)//10
        ret = adict[idx] if int(i)%10 else adict[idx].upper()
        nlist.append(ret) 
    return nlist

def do_layout(armbot: Armbot, ret_list: list, init_board = None):
    from armbot import config_a
    
    if init_board == None: #正常开局
        # 计算(棋子[位置1, 位置2 ...])字典dict_v
        from collections import defaultdict
        dict_v = defaultdict(list)
        for i, v in enumerate(ret_list):
            dict_v[v].append(i)
        # print(dict_v)
        # defaultdict(<class 'list'>, {'31': [0, 25], '61': [1, 5, 10, 13, 14], '30': [2, 12], '60': [3, 7, 9, 19, 29], '20': [4, 26], '41': [6, 20], '71': [8], '10': [11, 15], '21': [16, 24], '50': [17, 27], '51': [18, 21], '40': [22, 28], '11': [23, 30], '70': [31]})

        for idx in dict_v:
            for i, v in enumerate(dict_v[idx]):
                x_last, y_last = config_a.POS_STORE_LIST[v]
                x_new, y_new = config_a.POS_INIT_DICT[idx][i]
                print(f"move: idx:{idx}, ({x_last},{y_last}) to ({x_new}, {y_new})")
                alist = [x_new, y_new, x_last, y_last]
                armbot.move(alist)
                a = input()
    else:
        ret_list = rlist_to_nlist(ret_list)
        print(f"rlist: {ret_list}")

        # 计算(棋子[位置1, 位置2 ...])字典dict_v
        from collections import defaultdict
        dict_v = defaultdict(list)
        for i, v in enumerate(ret_list):
            dict_v[v].append(i)
        # print(dict_v)

        # "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR"
        pos_str = init_board.replace('/','')
        pos_str = pos_str.replace('9','111111111')
        pos_str = pos_str.replace('8','11111111')
        pos_str = pos_str.replace('7','1111111')
        pos_str = pos_str.replace('6','111111')
        pos_str = pos_str.replace('5','11111')
        pos_str = pos_str.replace('4','1111')
        pos_str = pos_str.replace('3','111')
        pos_str = pos_str.replace('2','11')
        # 'rnbakabnr1111111111c11111c1p1p1p1p1p111111111111111111P1P1P1P1P1C11111C1111111111RNBAKABNR'
        from collections import defaultdict
        dict_pos = defaultdict(list)
        print(pos_str)
        for i, v in enumerate(pos_str):
            dict_pos[v].append((i%9, i//9))
        dict_pos.pop('1')

        print(f"dict_pos: {dict_pos}")
        print(f"dict_v: {dict_v}")


        for idx in dict_pos:
            if idx != '1':
                for i, v in enumerate(dict_pos[idx]):
                    xx = dict_v[idx][i]
                    x_last, y_last = config_a.POS_STORE_LIST[xx]
                    x_new, y_new = v
                    print(f"move: idx:{idx}, ({x_last},{y_last}) to ({x_new}, {y_new})")
                    alist = [x_new, y_new, x_last, y_last]
                    armbot.move(alist)
                    time.sleep(2)


if __name__ == "__main__":

    ident = Classify()
    chessai = StrategyAlphaZero()
    armbot = Armbot()
    armbot.go_ready()

    cap = cv2.VideoCapture(0)
    ret,img = cap.read()
    
    
    while ret is True:
        cv2.imshow("test",img)
        ret, img = cap.read() 
        ch = cv2.waitKey(1)
        
        if ch == ord('q') :
            break
        if ch == ord('a') :
            alist_ret = ident.recognize_chess_list(img)
            if True:
                print("ret:")
                print(alist_ret[:8])
                print(alist_ret[8:16])
                print(alist_ret[16:24])
                print(alist_ret[24:])
            do_layout( armbot, alist_ret, init_board="4k4/4r4/9/9/9/9/9/9/4A4/4KA3")

        if ch == ord('w') :
            is_end = False
            while not is_end:
                ret_chess_old = ident.recognize_chess_list_t(img)
                n_zero_old = np.count_nonzero(ret_chess_old)
                is_update = False
                ch = cv2.waitKey(3)
                while not is_update:
                    cv2.imshow("test",img)
                    ret, img = cap.read() 
                    ch = cv2.waitKey(3)
                    if ch == ord('q') :
                        break
                    ret_chess_new = ident.recognize_chess_list_t(img)
                    print(n_zero_old)
                    print(np.count_nonzero(ret_chess_new))
                    if np.count_nonzero(ret_chess_new) != n_zero_old or np.count_nonzero(ret_chess_new) != n_zero_old-1:
                        if np.count_nonzero(ret_chess_new - ret_chess_old) == 2:
                            # print(ret_chess_new)
                            is_update = True
                        else:
                            print(ret_chess_new)
                        
                fen = board_to_situation(ret_chess_new)
                print(f"fen: {fen}")
                move = chessai.get_move(position=fen, show_thinking = True)
                print(f"move: {move}")

                # 机械臂下棋
                alist, flag_capture = update_board(move, board = ret_chess_new)
                print(f"list: {alist}")
                armbot.move(alist, capture = flag_capture, isShow=True)

        if ch == ord('r') :
            t1 = time.time()
            ret_chess = ident.recognize_chess_list_t(img, is_save=True)
            print(f"use tiem: {time.time() - t1}")
            print(ret_chess)
        


    cv2.destroyAllWindows()