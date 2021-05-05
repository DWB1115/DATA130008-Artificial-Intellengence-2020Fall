"""
Training the network
self-learnings
"""

import os
import pickle
import random
import time
import board
from CriticalNetwork import CriticNetwork, ActionNetwork

# TODO: 保存结果
WORK_FOLDER = r"D:\课程\人工智能\adp"
CRITIC_NETWORK_SAVEPATH = WORK_FOLDER + r'\critic_network'

ME = 1
OPPONENT = 2
OBJECTIVE_MY = 1
OBJECTIVE_OPPONENTS = 0
MAX_BOARD = 25

cur_board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]

board = board.Board(cur_board=cur_board, size=(20, 20))

action_network_me = ActionNetwork(objective=OBJECTIVE_MY, EPSILON=0.25)
action_network_opponent = ActionNetwork(objective=OBJECTIVE_OPPONENTS, EPSILON=0.25)

critic_network = CriticNetwork(params=[100 * 4 + 2, 64, 1])  # 神经网络结构
# TODO:输入层大小要显式地算出来

if os.path.exists(CRITIC_NETWORK_SAVEPATH):
    critic_network.layers = pickle.load(open(CRITIC_NETWORK_SAVEPATH, 'rb'))


def get_candidate(role):
    moves = board.get_moves()  # 返回临近的点
    mv_values = []
    for move in moves:
        board.toMove(move, role)
        mv_values.append(critic_network.forward(board))
        board.toDraw(move)
        # x, y = action
        # # 能不能不用deepcopy
        # board_next = board.deepcopy()
        # board_next[x][y] = role
        # values.append(critic_network.forward(board_next))
    return moves, mv_values


win_record = []

for i in range(10000):
    start_t = time.time()
    while board.win is None:
        if board.whose_turn is None:
            board.whose_turn = random.choice([ME, OPPONENT])

        if board.whose_turn == ME:
            # print("my_move:", end=' ')
            moves, values = get_candidate(ME)
            move, value = action_network_me.forward(moves, values)
            # print(str(move))
            # board_now = deepcopy(board)
            # board[action[0]][action[1]] = ME  # pp.do_mymove here
            reward = 1.0 if (board.win is not None and board.win) else 0.0
            critic_network.back_propagation(board, move, role=ME, reward=reward)
        else:
            # print('OPPONENT\'S TURN:')
            # print("oppo_move:", end=' ')
            moves, values = get_candidate(OPPONENT)
            move, value = action_network_opponent.forward(moves, values)
            # print(str(move))
            # board_now = deepcopy(board)
            # board[action[0]][action[1]] = OPPONENT  # pp.do_mymove here
            # reward = 0.0
            critic_network.back_propagation(board, move, role=OPPONENT, reward=0)
    end_t = time.time()
    print('Game %s set. Winner: ' % i + ('ME' if board.win else 'OPPONENT'))
    print('train time:', end_t - start_t)
    win_record.append('ME' if board.win else 'OPPONENT')
    try:
        with open(CRITIC_NETWORK_SAVEPATH, 'wb') as f:
            pickle.dump(critic_network.layers, f)
            f.close()
    except:
        print('Save model failed')
    board.reset()
# print('Win record: ' + str(win_record))
