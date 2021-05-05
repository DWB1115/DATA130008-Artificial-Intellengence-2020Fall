import random
import pisqpipe as pp
from collections import defaultdict as ddict

DIST = 1

MAX_BOARD = 100
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]


class MCTS:
    '''
        Monte Carlo Tree Search with Heuristics.
    '''

    def __init__(self, board):
        self.board = board
        # root node do not have parent ,and sure with prior probability 1
        self.direct_dict = {
            'r': [(1, 0), (-1, 0)],
            'c': [(0, 1), (0, -1)],
            'm': [(1, -1), (-1, 1)],
            'v': [(1, 1), (-1, -1)]
        }
        self.scores = ddict(lambda: 0.0)
        self.count_dict = [[], ddict(lambda:0), ddict(lambda:0)]
        # self.count_cache = {
        #     1: {
        #         'r': ddict(int),
        #         'c': ddict(int),
        #         'm': ddict(int),
        #         'v': ddict(int)
        #     },
        #     2: {
        #         'r': ddict(int),
        #         'c': ddict(int),
        #         'm': ddict(int),
        #         'v': ddict(int)
        #     }
        # }
        self.init_count()

    def init_count(self):
        for i in range(pp.width):
            for j in range(pp.height):
                if self.board[i][j] == 0:
                    self.get_point_count(i, j, 1)
                    self.get_point_count(i, j, 2)

    def get_point_count(self, x, y, role):
        target_direct_list = list(self.direct_dict.keys())
        for target_direct in target_direct_list:
            direct = self.direct_dict[target_direct]
            count = 1
            for k in range(len(direct)):
                i = x
                j = y
                while True:
                    i += direct[k][0]
                    j += direct[k][1]
                    t = self.board[i][j]
                    if t == role:
                        count += 1
                        continue
                    # elif empty == 0 and (0 < i < scale - 1 or not direct[k][0]) \
                    #         and (0 < j < scale - 1 or not direct[k][1]) and \
                    #         self.board[i + direct[k][0]][j + direct[k][1]] == role:
                    #     empty = 1
                    #     continue
                    else:
                        break
            # self.count_cache[role][target_direct][(x, y)] = count
            self.count_dict[role][(x, y)] = max(
                self.count_dict[role][(x, y)], count)

    def nowFree(self, x, y):
        return x >= 0 and y >= 0 and x < pp.width and y < pp.height and self.board[x][y] == 0

    def nowOccupied(self, x, y):
        return self.board[x][y] != 0

    def now_has_neighbor(self, move, dist=DIST):
        x, y = move
        if not self.nowFree(x, y):
            return False
        for i in range(-dist, dist + 1):
            for j in range(-dist, dist + 1):
                if self.nowOccupied(x + i, y + j):
                    return True
        return False

    def is_five(self, x, y, role):
        scale = pp.height
        directs = list(self.direct_dict.values())
        for direct in directs:
            count = 1
            for k in range(len(direct)):
                i = x + direct[k][0]
                j = y + direct[k][1]
                while True:
                    if i >= scale or j >= scale or i < 0 or j < 0 or self.board[i][j] != role:
                        break
                    else:
                        count += 1
                        i += direct[k][0]
                        j += direct[k][1]
            if count >= 5:
                return True
        return False

    def get_winner(self):
        for i in range(pp.width):
            for j in range(pp.height):
                role = self.board[i][j]
                if role and self.is_five(i, j, role):
                    return role
        return False

    def get_possible_moves(self):
        move_list = []
        for x in range(pp.width):
            for y in range(pp.height):
                if self.now_has_neighbor((x, y)):
                    move_list.append((x, y))
        return move_list

    def get_best_move(self, times=200):
        my_max = max(list(self.count_dict[1].items()), key=lambda x: x[1])
        enemy_max = max(list(self.count_dict[2].items()), key=lambda x: x[1])
        if my_max[1] >= 5:
            return my_max[0]
        elif enemy_max[1] >= 5:
            return enemy_max[0]
        elif my_max[1] == 4:
            return my_max[0]
        elif enemy_max[1] == 4:
            return enemy_max[0]
        else:
            moves = self.get_possible_moves()
            for move in moves:
                x, y = move
                self.board[x][y] = 1
                for _ in range(times):
                    r = self.simulation(role=2)
                    self.scores[move] += r
                self.board[x][y] = 0
            return max(moves, key=lambda x: self.scores[x]) if moves else None

    def is_full(self):
        sign = True
        for i in range(pp.width):
            for j in range(pp.height):
                if self.board[i][j] == 0:
                    sign = False
        return sign

    def is_teriminal(self):
        winner = self.get_winner()
        if not winner:
            return "draw" if self.is_full() else False
        else:
            return winner

    def simulation(self, role):
        who = self.is_teriminal()
        if who == "draw":
            return 0.5
        elif who == 1:
            return 1.0
        elif who == 2:
            return 0.0
        else:
            my_max = max(list(self.count_dict[1].items()), key=lambda x: x[1])
            enemy_max = max(
                list(self.count_dict[2].items()), key=lambda x: x[1])
            if my_max[1] >= 5:
                x, y = my_max[0]
                self.board[x][y] = role
                self.update_point_count(x, y, role)
                v = self.simulation(3 - role)
                self.board[x][y] = 0
                self.update_point_count(x, y, 0)
            elif enemy_max[1] >= 5:
                x, y = enemy_max[0]
                self.board[x][y] = role
                self.update_point_count(x, y, role)
                v = self.simulation(3 - role)
                self.board[x][y] = 0
                self.update_point_count(x, y, 0)
            elif my_max[1] == 4:
                x, y = my_max[0]
                self.board[x][y] = role
                self.update_point_count(x, y, role)
                v = self.simulation(3 - role)
                self.board[x][y] = 0
                self.update_point_count(x, y, 0)
            elif enemy_max[1] == 4:
                x, y = enemy_max[0]
                self.board[x][y] = role
                self.update_point_count(x, y, role)
                v = self.simulation(3 - role)
                self.board[x][y] = 0
                self.update_point_count(x, y, 0)
            else:
                moves = self.get_possible_moves()
                x, y = moves[random.randint(0, len(moves)-1)]
                self.board[x][y] = role
                v = self.simulation(3 - role)
                self.board[x][y] = 0
                return v

    def update_point_count(self, x, y, role, radius=6):
        scale = pp.height
        for target_direct in list(self.direct_dict.keys()):
            direct = self.direct_dict[target_direct][0]
            for w in (-1, 1):
                block_1 = block_2 = False
                for r in range(1, radius + 1):
                    i = x + direct[0] * w * r
                    j = y + direct[1] * w * r
                    if i < 0 or j < 0 or i >= scale or j >= scale:
                        break
                    if not block_1:
                        if self.board[i][j] == 2:
                            block_1 = True
                        else:
                            self.update_function(i, j, self.board[i][j])
                    if not block_2:
                        if self.board[i][j] == 1:
                            block_2 = True
                        else:
                            self.update_function(i, j, self.board[i][j])
        self.update_function(x, y, role)

    def update_function(self, x, y, role):
        if role == 0:
            self.get_point_count(x, y, 1)
            self.get_point_count(x, y, 2)
        else:
            del self.count_dict[1][(x, y)]
            del self.count_dict[2][(x, y)]


def choose_move(cur_board):
    best_move = [8, 6]
    mct = MCTS(board=cur_board)
    move = mct.get_best_move(times=10)
    if move:
        best_move = move
    return best_move
