import os
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
    pwhc.update_play_config(config.play)
    logger.info(f"AI move first : {args.ai_move_first}")
    


    logger = getLogger(__name__)
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    PIECE_STYLE = 'WOOD'

    # def start(config: Config, human_move_first=True):
    #     global PIECE_STYLE
    #     PIECE_STYLE = config.opts.piece_style
    #     play = PlayWithHuman(config)
    #     play.start(human_move_first)

    # play.start(config, not args.ai_move_first)
  
    play = PlayWithHuman(config)
    # play.start(not args.ai_move_first)
    play.env.reset(init_state="r8/3k5/9/9/9/9/9/9/4A4/3AK4")
    play.load_model()
    play.pipe = play.model.get_pipes()
    play.ai = CChessPlayer(play.config, search_tree=defaultdict(VisitState), pipes=play.pipe,
                           enable_resign=True, debugging=True)
    human_first = not args.ai_move_first
    play.human_move_first = human_first

    # pygame.init()
    # screen, board_background, widget_background = play.init_screen()
    # framerate = pygame.time.Clock()

    # labels = ActionLabelsRed
    # labels_n = len(ActionLabelsRed)

    current_chessman = None
    if human_first:
        play.env.board.calc_chessmans_moving_list()


    # state = 'r8/3s5/9/9/9/9/9/9/4M4/4SM3'
    # # state = '4s4/4m4/5m3/9/9/9/9/9/3R5/4S4'
    # # state = '5s3/4m4/5m3/9/9/9/9/9/3RS4/9'
    # # state = '5s3/4m4/5m3/9/9/9/9/9/3RS4/9'
    # # state = '9/3sm4/5m3/9/9/9/9/9/6R2/4S4'
    # no_act = None
    # # action, policy = play.ai.action(state, 0, no_act)
    # print("Herererererere:")
    # print(f"state: {state}")
    # print(f"no_act: {no_act}")
    # print(f"self.env.num_halfmoves: {play.env.num_halfmoves}")
    # action, policy = play.ai.action(state, play.env.num_halfmoves, no_act)
    # print(f"action: {action}")
    # print(f"policy: {policy}")


    
    def get_move(self, position = "rCbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/4C2C1/9/RNBAKABNR",  show_thinking = False):   
        
        mess_board = position[::-1]
        mess_board = mess_board.replace('k','S')
        mess_board = mess_board.replace('n','K')
        mess_board = mess_board.replace('b','E')
        mess_board = mess_board.replace('a','M')
        mess_board = mess_board.replace('c','C')
        mess_board = mess_board.replace('p','P')
        mess_board = mess_board.replace('r','R')
        mess_board = mess_board.replace('K','s')
        mess_board = mess_board.replace('N','k')
        mess_board = mess_board.replace('B','e')
        mess_board = mess_board.replace('A','m')
        mess_board = mess_board.replace('c','C')
        mess_board = mess_board.replace('p','P')
        mess_board = mess_board.replace('r','R')

        no_act = None
        # action, policy = play.ai.action(state, 0, no_act)
        print("Hahahahhahaha")
        print(f"state: {mess_board}")
        print(f"no_act: {no_act}")
        action, policy = self.play.ai.action(mess_board, 0, no_act)
        print(f"action: {action}")
        # print(f"policy: {policy}")
        
        l = [0,0,0,0]
        l[2] = chr(8 - int(action[2]) + 97) 
        l[3] = str(9 - int(action[3]))
        l[0] = chr(8 - int(action[0]) + 97) 
        l[1] = str(9 - int(action[1]))
        
        action = ''.join(l)

        return action


if __name__ == "__main__":
    ai = StrategyAlphaZero()
    # situation = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/2C4C1/9/RNBAKABNR"
    # move = ai.get_move(position=situation, show_thinking = True)
    # print(move)

    while True:
        situation = input()
        move = ai.get_move(position=situation, show_thinking = True)
        print(move)


