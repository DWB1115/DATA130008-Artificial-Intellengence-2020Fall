import heapq
import sys


class PriorityQueue:

    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)


class node:
    """define node"""

    def __init__(self, state, parent, path_cost, action,):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost
        self.action = action


class problem:
    """searching problem"""

    def __init__(self, initial_state, actions):
        self.initial_state = initial_state
        self.actions = actions

    def search_actions(self, state):
        """Search actions for the given state.
        Args:
            state: a string e.g. 'A'

        Returns:
            a list of action string list
            e.g. [['A', 'B', '2'], ['A', 'C', '3']]
        """
        ################################# Your code here ###########################
        act_list = []
        for action in self.actions:
            if action[0] == state:
                act_list.append(action)
        return act_list

    def solution(self, node):
        """Find th path from the beginning to the given node.

        Args:
            node: the node class defined above.

        Returns:
            ['Start', 'A', 'B', ....]
        """
        ################################# Your code here ###########################
        ing = node
        sol_list = []
        while ing.state != 'Start':
            sol_list.append(ing.state)
            ing = ing.parent
        sol_list.append('Start')

        return sol_list.reverse

    def transition(self, state, action):
        """Find the next state from the state adopting the given action.

        Args:
            state: 'A'
            action: ['A', 'B', '2']

        Returns:
            string, representing the next state, e.g. 'B'
        """
        ################################# Your code here ###########################
        return action[1]

    def goal_test(self, state):
        """Test if the state is goal

        Args:
            state: string, e.g. 'Goal' or 'A'

        Returns:
            a bool (True or False)
        """

        ################################# Your code here ###########################
        return state == 'Goal'

    def step_cost(self, state1, action, state2):
        if (state1 == action[0]) and (state2 == action[1]):
            return int(action[2])
        else:
            print("Step error!")
            sys.exit()

    def child_node(self, node_begin, action):
        """Find the child node from the node adopting the given action

        Args:
            node_begin: the node class defined above.
            action: ['A', 'B', '2']

        Returns:
            a node as defined above
        """
        ################################# Your code here ###########################
        return node(state=action[1], parent=node_begin, path_cost=int(action[2]) + node_begin.path_cost, action = node_begin.action + [action[1]])


def UCS(problem):
    """Using Uniform Cost Search to find a solution for the problem.

    Args:
        problem: problem class defined above.

    Returns:
        a list of strings representing the path.
            e.g. ['A', 'B', '2']
        if the path does not exist, return 'Unreachable'
    """
    node_test = node(problem.initial_state, '', 0, ['Start'])
    frontier = PriorityQueue()
    frontier.push(node_test, node_test.path_cost)
    state2node = {node_test.state: node_test}
    explored = []

    ################################# Your code here ###########################
    while not frontier.isEmpty():
        item = frontier.pop()
        explored.append(item.state)
        if item.state == 'Goal':
            return item.action
        state2node[item.state] = item
        item_actions = problem.search_actions(item.state)
        for action in item_actions:
            next_node = problem.child_node(item, action)
            if next_node.state not in explored:
                c = node(next_node.state, item, item.path_cost + int(action[2]), item.action + [next_node.state])
                frontier.update(c, c.path_cost)
                
    return 'Unreachable'

if __name__ == '__main__':
    Actions = []
    while True:
        a = input().strip()
        if a != 'END':
            a = a.split()
            Actions += [a]
        else:
            break
    graph_problem = problem('Start', Actions)
    answer = UCS(graph_problem)
    s = "->"
    if answer == 'Unreachable':
        print(answer)
    else:
        path = s.join(answer)
        print(path)
