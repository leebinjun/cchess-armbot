# 封装成类，输入FEN棋盘描述串，返回黑棋移动策略

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import sys
import multiprocessing as mp
    
_PATH_ = os.path.dirname(os.path.dirname(__file__))

if _PATH_ not in sys.path:
    sys.path.append(_PATH_)

import sys
import pygame
import random
import os.path
import time
import copy
import numpy as np

from pygame.locals import *
from logging import getLogger
from collections import defaultdict
from threading import Thread
from time import sleep
from datetime import datetime

from cchess_alphazero.environment.chessboard import Chessboard
from cchess_alphazero.environment.chessman import *
from cchess_alphazero.agent.model import CChessModel
from cchess_alphazero.agent.player import CChessPlayer, VisitState
from cchess_alphazero.agent.api import CChessModelAPI
from cchess_alphazero.config import Config
from cchess_alphazero.environment.env import CChessEnv
from cchess_alphazero.environment.lookup_tables import Winner, ActionLabelsRed, flip_move
from cchess_alphazero.lib.model_helper import load_best_model_weight
from cchess_alphazero.lib.tf_util import set_session_config

from cchess_alphazero.play_games.play import PlayWithHuman
from cchess_alphazero.environment import static_env as senv

import argparse
import multiprocessing as mp

from logging import getLogger

from cchess_alphazero.lib.logger import setup_logger
from cchess_alphazero.config import Config, PlayWithHumanConfig

logger = getLogger(__name__)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

CMD_LIST = ['self', 'opt', 'eval', 'play', 'eval', 'sl', 'ob']
PIECE_STYLE_LIST = ['WOOD', 'POLISH', 'DELICATE']
BG_STYLE_LIST = ['CANVAS', 'DROPS', 'GREEN', 'QIANHONG', 'SHEET', 'SKELETON', 'WHITE', 'WOOD']
RANDOM_LIST = ['none', 'small', 'medium', 'large']

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cmd", help="what to do", choices=CMD_LIST, default="play")
    parser.add_argument("--new", help="run from new best model", action="store_true")
    parser.add_argument("--type", help="use normal setting", default="mini")
    parser.add_argument("--total-step", help="set TrainerConfig.start_total_steps", type=int)
    parser.add_argument("--ai-move-first", help="set human or AI move first", action="store_true")
    parser.add_argument("--cli", help="play with AI with CLI, default with GUI", action="store_true")
    parser.add_argument("--gpu", help="device list", default="0")
    parser.add_argument("--onegreen", help="train sl work with onegreen data", action="store_true")
    parser.add_argument("--skip", help="skip games", default=0, type=int)
    parser.add_argument("--ucci", help="play with ucci engine instead of self play", action="store_true")
    parser.add_argument("--piece-style", help="choose a style of piece", choices=PIECE_STYLE_LIST, default="WOOD")
    parser.add_argument("--bg-style", help="choose a style of board", choices=BG_STYLE_LIST, default="WOOD")
    parser.add_argument("--random", help="choose a style of randomness", choices=RANDOM_LIST, default="none")
    parser.add_argument("--distributed", help="whether upload/download file from remote server", action="store_true")
    parser.add_argument("--elo", help="whether to compute elo score", action="store_true")
    return parser

def setup(config: Config, args):
    config.opts.new = args.new
    if args.total_step is not None:
        config.trainer.start_total_steps = args.total_step
    config.opts.device_list = args.gpu
    config.resource.create_directories()
    if args.cmd == 'self':
        setup_logger(config.resource.main_log_path)
    elif args.cmd == 'opt':
        setup_logger(config.resource.opt_log_path)
    elif args.cmd == 'play' or args.cmd == 'ob':
        setup_logger(config.resource.play_log_path)
    elif args.cmd == 'eval':
        setup_logger(config.resource.eval_log_path)
    elif args.cmd == 'sl':
        setup_logger(config.resource.sl_log_path)


class StrategyAlphaZero:
    sys.setrecursionlimit(10000)
    parser = create_parser()
    args = parser.parse_args()
    args.cmd = 'play'
    config_type = 'mini'
    config = Config(config_type=config_type)
    setup(config, args)
    logger.info('Config type: %s' % (config_type))
    config.opts.piece_style = args.piece_style
    config.opts.bg_style = args.bg_style
    config.internet.distributed = args.distributed
    if args.cli:
        import cchess_alphazero.play_games.play_cli as play
    else:
        from cchess_alphazero.play_games import play
    config.opts.light = False
    pwhc = PlayWithHumanConfig()
    logger.info(f"AI move first : {args.ai_move_first}")
    logger = getLogger(__name__)
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    PIECE_STYLE = 'WOOD'
    
    
    # USE:
    # state 开局FEN字符串
    # rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1
    # rkemsmekr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RKEMSMEKR
    state = "r2k4C/1PN1P1c2/5c3/9/9/9/9/9/3p1p3/4KA3"  ##
                # mess_board = "4k4/9/9/9/1R2n2Rp/9/4p4/5p3/4p4/3p1K3"
            # mess_board = "3ak4/4a4/9/5N3/8C/6B2/9/4KA1p1/9/5A1r1"
            # mess_board = "3a5/3ka3r/9/9/9/9/2R6/9/4K3C/9"
            # mess_board = "3rka1R1/4aR3/4b4/9/9/9/4r4/p3C4/3p5/c1BA1K3"
            # mess_board = "2bak2r1/4aP2R/2R1b4/8p/1Np6/2C6/8P/9/3pr4/5K2c"
    # state = "4k4/9/9/9/1R2n2Rp/9/4p4/5p3/4p4/3p1K3"
    # state = "3ak4/4a4/9/5N3/8C/6B2/9/4KA1p1/9/5A1r1"
    # state = "3a5/3ka3r/9/9/9/9/2R6/9/4K3C/9"
    # state = "3rka1R1/4aR3/4b4/9/9/9/4r4/p3C4/3p5/c1BA1K3"
    # state = "2bak2r1/4aP2R/2R1b4/8p/1Np6/2C6/8P/9/3pr4/5K2c"
    # state =  "r8/3k5/9/9/9/9/9/9/4A4/3AK4"
    # state = "r8/3k5/9/9/9/9/9/9/4A4/3AK4"
    # MTCS 搜索局数
    pwhc.simulation_num_per_move = 200
    
    pwhc.update_play_config(config.play)
    play = PlayWithHuman(config)
    play.start(not args.ai_move_first, init_s=state)
    
    

if __name__ == "__main__":
    ai = StrategyAlphaZero()

