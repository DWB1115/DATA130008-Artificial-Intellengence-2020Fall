"""
This is a Python gomoku AI agent using alpha-beta pruning, a final PJ for class AI, FDU-DataScience

Author: DWB, ZZJ

Date: 2020.12
"""
import os
import pickle
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL
import board as bd
from CriticalNetwork import CriticNetwork, ActionNetwork

# pp.infotext = infotext
MAX_BOARD = 100
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
estimator = None
oppo_move = None

WORK_FOLDER = r"D:\课程\人工智能\adp"
CRITIC_NETWORK_SAVEPATH = WORK_FOLDER + r'\critic_network'

# f = open("C:/Users/Little_Zhang/Desktop/人工智能/finalpj/ADP-MCTS/text.txt", 'w')

action_network_me = ActionNetwork(objective=1, EPSILON=0.)
critic_network = CriticNetwork(params=[100 * 4 + 2, 64, 1])

if os.path.exists(CRITIC_NETWORK_SAVEPATH):
    critic_network.layers = pickle.load(open(CRITIC_NETWORK_SAVEPATH, 'rb'))


def get_candidate(role):
    if estimator:
        moves = estimator.get_moves()  # 返回临近的点
        # f.write(str(moves)+'\n')
        mv_values = []
        for move in moves:
            estimator.toMove(move, role)
            # f.write('try to append\n')
            mv_values.append(critic_network.forward(estimator))
            # f.write('finish append\n')
            estimator.toDraw(move)
            # x, y = action
            # # 能不能不用deepcopy
            # board_next = board.deepcopy()
            # board_next[x][y] = role
            # values.append(critic_network.forward(board_next))
        # f.write(str(mv_values)+'\n')
        return moves, mv_values
    else:
        pass


def brain_init():
    global estimator, oppo_move
    estimator = None
    oppo_move = None
    # f.write("init\n")
    if pp.width < 5 or pp.height < 5:
        pp.pipeOut("ERROR size of the board")
        return
    if pp.width > MAX_BOARD or pp.height > MAX_BOARD:
        pp.pipeOut("ERROR Maximal board size is {}".format(MAX_BOARD))
        return
    pp.pipeOut("OK")


def brain_restart():
    global estimator, oppo_move
    estimator = None
    oppo_move = None
    for x in range(pp.width):
        for y in range(pp.height):
            board[x][y] = 0
    pp.pipeOut("OK")


def isFree(x, y):
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0


def brain_my(x, y):
    if isFree(x, y):
        board[x][y] = 1
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))


def brain_opponents(x, y):
    global oppo_move, vegetable
    # f.write('oppo_turn\n')
    if isFree(x, y):
        board[x][y] = 2
        oppo_move = (x, y)
    else:
        pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))


def brain_block(x, y):
    if isFree(x, y):
        board[x][y] = 3
    else:
        pp.pipeOut("ERROR winning move [{},{}]".format(x, y))


def brain_takeback(x, y):
    if x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] != 0:
        board[x][y] = 0
        return 0
    return 2


def brain_turn():
    global estimator, oppo_move
    try:
        # f.write('my_turn\n')
        if pp.terminateAI:
            return

        if estimator is None:
            estimator = bd.Board(board, (20, 20), whose_turn=1)
            # f.write('estimator_init\n')
            # 第一步假定对方很强
            # candidates = [None]
        else:
            # candidates = estimator.get_candidates(brunch=8)
            # f.write('estimator_update\n')
            estimator.toMove(oppo_move, 2)

        # f.write(str(candidates)+"\n")
        # move_t = oppo_move
        # f.write(str(move_t) + "\n")

        # f.write('try to get candidate\n')
        moves, values = get_candidate(1)
        # f.write('try to choose move\n')
        move, value = action_network_me.forward(moves, values)
        # f.write(str(move)+'\n')
        x, y = move
        pp.do_mymove(x, y)
        # f.write('finish:do_mymove\n')
        estimator.toMove((x, y), 1)
        # f.write('estimator_update2\n')
    except:
        pass
    # logTraceBack()


def brain_end():
    pass


def brain_about():
    pp.pipeOut(pp.infotext)


if DEBUG_EVAL:
    import win32gui


    def brain_eval(x, y):
        # TODO check if it works as expected
        wnd = win32gui.GetForegroundWindow()
        dc = win32gui.GetDC(wnd)
        rc = win32gui.GetClientRect(wnd)
        c = str(board[x][y])
        win32gui.ExtTextOut(dc, rc[2] - 15, 3, 0, None, c, ())
        win32gui.ReleaseDC(wnd, dc)

######################################################################
# A possible way how to debug brains.
# To test it, just "uncomment" it (delete enclosing """)
######################################################################
"""
# define a file for logging ...
DEBUG_LOGFILE = "C:/Users/Little_Zhang/Desktop/人工智能/finalpj/Log"
# ...and clear it initially
with open(DEBUG_LOGFILE, "w") as f:
    pass


# define a function for writing messages to the file
def logDebug(msg):
    with open(DEBUG_LOGFILE, "a") as f:
        f.write(msg + "\n")
        f.flush()


# define a function to get exception traceback
def logTraceBack():
    import traceback
    with open(DEBUG_LOGFILE, "a") as f:
        traceback.print_exc(file=f)
        f.flush()
    raise


# use logDebug wherever
# use try-except (with logTraceBack in except branch) to get exception info
# an example of problematic function
# def brain_turn():
# # 	logDebug("some message 1")
# # 	try:
# # 		logDebug("some message 2")
# # 		1. / 0. # some code raising an exception
# # 		logDebug("some message 3") # not logged, as it is after error
# # 	except:
# # 		logTraceBack()
"""
######################################################################

# "overwrites" functions in pisqpipe module
pp.brain_init = brain_init
pp.brain_restart = brain_restart
pp.brain_my = brain_my
pp.brain_opponents = brain_opponents
pp.brain_block = brain_block
pp.brain_takeback = brain_takeback
pp.brain_turn = brain_turn
pp.brain_end = brain_end
pp.brain_about = brain_about
if DEBUG_EVAL:
    pp.brain_eval = brain_eval


def main():
    pp.main()


if __name__ == "__main__":
    main()
