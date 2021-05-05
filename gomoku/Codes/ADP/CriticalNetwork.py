from NeuralNetwork import *
import os
import pickle


class CriticNetwork:
    def __init__(self, params):

        # 超参数
        self.ALPHA = 1
        self.LEARNING_RATE = 0.1
        self.MAGNIFY = 1
        activator = SigmoidActivator()

        # 建构神经网络
        self.layers = []
        for i in range(len(params) - 1):
            self.layers.append(FullConnectedLayer(params[i], params[i + 1], activator))

        # 获胜与失败序列?
        # self.losing_encodings = [
        #     pattern_finder.get_encoding('-xxxx'),
        #     pattern_finder.get_encoding('x-xxx'),
        #     pattern_finder.get_encoding('xx-xx'),
        # ]
        # self.winning_encodings = [
        #     pattern_finder.get_encoding('-oooo'),
        #     pattern_finder.get_encoding('o-ooo'),
        #     pattern_finder.get_encoding('oo-oo'),
        # ]

    # 神经网络也可以从文件提取
    def load_layers(self, filepath):
        if os.path.exists(filepath):
            self.layers = pickle.load(open(filepath, 'rb'))
        else:
            raise Exception('File ' + filepath + ' does not exist')

    # 特征提取，此处的架构与ADP-MCTS一致
    def extract_features(self, board):
        # logDebug('board features: '+ str(board.features))
        flattened_features = []
        for i in range(1, 101):
            flattened_features.append(board.features1[i])
            flattened_features.append(board.features2[i])
            flattened_features.append(board.whose_turn - 1)
            flattened_features.append(2 - board.whose_turn)
        return np.asarray(flattened_features + [board.whose_turn - 1, 2 - board.whose_turn]).reshape(-1, 1)
        # for feature in board.features:
        #     for i in range(4):
        #         flattened_features.append(int(feature > i))
        #     flattened_features.append((feature - 4) / 2 if feature > 4 else 0)
        # return np.asarray(flattened_features + [board.whose_turn - 1, 2 - board.whose_turn]).reshape(-1, 1)
        # return np.random.rand(200, 1)

    # TODO: 能不能不维护board类？
    def forward(self, board):
        # 前向计算，返回获胜概率
        if board.win is not None:
            return 1 if board.win else 0

        # if board.whose_turn == 1:
        #     for index in self.winning_encodings:
        #         if board.features[index] > 0:
        #             return 1
        #
        # if board.whose_turn == 2:
        #     for index in self.losing_encodings:
        #         if board.features[index] > 0:
        #             return 0

        output = self.extract_features(board)

        for layer in self.layers:
            layer.forward(output)
            output = layer.output_data

        return float(output)

    # 计算梯度
    def calc_gradient(self, error):
        delta = -self.ALPHA * error  # 注意！！！
        for layer in self.layers[::-1]:
            delta = layer.backward(delta)
        # return error * delta
        return delta

    # 后向迭代
    def back_propagation(self, board, move, role, reward):
        V = self.forward(board)
        board.toMove(move, role)
        next_V = self.forward(board)

        # next_V = self.forward(board_next)
        # V = self.forward(board)

        learning_rate = self.LEARNING_RATE * self.MAGNIFY if next_V == 0 else self.LEARNING_RATE
        error = self.ALPHA * (reward + next_V - V)
        self.calc_gradient(error)

        for layer in self.layers:
            layer.update(learning_rate, mode=0)


class ActionNetwork:
    # TODO: Object 是什么东西?
    def __init__(self, objective=1, EPSILON=0.0):
        self.objective = objective
        self.EPSILON = EPSILON

    def forward(self, actions, values):
        if random.random() < self.EPSILON:  # EPSILON greedy
            zipped = list(
                filter(lambda z: abs(z[1] - self.objective) < 1, zip(actions, values)))  # 有策略的随机选择
            if len(zipped) > 0:
                random_index = random.randint(0, len(zipped) - 1)
                return zipped[random_index][0], zipped[random_index][1]
            else:
                random_index = random.randint(0, len(actions) - 1)
                return actions[random_index], values[random_index]
        else:
            best_diff_from_objective = 999
            best_value = None
            best_action = None

            for action, value in zip(actions, values):
                diff = abs(value - self.objective)
                if diff < best_diff_from_objective:
                    best_diff_from_objective, best_action, best_value = diff, action, value

            return best_action, best_value
