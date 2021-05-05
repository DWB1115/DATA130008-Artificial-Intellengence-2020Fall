import numpy as np
import random
import copy
import pisqpipe as pp
from collections import defaultdict as ddict
from operator import itemgetter

class Node:
    """A node in the MCTS tree.

    Attributes:
        parent: the node's parent, also a Node
        action_child_dict: <key:value>--<an action:a child node(also a Node)>
        visit_count: how many times this node is visited
        
        Each node keeps its own value Q, and its exploitation-exploration balance constant
    """
    def __init__(self, parent, role):
        self.parent = parent
        self.action_child_dict = dict()  # <key : value> = <action : nextboard(also a Node)> 
        self.visit_count = 0   # record how many times do this node have being visited
        self.Q = 0  # its own value
        self.u = 0
        self.role = role
    
    def is_leaf(self):
        return len(self.action_child_dict) == 0

    def is_root(self):
        return self.parent is None

    def Select(self, c_puct):
        return max(self.action_child_dict.items(),
                   key=lambda x: x[1].get_value(c_puct))
        # self.action_child_dict is a dict
        # act_node[1].get_value will return the action with max Q+u and corresponding board
    
    def Expand(self, action_prob):
        for action, _ in action_prob:
            if action not in self.action_child_dict:
                self.action_child_dict[action] = Node(self, 3 - self.role)
        # Expand all children that under this board
       
    def BackPropagation(self, leaf_value):
        # If it is not root, this node's parent should be updated first.
        if self.parent:
            self.parent.BackPropagation(1.0 - leaf_value)
        self.visit_count += 1
        # there is a simple equation: (v+n*Q)/(n+1) = Q + (v-Q)/(n+1)
        self.Q += (leaf_value - self.Q) / self.visit_count

    def get_total_count(self):
        if self.is_root():
            return self.visit_count
        return self.parent.get_total_count()
    
    def get_value(self, c_puct):
        """Calculate the value of a node.
        
        Args:
            c_puct: a number in (0, inf) controlling the relative impact of
                exploration and exploition
        
        Return: 
            A tuple of (action, next_node), the best action and related node
        """
        total_count = self.get_total_count()
        self.u = c_puct * np.sqrt(2 * np.log(total_count)/self.visit_count)
        return self.Q + self.u

class UCT:
    '''
        An implementation of called Upper Confidence bounds for Tree (UCT).
    '''
    def __init__(self, board, c_puct=5, simulation_times=400):
        self.board = board
        self.root = Node(parent=None, role = 2)
        self.c_puct = c_puct
        self.Simulation_times = simulation_times # times of tree search
        self.direct_dict = {
            'r': [(1, 0), (-1, 0)],
            'c': [(0, 1), (0, -1)],
            'm': [(1, -1), (-1, 1)],
            'v': [(1, 1), (-1, -1)]
        }
        self.count_dict = [[], ddict(lambda:0), ddict(lambda:0)]
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


    def tree_policy(self, board):
        action_probs = np.ones(len(board.availables))/len(board.availables)
        return zip(board.availables, action_probs), 0

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
  
    def nowFree(self, x, y):
        return x >= 0 and y >= 0 and x < pp.width and y < pp.height and self.board[x][y] == 0

    def nowOccupied(self, x, y):
        return self.board[x][y] != 0

    def now_has_neighbor(self, move):
        dist = 1
        x, y = move
        if not self.nowFree(x, y):
            return False
        for i in range(-dist, dist + 1):
            for j in range(-dist, dist + 1):
                if self.nowOccupied(x + i, y + j):
                    return True
        return False

    def get_possible_moves(self):
        move_list = []
        for x in range(pp.width):
            for y in range(pp.height):
                if self.now_has_neighbor((x, y)):
                    move_list.append((x, y))
        return move_list
 
    def Simulation(self, role):
        # node = self.root
        # while True:
        #     if node.is_leaf():
        #         break
        #     move, node = node.Select(self.c_puct)
        #     x, y = move
        #     board[x][y] = node.role
        # node.Expand()
        who = self.is_teriminal()
        if who == "draw":
            return 0.5
        elif who == 1:
            return 1.0
        elif who == 2:
            return 0.0
        else:
            my_max = max(list(self.count_dict[1].items()), key=lambda x: x[1])
            enemy_max = max(list(self.count_dict[2].items()), key=lambda x: x[1])
            if my_max[1] >= 5:
                x, y = my_max[0]
                self.board[x][y] = role
                v = self.Simulation(3 - role)
                self.board[x][y] = 0
            elif enemy_max[1] >= 5:
                x, y = enemy_max[0]
                self.board[x][y] = role
                v = self.Simulation(3 - role)
                self.board[x][y] = 0
            elif my_max[1] == 4:
                x, y = my_max[0]
                self.board[x][y] = role
                v = self.Simulation(3 - role)
                self.board[x][y] = 0
            elif enemy_max[1] == 4:
                x, y = enemy_max[0]
                self.board[x][y] = role
                v = self.Simulation(3 - role)
                self.board[x][y] = 0
            else:
                moves = self.get_possible_moves()
                x, y = moves[random.randint(0, len(moves)-1)] if moves else (8, 6)
                self.board[x][y] = role
                v = self.Simulation(3 - role)
                self.board[x][y] = 0
                return v

    def _evaluate_rollout(self, board, limit=1000):
        '''
            Use the rollout policy to play until the end of the game,
            returning +1 if the current player wins, 0 if the opponent wins,
            and 0.5 if it is a draw.
        '''
        player = board.get_current_player()
        for _ in range(limit):
            winner = self.is_teriminal()
            if not winner:
                break
            action_probs = self.tree_policy(board)
            max_action = max(action_probs, key=itemgetter(1))[0]
            board.do_move(max_action)
        else:
            # If no break from the loop, issue a warning.
            print("WARNING: rollout reached move limit")
        # print('winner is ...',winner)
        if winner == -1:  # tie
            return 0
        else:
            return 1 if winner == player else -1

    def get_move(self):
        '''
            Runs all playouts sequentially and returns the most visited action.
            board: the current game board
            Return: the Selected action
        '''
        moves = self.get_possible_moves()     
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
            for _ in range(self.Simulation_times):
                self.Simulation(role = 2)
            # # return max(self.root.action_dict.items(),
            # #        key=lambda x: x[1].visit_count)[0]
            return moves[random.randint(0, len(moves)-1)] if moves else None


    def update_with_move(self, last_move):
        '''
            Step forward in the tree, keeping everything we already know about the subtree.
        '''
        if last_move in self.root.action_child_dict:
            self.root = self.root.action_child_dict[last_move]
            self.root.parent = None
        else:
            self.root = Node(None, 2)

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
    uct = UCT(cur_board, c_puct=np.sqrt(2), simulation_times=10)
    move = uct.get_move()
    if move:
        best_move = move
    return best_move