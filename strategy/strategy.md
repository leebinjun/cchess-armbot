
## 目录

CCHESS-ARMBOT   
└─strategy  
   ├─alphazero  
   │  │  README.md  
   │  ├─cchess_alphazero  
   │  │  │  mytest2.py   StrategyAlphaZero类    
   │  │  │  mytest3.py   GUI用于残局测试  
   │  │  │  config.py    Config类  
   │  │  │  run-cg.py    原始工程执行入口  
   │  │  ├─agent  
   │  │  │  │  model.py  CChessModel类  
   │  │  │  └─ player.py CChessPlayer类  
   │  │  ├─configs  
   │  │  │  └─ mini.py  
   │  │  ├─environment  
   │  │  │  └─ chessboard.py  棋盘类，初始化棋盘   
   │  │  └─play_games  
   │  │     └─ play.py  PlayWithHuman类  
   │  └─data  
   │     └─model  
   │        └─ model_best_weight.h5    cczero最新权重  
   ├─binghewusi   象棋引擎-兵河五车   
   │  │  Binghewusi.exe           引擎文件  
   │  │  binghewusi_strategy.py   StrategyBinghewusi类  
   │  └─ test.py                  subprocess通信测试   
   └─cyclone      象棋引擎-象棋旋风  
      │  cyclone.exe 引擎文件  
      │  cyclone_strategy.py StrategyCyclone类  
      └─ test.py subprocess通信测试  


