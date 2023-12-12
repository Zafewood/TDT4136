# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    
    """ 
    
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        depth = 0
        desiredAction = Directions.STOP
        desiredValue = float('-inf')
        for action in gameState.getLegalActions(0):
            nextValue = self.miniMaxSearch(gameState.generateSuccessor(0, action), 1, depth)
            if nextValue > desiredValue:
                desiredValue = nextValue
                desiredAction = action
        return desiredAction

    """Description of miniMax_search
    Recursive function which is called to check for recursions or evalution:
    Checks for loss and win conditions, True -> Returns evaluationFunction
    Checks for reached specified depth equals depth -> Returns evaluationFunction
    Checks for current agent status, 0 -> Returns max_value
    Else returns min_value
    """
    def miniMaxSearch(self, gameState, agent, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        if agent == 0:
            return self.max_value(gameState, depth)
        else:
          return self.min_value(gameState, agent, depth)    
  
    """Description of min_value
    find min value of all possible actions
    For all ghost agents, the miniMaxSearch is called recursively to find the minimum value in total
    When the last ghost agent (agent == gameState.getNumAgents() - 1) is checked, the depth is increased by 1 and it is pacman's turn
    returns value
    """
    def min_value(self, gameState, agent, depth):
        value = float('inf')
        for action in gameState.getLegalActions(agent):
            nextGameState = gameState.generateSuccessor(agent, action)
            if agent == gameState.getNumAgents() - 1:
                nextValue = self.miniMaxSearch(nextGameState, 0, depth+1)
                if nextValue < value:
                    value = nextValue
            else:
                nextValue = self.miniMaxSearch(nextGameState, agent+1, depth)
                if nextValue < value:
                    value = nextValue
        return value
    
    """Description of max_value
        Find max value of all possible actions
        As the pacman is a single agent, the max_value doesn't need to take in an agent parameter
        For all legal action, the next state is generated and the miniMaxSearch is called recursively to find the maximum value in total
        returns value
    """
    def max_value(self, gameState, depth):
        value = float('-inf')
        for action in gameState.getLegalActions(0):
            nextGameState = gameState.generateSuccessor(0, action)
            nextValue = self.miniMaxSearch(nextGameState, 1, depth)
            if nextValue > value:
                value = nextValue
        return value

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        """
        Pretty much the same as MiniMaxAgent, but with alpha and beta values, which is updated throughout the search in order to prune branches,
        making the search more efficient.
        """

        depth = 0
        desiredAction = Directions.STOP
        desiredValue = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for action in gameState.getLegalActions(0):
            next_value = self.miniMax_search(gameState.generateSuccessor(0, action), 1, depth, alpha, beta)
            if next_value > desiredValue:
                desiredValue = next_value
                desiredAction = action
                alpha = max(desiredValue, alpha)
        return desiredAction
    
    def miniMax_search(self, gameState, agent, depth, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        if agent == 0:
            return self.max_value(gameState, depth, alpha, beta)
        else:
            return self.min_value(gameState, agent, depth, alpha, beta)

    def max_value(self, gameState, depth, alpha, beta):
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        value = float('-inf')
        for action in gameState.getLegalActions(0):
            value = max(value, self.min_value(gameState.generateSuccessor(0, action), 1, depth, alpha, beta))
            if value > beta:
                return value
            alpha = max(alpha, value)
        return value
    
    def min_value(self, gameState, agentIndex, depth, alpha, beta):
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        value = float('inf')
        for action in gameState.getLegalActions(agentIndex):
            if agentIndex == gameState.getNumAgents() - 1:
                nextValue = self.max_value(gameState.generateSuccessor(agentIndex, action), depth+1, alpha, beta)
                if nextValue < value:
                    value = nextValue
            else:
                nextValue = self.min_value(gameState.generateSuccessor(agentIndex, action), agentIndex+1, depth, alpha, beta)
                if nextValue < value:
                    value = nextValue
            if value < alpha:
                return value
            beta = min(beta, value)
        return value

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
