# 电脑象棋引擎排名表        http://www.xqbase.com/league/ranklist.htm
# 中国象棋程序《象棋旋风》  http://www.xqbase.com/league/xqcyclone.htm

import sys
sys.path.append(r".\strategy\cyclone")

import subprocess
import time



# go time 500 depth 5
class StrategyCyclone:

    exepath = r".\strategy\cyclone\cyclone.exe"

    def __init__(self):
        self.p = subprocess.Popen(self.exepath, stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ret = self.p.stdout.readline()
        print(ret)

    def get_move(self, position = "rCbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/4C2C1/9/RNBAKABNR", 
                 player = "b", times = 1000, depth = 8, show_thinking = 1):   
        
        com = "position fen " + position + " " + player + " - - 0 1\r\n"
        self.p.stdin.write(com.encode('GBK'))
        # com = 'go depth ' + str(depth) + ' time 20000\r\n'
        com = 'go depth ' + str(depth) + '\r\n'
        self.p.stdin.write(com.encode('GBK'))
        self.p.stdin.flush()

        while True:
            ret = self.p.stdout.readline()
            if show_thinking:
                print(ret)
            if ret.decode()[:8] == 'bestmove':
                ans = ret.decode()[9:13]
                break
        # print("ans", ans)
        return ans

if __name__ == '__main__':
    ai = StrategyCyclone()
    situation = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/2C4C1/9/RNBAKABNR"
    move = ai.get_move(position=situation, show_thinking = True)
    print(move)




