from copy import deepcopy
from collections import defaultdict as ddict

# count to chess 打表
# key: (左堵, 左段, 中心段, 右段, 右堵) value:棋形id
chessDict = {
    # 无空点
    # 活一
    (0, 0, 1, 0, 0): 1,
    # 眠一
    (1, 0, 1, 0, 0): 2,
    (0, 0, 1, 0, 1): 2,
    # 活二
    (0, 0, 2, 0, 0): 3,
    # 眠二
    (1, 0, 2, 0, 0): 4,
    (0, 0, 2, 0, 1): 4,
    # 活三
    (0, 0, 3, 0, 0): 5,
    # 眠三
    (1, 0, 3, 0, 0): 6,
    (0, 0, 3, 0, 1): 6,
    # 活四
    (0, 0, 4, 0, 0): 7,
    # 眠四
    (1, 0, 4, 0, 0): 8,
    (0, 0, 4, 0, 1): 8,

    # 一个空点, 无堵点
    # Question: 是否应该与活二等同?

    # 跳二
    # count = 2
    (0, 1, 1, 0, 0): 9,
    (0, 0, 1, 1, 0): 9,
    # 跳三
    # count = 3
    (0, 1, 2, 0, 0): 10,
    (0, 0, 2, 1, 0): 10,
    (0, 2, 1, 0, 0): 10,
    (0, 0, 1, 2, 0): 10,
    # 跳四
    # count = 4
    (0, 0, 3, 1, 0): 11,
    (0, 1, 3, 0, 0): 11,
    (0, 0, 1, 3, 0): 11,
    (0, 3, 1, 0, 0): 11,
    # 另一种跳四
    (0, 0, 2, 2, 0): 12,
    (0, 2, 2, 0, 0): 12,
    # count = 5
    (0, 0, 3, 2, 0): 13,
    (0, 2, 3, 0, 0): 13,
    (0, 0, 2, 3, 0): 13,
    (0, 3, 2, 0, 0): 13,
    # count = 6
    (0, 0, 3, 3, 0): 14,
    (0, 3, 3, 0, 0): 14,

    # 活四
    (0, 0, 4, 1, 0): 7,
    (0, 1, 4, 0, 0): 7,
    (0, 0, 4, 2, 0): 7,
    (0, 2, 4, 0, 0): 7,
    (0, 0, 4, 3, 0): 7,
    (0, 3, 4, 0, 0): 7,

    # 一个空点，一个堵点
    # 空点和堵点共侧
    # count = 2
    # 210[1]0
    (1, 1, 1, 0, 0): 15,
    (0, 0, 1, 1, 1): 15,
    # count = 3
    # 210[1]10, 21[1]01
    (1, 1, 2, 0, 0): 16,
    (1, 2, 1, 0, 0): 17,
    (0, 0, 2, 1, 1): 16,
    (0, 0, 1, 2, 1): 17,
    # count >= 4
    # 21101[1]0
    (1, 2, 2, 0, 0): 18,
    (0, 0, 2, 2, 1): 18,
    # 21110[1]0, 21011[1]0
    (1, 3, 1, 0, 0): 19,
    (1, 1, 3, 0, 0): 20,
    (1, 3, 2, 0, 0): 21,
    (1, 2, 3, 0, 0): 22,
    (0, 0, 1, 3, 1): 19,
    (0, 0, 3, 1, 1): 20,
    (0, 0, 2, 3, 1): 21,
    (0, 0, 3, 2, 1): 22,
    # 210[1]1110, 211110[1]0
    (1, 1, 4, 0, 0): 7,
    (1, 4, 1, 0, 0): 23,
    (0, 0, 4, 1, 1): 7,
    (0, 0, 1, 4, 1): 23,
    # 2110111[1]0, 2111101[1]0
    (1, 2, 4, 0, 0): 7,
    (1, 4, 2, 0, 0): 24,
    (0, 0, 4, 2, 1): 7,
    (0, 0, 2, 4, 1): 24,
    # 21110111[1]0, 21111011[1]0
    (1, 3, 4, 0, 0): 7,
    (1, 4, 3, 0, 0): 25,
    (0, 0, 4, 3, 1): 7,
    (0, 0, 3, 4, 1): 25,
    # 211110111[1]0
    (1, 4, 4, 0, 0): 7,
    (0, 0, 4, 4, 1): 7,

    # 一个空点，一个堵点
    # 空点和堵点异侧
    # count = 2
    # 2[1]010
    (1, 0, 1, 1, 0): 26,
    (0, 1, 1, 0, 1): 26,
    # count = 3
    # 2[1]1010, 2[1]0110
    (1, 0, 2, 1, 0): 27,
    (1, 0, 1, 2, 0): 28,
    (0, 1, 2, 0, 1): 27,
    (0, 2, 1, 0, 1): 28,
    # count >= 4
    # 21[1]0110
    (1, 0, 2, 2, 0): 29,
    (0, 2, 2, 0, 1): 29,
    # 211[1]010, 2[1]01110
    (1, 0, 1, 3, 0): 30,
    (1, 0, 3, 1, 0): 31,
    (1, 0, 2, 3, 0): 32,
    (1, 0, 3, 2, 0): 33,
    (0, 3, 1, 0, 1): 30,
    (0, 1, 3, 0, 1): 31,
    (0, 3, 2, 0, 1): 32,
    (0, 2, 3, 0, 1): 33,
    # 2[1]011110, 2[1]111010
    (1, 0, 4, 1, 0): 34,
    (1, 0, 1, 4, 0): 35,
    (0, 1, 4, 0, 1): 34,
    (0, 4, 1, 0, 1): 35,
    # 2110111[1]0, 2111101[1]0
    (1, 0, 4, 2, 0): 36,
    (1, 0, 2, 4, 0): 37,
    (0, 2, 4, 0, 1): 36,
    (0, 4, 2, 0, 1): 37,
    # 21110111[1]0, 21111011[1]0
    (1, 0, 4, 3, 0): 38,
    (1, 0, 3, 4, 0): 39,
    (0, 3, 4, 0, 1): 38,
    (0, 4, 3, 0, 1): 39,
    # 211110111[1]0
    (1, 0, 4, 4, 0): 40,
    (0, 4, 4, 0, 1): 40,

    # 一个空点，两个堵点。
    # 当且仅当 count>= 4时，返回眠四
    # Question: 两个堵点与一个堵点的得分一致, 这合理吗?

    # 21[1]0112
    (1, 0, 2, 2, 1): 41,
    (1, 2, 2, 0, 1): 41,
    # 211[1]012, 2[1]01112
    (1, 0, 1, 3, 1): 42,
    (1, 0, 3, 1, 1): 43,
    (1, 0, 2, 3, 1): 44,
    (1, 0, 3, 2, 1): 45,
    (1, 3, 1, 0, 1): 42,
    (1, 1, 3, 0, 1): 43,
    (1, 3, 2, 0, 1): 44,
    (1, 2, 3, 0, 1): 45,
    # 2[1]011110, 2[1]111010
    (1, 0, 4, 1, 1): 46,
    (1, 0, 1, 4, 1): 47,
    (1, 1, 4, 0, 1): 46,
    (1, 4, 1, 0, 1): 47,
    # 2110111[1]0, 2111101[1]0
    (1, 0, 4, 2, 1): 48,
    (1, 0, 2, 4, 1): 49,
    (1, 2, 4, 0, 1): 48,
    (1, 4, 2, 0, 1): 49,
    # 21110111[1]0, 21111011[1]0
    (1, 0, 4, 3, 1): 50,
    (1, 0, 3, 4, 1): 51,
    (1, 3, 4, 0, 1): 50,
    (1, 4, 3, 0, 1): 51,
    # 211110111[1]0
    (1, 0, 4, 4, 1): 52,
    (1, 4, 4, 0, 1): 52,

    # 两个空点
    # TODO: 1.采取 两侧相加 的策略 2.中心为四尚未考虑
    # 无堵点
    # 010[1]010
    (0, 1, 1, 1, 0): 53,
    (0, 1, 2, 1, 0): 54,
    (0, 1, 3, 1, 0): 55,
    # 0110[1]010
    (0, 3, 1, 2, 0): 56,
    (0, 2, 1, 3, 0): 56,
    (0, 3, 1, 3, 0): 57,

    (0, 2, 2, 1, 0): 58,
    (0, 1, 2, 2, 0): 58,
    (0, 2, 2, 2, 0): 59,

    (0, 3, 2, 2, 0): 60,
    (0, 2, 2, 3, 0): 60,
    (0, 3, 2, 3, 0): 61,
    (0, 1, 3, 2, 0): 62,
    (0, 2, 3, 1, 0): 62,
    (0, 2, 3, 2, 0): 63,
    (0, 3, 3, 1, 0): 64,
    (0, 1, 3, 3, 0): 64,
    (0, 3, 3, 2, 0): 65,
    (0, 2, 3, 3, 0): 65,
    (0, 3, 3, 3, 0): 66,

    # 一个堵点
    # 210[1]010
    (1, 1, 1, 1, 0): 67,
    (1, 1, 2, 1, 0): 68,
    (1, 1, 3, 1, 0): 69,
    (0, 1, 1, 1, 1): 67,
    (0, 1, 2, 1, 1): 68,
    (0, 1, 3, 1, 1): 69,

    # 2110[1]010
    (1, 3, 1, 2, 0): 70,
    (1, 2, 1, 3, 0): 71,
    (1, 3, 1, 3, 0): 72,
    (0, 2, 1, 3, 1): 70,
    (0, 3, 1, 2, 1): 71,
    (0, 3, 1, 3, 1): 72,

    # TODO: too much chess
    # 21101[1]010
    (1, 2, 2, 1, 0): 73,
    (1, 1, 2, 2, 0): 74,
    (1, 2, 2, 2, 0): 75,
    (0, 1, 2, 2, 1): 73,
    (0, 2, 2, 1, 1): 74,
    (0, 2, 2, 2, 1): 75,

    (1, 3, 2, 2, 0): 76,
    (1, 2, 2, 3, 0): 77,
    (1, 3, 2, 3, 0): 78,
    (1, 1, 3, 2, 0): 79,
    (1, 2, 3, 1, 0): 80,
    (1, 2, 3, 2, 0): 81,
    (1, 3, 3, 1, 0): 82,
    (1, 1, 3, 3, 0): 83,
    (1, 3, 3, 2, 0): 84,
    (1, 2, 3, 3, 0): 85,
    (1, 3, 3, 3, 0): 86,

    (0, 3, 2, 2, 1): 77,
    (0, 2, 2, 3, 1): 76,
    (0, 3, 2, 3, 1): 78,
    (0, 1, 3, 2, 1): 80,
    (0, 2, 3, 1, 1): 79,
    (0, 2, 3, 2, 1): 81,
    (0, 3, 3, 1, 1): 83,
    (0, 1, 3, 3, 1): 82,
    (0, 3, 3, 2, 1): 85,
    (0, 2, 3, 3, 1): 84,
    (0, 3, 3, 3, 1): 86,

    # 两个堵点
    # 010[1]010
    (1, 1, 1, 1, 1): 87,
    (1, 1, 2, 1, 1): 88,
    (1, 1, 3, 1, 1): 89,
    # 0110[1]010
    (1, 3, 1, 2, 1): 90,
    (1, 2, 1, 3, 1): 90,
    (1, 3, 1, 3, 1): 91,

    (1, 2, 2, 1, 1): 92,
    (1, 1, 2, 2, 1): 92,
    (1, 2, 2, 2, 1): 93,

    # 双方 count>=4
    (1, 3, 2, 2, 1): 94,
    (1, 2, 2, 3, 1): 94,
    (1, 3, 2, 3, 1): 95,
    (1, 1, 3, 2, 1): 96,
    (1, 2, 3, 1, 1): 96,
    (1, 2, 3, 2, 1): 97,
    (1, 3, 3, 1, 1): 98,
    (1, 1, 3, 3, 1): 98,
    (1, 3, 3, 2, 1): 99,
    (1, 2, 3, 3, 1): 99,
    (1, 3, 3, 3, 1): 100,

}


class Board(object):
    def __init__(self, cur_board, size, whose_turn=1):
        self.origin_board = deepcopy(cur_board)
        self.board = deepcopy(cur_board)
        self.size = size

        self.features1 = ddict(int)  # 己方特征数量
        self.features2 = ddict(int)  # 对方特征数量

        self.whose_turn = whose_turn
        self.win = None
        self.num_steps = 0

        # row, colomn, main diagonal, vice diagonal 四个方向；类似矩阵中的方向命名。
        self.direct_dict = {
            'r': [(1, 0), (-1, 0)],
            'c': [(0, 1), (0, -1)],
            'm': [(1, -1), (-1, 1)],
            'v': [(1, 1), (-1, -1)]
        }
        self.chess_cache = {
            1: {
                'r': ddict(int),
                'c': ddict(int),
                'm': ddict(int),
                'v': ddict(int)
            },
            2: {
                'r': ddict(int),
                'c': ddict(int),
                'm': ddict(int),
                'v': ddict(int)
            }
        }
        self.init_chess()

    def reset(self):
        self.board = deepcopy(self.origin_board)
        self.features1 = ddict(int)  # 己方特征数量
        self.features2 = ddict(int)  # 对方特征数量

        self.win = None
        self.whose_turn = 1
        self.num_steps = 0

        self.chess_cache = {
            1: {
                'r': ddict(int),
                'c': ddict(int),
                'm': ddict(int),
                'v': ddict(int)
            },
            2: {
                'r': ddict(int),
                'c': ddict(int),
                'm': ddict(int),
                'v': ddict(int)
            }
        }
        self.init_chess()

    def init_chess(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                # 不需要继续为空白节点打分了
                # if self.board[i][j] == 0:
                #     self.get_chess(i, j, 1)
                #     self.get_chess(i, j, 2)
                if self.board[i][j] == 1:
                    self.get_chess(i, j, 1)
                elif self.board[i][j] == 2:
                    self.get_chess(i, j, 2)

    def nowFree(self, x, y):
        return self.size[0] > x >= 0 <= y < self.size[1] and self.board[x][y] == 0

    def nowOccupied(self, x, y):
        return self.board[x][y] != 0

    def now_has_neighbor(self, move, dist=1):
        x, y = move
        if not self.nowFree(x, y):
            return False
        for i in range(-dist, dist + 1):
            for j in range(-dist, dist + 1):
                if self.nowOccupied(x + i, y + j):
                    return True
        return False

    def get_moves(self):
        move_list = []
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if self.now_has_neighbor((x, y)):
                    move_list.append((x, y))
        if not move_list:
            return [(10, 10)]
        return move_list

    # 对某个特定点，获得棋形
    def get_chess(self, x, y, role, direction=None):
        # 完善打分模组
        enemy = 3 - role
        if direction is None:
            target_direct_list = list(self.direct_dict.keys())
        else:
            target_direct_list = [direction]

        scale = self.size[0]
        for target_direct in target_direct_list:
            direct = self.direct_dict[target_direct]
            # 计数
            count = 0
            # 封堵
            block = [0, 0]
            # 中心连续棋子 # 非中心连续棋子
            cc = [[1, 0], [0, 0]]
            # 空点，两边最多可忍受的空点数目均为1
            empty = [0, 0]
            for k in range(len(direct)):
                i = x
                j = y
                while True:
                    i += direct[k][0]
                    j += direct[k][1]
                    t = self.board[i][j]
                    # 从中心向两边扫描
                    # 堵，退出
                    if i >= scale or j >= scale or i < 0 or j < 0 or t == enemy:
                        block[k] += 1
                        break

                    elif t == role:
                        count += 1
                        cc[empty[k]][k] += 1
                        continue

                    elif empty[k] == 0 and (0 < i < scale - 1 or not direct[k][0]) \
                            and (0 < j < scale - 1 or not direct[k][1]) and \
                            self.board[i + direct[k][0]][j + direct[k][1]] == role:
                        empty[k] = 1
                        continue

                    else:
                        break

            chess_id = 0
            # 未将此情况包含在字典内
            if sum(cc[0]) >= 5:
                chess_id = 101
            elif sum(empty) == 2 and sum(cc[0]) == 4:
                chess_id = 7
            else:
                key = (block[0], cc[1][0], sum(cc[0]), cc[1][1], block[1])
                if key in chessDict:
                    chess_id = chessDict[key]

            if role == 1:
                if self.features1[self.chess_cache[role][target_direct][(x, y)]]:
                    self.features1[self.chess_cache[role][target_direct][(x, y)]] -= 1
                self.chess_cache[role][target_direct][(x, y)] = chess_id
                self.features1[chess_id] += 1
            elif role == 2 and self.features2[self.chess_cache[role][target_direct][(x, y)]]:
                if self.features2[self.chess_cache[role][target_direct][(x, y)]]:
                    self.features2[self.chess_cache[role][target_direct][(x, y)]] -= 1
                self.chess_cache[role][target_direct][(x, y)] = chess_id
                self.features2[chess_id] += 1

    def update_chess(self, x, y, role, radius=8):
        scale = self.size[0]
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
                            self.quick_update_function(i, j, self.board[i][j], target_direct)
                    if not block_2:
                        if self.board[i][j] == 1:
                            block_2 = True
                        else:
                            self.quick_update_function(i, j, self.board[i][j], target_direct)
        self.update_function(x, y, role)

    # BLU
    def quick_update_function(self, x, y, role, direction):
        if role == 1:
            self.get_chess(x, y, 1, direction)
        elif role == 2:
            self.get_chess(x, y, 2, direction)
        else:
            pass

    def update_function(self, x, y, role):
        if role == 1:
            self.get_chess(x, y, 1)
        elif role == 2:
            self.get_chess(x, y, 2)
        else:
            target_direct_list = list(self.direct_dict.keys())
            for target_direct in target_direct_list:
                if self.features1[self.chess_cache[1][target_direct][(x, y)]]:
                    self.features1[self.chess_cache[1][target_direct][(x, y)]] -= 1
                    self.chess_cache[1][target_direct][(x, y)] = 0
                elif self.features2[self.chess_cache[2][target_direct][(x, y)]]:
                    self.features2[self.chess_cache[2][target_direct][(x, y)]] -= 1
                    self.chess_cache[2][target_direct][(x, y)] = 0

    def is_five(self, x, y, role):
        scale = self.size[0]
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

    # 使用点更新?
    def update_features(self, move, role):
        if role == 0:  # 撤回上一步
            self.toDraw(move)
        else:
            self.toMove(move, role)

    # 落子函数
    def toMove(self, move, role):
        if move:
            x, y = move
            if self.win is None and self.is_five(x, y, role):
                self.win = (role == 1)

            self.board[x][y] = role
            self.update_chess(x, y, role)

            self.whose_turn = 1 if role == 2 else 2
            self.num_steps += 1

    # 悔子函数
    def toDraw(self, move):
        if move:
            x, y = move
            self.board[x][y] = 0
            self.update_chess(x, y, 0)

            self.whose_turn = 1 if self.whose_turn == 2 else 2
            self.num_steps -= 1

    # def load(self, filename, whose_turn):
    #     f = open(filename, 'r')
    #     for line in f.readlines():
    #         start = line.index('[')
    #         end = line.index(']') + 1
    #         where = eval(line[start:end])
    #         self.board[where[0]][where[1]] = whose_turn
    #         whose_turn = 1 if whose_turn == 2 else 2


if __name__ == '__main__':
    board = Board(20)
    board_copy = board.deepcopy()
    board_copy[0][0] = 1
    pass
