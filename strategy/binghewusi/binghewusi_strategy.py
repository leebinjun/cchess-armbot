# 电脑象棋引擎排名表        http://www.xqbase.com/league/ranklist.htm
# 中国象棋程序《兵河五四》  http://www.xqbase.com/league/bhws.htm
# 中国象棋电脑应用规范(五)：中国象棋通用引擎协议 http://www.xqbase.com/protocol/cchess_ucci.htm

import sys
sys.path.append(r".\strategy\binghewusi")

import subprocess
import time


# go time 500 depth 5
class StrategyBinghewusi:

    exepath = r".\strategy\binghewusi\Binghewusi.exe"

    def __init__(self):
        self.p = subprocess.Popen(self.exepath, stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ret = self.p.stdout.readline()
        print(ret.decode('GBK'))

    def get_move(self, position = "rCbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/4C2C1/9/RNBAKABNR", 
                 player = "b", times = 1000, depth = 6, show_thinking = False):   
        
        self.p.stdin.write("ucci".encode('GBK'))
        com = "position fen " + position + " " + player + " - - 0 1\r\n"
        if show_thinking:
            print(f"position: {position}")
            print(f"com: {com}")
        self.p.stdin.write(com.encode('GBK'))
        self.p.stdin.write('go infinite time 20000\r\n'.encode('GBK'))
        self.p.stdin.flush()

        while True:
            ret = self.p.stdout.readline()
            if show_thinking:
                print(ret.decode('GBK'))
            if ret.decode('GBK')[:8] == 'bestmove':
                ans = ret.decode()[9:13]
                break
        # print("ans", ans)
        return ans

if __name__ == '__main__':
    ai = StrategyBinghewusi()
    # situation = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/2C4C1/9/RNBAKABNR"
    situation = "4k4/9/7R1/9/9/9/9/5A3/4AK3/9"
    move = ai.get_move(position=situation, show_thinking = True)
    print(move)




