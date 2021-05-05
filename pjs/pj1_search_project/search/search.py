# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class node:
    """self-define node class the same as that in lab_1"""

    def __init__(self, state, parent, path_cost, action):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost
        self.action = action
class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print ("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print ("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    first_node = node(problem.getStartState(), '', 0, [])
    fringe = util.Stack()
    fringe.push(first_node)
    explored = []
    while not fringe.isEmpty():
        item = fringe.pop()
        if problem.isGoalState(item.state):
            return item.action
        if item.state not in explored:
            explored.append(item.state)
            successors = problem.getSuccessors(item.state)
            #a test if it is reversed, total explored will be 246
            #successors.reverse()
            for successor in successors:
                stating = successor[0]
                act = item.action + [successor[1]]
                next_node = node(stating, item, problem.getCostOfActions(act), act)
                fringe.push(next_node)
    return "no solution"

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    first_node = node(problem.getStartState(), '', 0, [])
    fringe = util.Queue()
    fringe.push(first_node)
    explored = []
    while not fringe.isEmpty():
        item = fringe.pop()
        if problem.isGoalState(item.state):
                return item.action
        if item.state not in explored:
            explored.append(item.state)
            successors = problem.getSuccessors(item.state)
            for successor in successors:
                stating = successor[0]
                act = item.action + [successor[1]]
                next_node = node(stating, item, problem.getCostOfActions(act), act)
                if problem.isGoalState(stating):
                    return next_node.action
                fringe.push(next_node)
    return "no solution"
    
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    first_node = node(problem.getStartState(), '', 0, [])
    fringe = util.PriorityQueue()
    fringe.push(first_node, first_node.path_cost)
    explored = []
    while not fringe.isEmpty():
        item = fringe.pop()
        if problem.isGoalState(item.state):
                return item.action
        if item.state not in explored:
            explored.append(item.state)  
            successors = problem.getSuccessors(item.state)
            for successor in successors:
                stating = successor[0]
                act = item.action + [successor[1]]
                next_node = node(stating, item, problem.getCostOfActions(act), act)
                fringe.update(next_node, next_node.path_cost)
    return "no solution"

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    first_state = problem.getStartState()
    first_node = node(first_state, '', heuristic(first_state, problem), [])
    fringe = util.PriorityQueue()
    fringe.push(first_node, first_node.path_cost)
    explored = []
    while not fringe.isEmpty():
        item = fringe.pop()
        if problem.isGoalState(item.state):
                return item.action
        if item.state not in explored:
            explored.append(item.state)  
            successors = problem.getSuccessors(item.state)
            for successor in successors:
                stating = successor[0]
                act = item.action + [successor[1]]
                next_node = node(stating, item, problem.getCostOfActions(act) + 
                                 heuristic(stating, problem), act)
                fringe.update(next_node, next_node.path_cost)
    return "no solution"


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
