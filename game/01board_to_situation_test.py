import numpy as np



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


if __name__ == "__main__":

    board = np.array([[11,  0, 51, 41, 71,  0, 51,  0, 11],
                      [ 0,  0,  0,  0,  0, 60,  0,  0,  0],
                      [ 0,  0, 21, 41,  0, 40, 10, 50,  0],
                      [ 0, 20, 10, 60,  0, 61, 30, 30,  0],
                      [ 0,  0, 40, 21,  0,  0, 61,  0, 70],
                      [ 0,  0, 60,  0,  0, 61,  0, 60,  0],
                      [ 0,  0,  0,  0,  0,  0, 61,  0,  0],
                      [ 0,  0, 60,  0,  0,  0, 31, 31,  0],
                      [ 0, 61, 50,  0,  0,  0,  0,  0,  0],
                      [ 0, 20,  0,  0,  0,  0,  0,  0,  0]], dtype = np.int8)

    ret = board_to_situation(board)
    print(ret)
    