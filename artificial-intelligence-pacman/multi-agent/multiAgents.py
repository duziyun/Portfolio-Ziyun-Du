# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
#
# Modified by Eugene Agichtein for CS325 Sp 2014 (eugene@mathcs.emory.edu)
#

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        Note that the successor game state includes updates such as available food,
        e.g., would *not* include the food eaten at the successor state's pacman position
        as that food is no longer remaining.
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood() #food available from successor state (excludes food@successor)
        newCapsules=successorGameState.getCapsules() #capsules available from successor (excludes capsules@successor)
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        from util import manhattanDistance
        capsulecount = len(newCapsules)

        foodlist = newFood.asList()
        food_distances = []
        #the distance to closest food is smaller, pecman gets more score
        if foodlist:
            for food in foodlist:
                food_distances.append(manhattanDistance(food, newPos))
                closest_food_distance = min(food_distances)
        else:
            closest_food_distance = 0

        newfoodcount=len(foodlist)

        if newGhostStates:
            ghostdistances=[]
            for ghost in newGhostStates:
                ghostdistances.append(manhattanDistance(ghost.getPosition(), newPos))
            closest_ghost_distance=min(ghostdistances)

            isscared=False
        #if pecman has eaten power capsule, the score increases and pecman does not need to escape even next move will meet ghost
            if closest_ghost_distance == 0:
                if newScaredTimes:
                    for scared_ghost_distance in newScaredTimes:
                        if scared_ghost_distance > 0:
                            isscared = True
                            closest_ghost_distance = + 5
        #if ghost is not scrared, penman should never move to ghost
                if isscared==False:
                    closest_ghost_distance = -3000
            else:
                closest_ghost_distance = -6 / closest_ghost_distance
        else:
            closest_ghost_distance = 0

        #pecman should try to eat more food and capsule(capsule weights much less than food )
        return  closest_ghost_distance-capsulecount-70*newfoodcount-3*closest_food_distance



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
        """
        "*** YOUR CODE HERE ***"
        #search from depth1 agent0
        return self.minimaxsearch(gameState,1,0)



    def minimaxsearch(self,state,depth,agentindex):
        #if one depth is finished
        if agentindex==state.getNumAgents():
            #if all depth is finished
            if depth == self.depth:
                return self.evaluationFunction(state)
            #start another depth from agent0
            else:
                return self.minimaxsearch(state, depth + 1, 0)

        else:
            legalactions = state.getLegalActions(agentindex)
            successorstates = [state.generateSuccessor(agentindex, action) for action in legalactions]
            nextagent = agentindex + 1

            #recursive function to caculate min or max
            recursiveresults = [self.minimaxsearch(successorstate, depth, nextagent) for successorstate in
                                successorstates]
            #if no susscessor in this search round
            if len(legalactions)==0:
                return self.evaluationFunction(state)

            # return the action of first agent0/pecman
            if agentindex==0 and depth==1:

                best= max(recursiveresults)
                bestindex = [index for index in range(len(recursiveresults)) if recursiveresults[index] == best]
                return legalactions[bestindex[0]]
            #when meet agent0 during seaching in tree
            if agentindex==0:
                best = max(recursiveresults)
            #when meet no-agent0/ghost during seaching in tree
            else:
                best=min(recursiveresults)
            return best



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def alphabeta(self,state, depth, agent, alpha, beta):
        #if minplayer
        if agent > 0:
        #if one depth is finished
            if agent == state.getNumAgents():
                return self.alphabeta(state, depth + 1, 0, alpha, beta)

            val1 = float("inf")
            legalactions1 = state.getLegalActions(agent)
            for action in legalactions1:
                successor = self.alphabeta(state.generateSuccessor(agent, action), depth, agent + 1, alpha, beta)
                val1 = min(val1, successor)
                beta = min(beta, val1)
                #if beta < alpha,pruning
                if beta < alpha:
                    return val1
            #if all depth is finished,return bottom node value
            if len(legalactions1) == 0:
                return self.evaluationFunction(state)

            return val1

        if agent == 0:
            if depth > self.depth:
                return self.evaluationFunction(state)

            val = float("-inf")
            legalactions2 = state.getLegalActions(agent)
            for action in legalactions2:
                successor = self.alphabeta(state.generateSuccessor(agent, action), depth, agent + 1, alpha, beta)
                val = max(val, successor)

                alpha = max(alpha, val)
                if alpha > beta:
                    return val

            if len(legalactions2) == 0:
                return self.evaluationFunction(state)

            return val

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        val, alpha, beta, best = float("-inf"), float("-inf"), float("inf"), None
        for action in gameState.getLegalActions(0):
            val = max(val, self.alphabeta(gameState.generateSuccessor(0, action), 1, 1, alpha, beta))
            if val > alpha:
                best=action
            alpha= max(val, alpha)

        return best


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectimaxsearch(self,state,depth,agentindex):
        #if one depth is finished
        if agentindex==state.getNumAgents():
            #if all depth is finished
            if depth == self.depth:
                return self.evaluationFunction(state)
            #start another depth from agent0
            else:
                return self.expectimaxsearch(state, depth + 1, 0)

        else:
            legalactions = state.getLegalActions(agentindex)
            successorstates = [state.generateSuccessor(agentindex, action) for action in legalactions]
            nextagent = agentindex + 1

            #recursive function to caculate min or max
            recursiveresults = [self.expectimaxsearch(successorstate, depth, nextagent) for successorstate in
                                successorstates]
            #if no susscessor in this search round
            if len(legalactions)==0:
                return self.evaluationFunction(state)

            #return the action of first agent0/pecman
            if agentindex==0 and depth==1:

                best= max(recursiveresults)
                bestindex = [index for index in range(len(recursiveresults)) if recursiveresults[index] == best]
                return legalactions[bestindex[0]]
            #when meet agent0 during seaching in tree
            if agentindex==0:
                best = max(recursiveresults)
            #calculate average cost of ghost
            else:
                best=sum(recursiveresults)/len(recursiveresults)
            return best

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectimaxsearch(gameState, 1, 0)


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: please read my below comment
    """
    "*** YOUR CODE HERE ***"
    from util import manhattanDistance

    position = currentGameState.getPacmanPosition()
    foodlist = currentGameState.getFood().asList()
    ghoststates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    ScaredTimes = [ghostState.scaredTimer for ghostState in ghoststates]

    #choose action which will shorten distance to closest food
    if foodlist:
        food_distances = [manhattanDistance(food, position)
                          for food in foodlist]
        closest_food_distance = 1 / min(food_distances)
    else:
        closest_food_distance = 0

    #try to reduce count of food and capsule
    foodcount = len(foodlist)
    capsulescount = len(capsules)

    #try to get away from ghost
    if ghoststates:
        ghost_distances = [manhattanDistance(ghost.getPosition(), position)
                           for ghost in ghoststates]
        closest_ghost_distance = min(ghost_distances)

    #if ghost is scared, no need to escape
        isscared = False
        if closest_ghost_distance == 0:
            if ScaredTimes:
                for scared_ghost_distance in ScaredTimes:
                    if scared_ghost_distance > 0:
                        isscared = True
                        closest_ghost_distance = + 22
            if isscared == False:
                closest_ghost_distance = -9999
        else:
            closest_ghost_distance = -1 / closest_ghost_distance
    else:
        closest_ghost_distance = 0

    #try to be closer to capsules
    if capsules:
        capsule_distances = [manhattanDistance(capsule, position)
                             for capsule in capsules]
        closest_capsule_distance = 1 / min(capsule_distances)
    else:
        closest_capsule_distance = 0

    score = 5 * closest_food_distance + 7 * closest_ghost_distance + 12 * closest_capsule_distance - 70 * foodcount - 150 * capsulescount
    return score



# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

