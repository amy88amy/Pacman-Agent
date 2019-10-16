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
        
        

        successorGameState = currentGameState.generatePacmanSuccessor(action)
       
        newPos = successorGameState.getPacmanPosition()
       
        newFood = successorGameState.getFood()
        food=newFood.asList()
       
        dist_far_food=-1
       
      
        for f in food:
            dist=manhattanDistance(newPos,f)
            
            if(dist_far_food>=dist or dist_far_food==-1):
                dist_far_food=dist
      
        dist_ghost=1
        dist_closest_ghost=0
        newGhostStates=successorGameState.getGhostStates()
       

        for ghosts in newGhostStates:
            dist=manhattanDistance(newPos,ghosts.getPosition())
            if(ghosts.scaredTimer):
                dist_closest_ghost+=1
            dist_ghost+=dist
     
        newScaredTimes = [ghostState.scaredTimer for ghostState in successorGameState.getGhostStates()]
        score=successorGameState.getScore()+(1/float(dist_far_food))-(1/float(dist_ghost))-dist_closest_ghost
        "*** YOUR CODE HERE ***"
        return score
        util.raiseNotDefined()

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
        def check(state):
            if(state.isWin() or state.isLose()):
                return True
            else:
                return False
        initial_depth=0
        def max_a(state,d):
            flag=check(state)
            if(flag==True):
                return state.getScore()

            else:
            
                v=float("-inf")
                best_v=v
                best_action="Smile"
                action=state.getLegalActions(0)
                for a in action:
                    v=min_a(state.generateSuccessor(0,a),d,1)
                    if(v>best_v):
                        best_v=v
                        best_action=a
                if(d==0):
                    return best_action
                else:
                    return best_v
        def min_a(state,d,ghost):
            flag=check(state)
            if(flag==True):
                return state.getScore()

            else:
                v=float("inf")
                next_ghost=ghost+1
                best_v=v
            
                action=state.getLegalActions(ghost)
                for a in action:
                    
                    if(next_ghost%state.getNumAgents()==0):
                        if((d+1)!=self.depth):
                            v=max_a(state.generateSuccessor(ghost,a),d+1)
                            
                        else:
                            v=self.evaluationFunction(state.generateSuccessor(ghost,a))
                            
                    else:
                        v=min_a(state.generateSuccessor(ghost,a),d,ghost+1)
                    if(v<best_v):
                        best_v=v
                return best_v
        
        return max_a(gameState, initial_depth)
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def check(state):
            if(state.isWin() or state.isLose()):
                return True
            else:
                return False
        initial_depth=0
        def max_value(state,a,b,d):
            flag=check(state)
            if(flag==True):
                return state.getScore()

            else:
            
                v=float("-inf")
                best_v=v
                best_action="Smile"
                action=state.getLegalActions(0)
                for acc in action:
                    v=min_value(state.generateSuccessor(0,acc),a,b,1,d)
                    if(v>best_v):
                        best_v=v
                        best_action=acc
                    if(a<best_v):
                        a=best_v
                    if(best_v>b):
                        return best_v
                    
                if(d==0):
                    return best_action
                else:
                    return best_v

        def min_value(state,a,b,ghost,d):
            flag=check(state)
            if(flag==True):
                return state.getScore()
            else:
                v=float("inf")
                next_ghost=ghost+1
                best_v=v
                action=state.getLegalActions(ghost)
                for acc in action:
                    if(next_ghost%state.getNumAgents()==0):
                        if((d+1)!=self.depth):
                            v=max_value(state.generateSuccessor(ghost,acc),a,b,d+1)
                            
                        else:
                            v=self.evaluationFunction(state.generateSuccessor(ghost,acc))
                            
                    else:
                        v=min_value(state.generateSuccessor(ghost,acc),a,b,ghost+1,d)
                    if(v<best_v):
                        best_v=v
                    if(b>best_v):
                        b=best_v
                    if(best_v<a):
                        return best_v
                    
                return best_v
    


        return max_value(gameState,float("-inf"),float("inf"), initial_depth)
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
       
        def max_a(state,d):
            if(state.isWin() or state.isLose()):
                return self.evaluationFunction(state)
            v=float("-inf")
            best_v=v
            best_action=Directions.STOP
            action=state.getLegalActions(0)
            for a in action:
                v=min_a(state.generateSuccessor(0,a),d,1)
                if(v>best_v):
                    best_v=v
                    best_action=a
            if(d==0):
                return best_action
            else:
                return best_v

        def min_a(state,d,ghost):
            if(state.isWin() or state.isLose()):
                return self.evaluationFunction(state)
            v=float("inf")
            next_ghost=ghost+1
            best_v=v
           
            action=state.getLegalActions(ghost)
            if(not action):
                return self.evaluationFunction(state)
            prob=1.0/len(action)
           
            for a in action:
                if(next_ghost%state.getNumAgents()==0):
                    if((d+1)==self.depth):
                        v=self.evaluationFunction(state.generateSuccessor(ghost,a))
                        
                    else:
                        v=max_a(state.generateSuccessor(ghost,a),d+1)
                        
                else:
                    v=min_a(state.generateSuccessor(ghost,a),d,next_ghost)
                v=v+v*prob   
            
            return v
        act=max_a(gameState,0)
        print(act)
        return act
        util.raiseNotDefined()
    

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    


# Abbreviation
better = betterEvaluationFunction
