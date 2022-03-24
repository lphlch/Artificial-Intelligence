from queue import PriorityQueue
from random import shuffle
from time import time
from cmath import sqrt
import numpy as np

from tree import TreeCreator

global expandedNodes
expandedNodes = set()
global emptyNum
emptyNum = 9
global tree
tree=TreeCreator()
global goal
goal = [i for i in range(1, 10)]
class Node:

    def __init__(self, status:list, cost:float) -> None:
        """initialize a node

        Args:
            status (list): status of the node
            cost (float): current cost of the node
        """        
        self.status = status
        self.cost = cost
        self.parent = None

    def __lt__(self, other):
        """override the < operator, used for priority queue
        """
        return self.cost < other.cost

    def __str__(self) -> str:
        """override the str function, used for print
        """
        return "Node:\n" + str(self.status[0:3]) + '\n'+str(self.status[3:6]) + '\n'+str(self.status[6:9])+"\nCost: " + str(self.cost)

    def setParent(self, parent) -> None:
        """set the parent of the node

        Args:
            parent (Node): parent of the node
        """
        self.parent = parent

    def swap(self, i1:int, j1:int, i2:int, j2:int) -> None:
        """swap two elements in the status

        Args:
            i1 (int): index x of the first element
            j1 (int): index y of the first element
            i2 (int): index x of the second element
            j2 (int): index y of the second element
        """
        self.status[(i1-1)*3+j1-1], self.status[(i2-1)*3+j2 -
                                                1] = self.status[(i2-1)*3+j2-1], self.status[(i1-1)*3+j1-1]


def twoToOne(matrix:list)->list:
    """transform the two-dimensional list to one-dimensional list

    Args:
        matrix (list): list of list

    Returns:
        list: plain list
    """
    # transform the matrix to one-dimensional list with deletion of boundary 0
    # // time costly
    # // oneDimensionalList = [matrix[i][j] for i in range(5)
    # //                       for j in range(5)
    # //                       if matrix[i][j] != 0]
    oneDimensionalList = matrix[1][1:4]+matrix[2][1:4]+matrix[3][1:4]

    return oneDimensionalList


def oneToTwo(list:list)->list:
    """transform the one-dimensional list to two-dimensional list

    Args:
        list (list): plain list

    Returns:
        list: two-dimensional list
    """
    # transform the list to two-dimensional list with boundary 0
    twoDimensionalList = [[0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0]]
    twoDimensionalList[1][1:4] = list[0:3]
    twoDimensionalList[2][1:4] = list[3:6]
    twoDimensionalList[3][1:4] = list[6:9]
    return twoDimensionalList


def manhattanDistance(status):
    dis = 0
    for i in range(0, 9):
        if status[i] != 0 and status[i] != 9:
            dis += abs(i//3-(status[i]-1)//3)
            dis += abs(i % 3-(status[i]-1) % 3)
    return dis


def euclideanDistance(status):
    dis = 0
    for i in range(0, 9):
        if status[i] != 0 and status[i] != 9:
            dis += sqrt((i//3-(status[i]-1)//3)**2 +
                        (i % 3-(status[i]-1) % 3)**2).real
    return dis


def cosineDistance(status):
    cos = np.dot(status, goal) / \
        (np.linalg.norm(status)*(np.linalg.norm(goal)))
    return (1-cos)*50


def heuristic(status, function):
    return function(status)


def evaluateNode(node,function):
    # add current cost and heuristic cost
    return node.cost+heuristic(node.status, function)


def expandNode(node):
    # these child nodes should be set parent to the current node

    start = time()

    # temporary transform the list to two-dimensional list, with boundary 0
    twoDimensionalList = oneToTwo(node.status)

    emptyPosition = (0, 0)
    # search for next exchangable status
    nodes = []

    # find empty position
    for i in range(5):
        for j in range(5):
            if twoDimensionalList[i][j] == emptyNum:
                emptyPosition = (i, j)

    # up
    if twoDimensionalList[emptyPosition[0]-1][emptyPosition[1]] != 0:
        newNode = Node(twoToOne(twoDimensionalList), node.cost+1)
        newNode.swap(emptyPosition[0], emptyPosition[1],
                     emptyPosition[0]-1, emptyPosition[1])
        newNode.setParent(node)
        nodes.append(newNode)

    # down
    if twoDimensionalList[emptyPosition[0]+1][emptyPosition[1]] != 0:
        newNode = Node(twoToOne(twoDimensionalList), node.cost+1)
        newNode.swap(emptyPosition[0], emptyPosition[1],
                     emptyPosition[0]+1, emptyPosition[1])
        newNode.setParent(node)
        nodes.append(newNode)

    # left
    if twoDimensionalList[emptyPosition[0]][emptyPosition[1]-1] != 0:
        newNode = Node(twoToOne(twoDimensionalList), node.cost+1)
        newNode.swap(emptyPosition[0], emptyPosition[1],
                     emptyPosition[0], emptyPosition[1]-1)
        newNode.setParent(node)
        nodes.append(newNode)

    # right
    if twoDimensionalList[emptyPosition[0]][emptyPosition[1]+1] != 0:
        newNode = Node(twoToOne(twoDimensionalList), node.cost+1)
        newNode.swap(emptyPosition[0], emptyPosition[1],
                     emptyPosition[0], emptyPosition[1]+1)
        newNode.setParent(node)
        nodes.append(newNode)

    return nodes


def search(list, function, isTreeNeed):
    startList = Node(list, 0)
    generationCount = 0
    expandCount = 0

    # search for solution
    pq = PriorityQueue()
    # priority queue stores nodes as a list of [priority, node]
    pq.put((0, startList))

    while not pq.empty():
        node = pq.get()[1]
        generationCount += 1

        expandedNodes.add(tuple(node.status))
        # print(node)

        if node.status == goal:
            print("Generated nodes:", generationCount)
            print("Expanded nodes:", expandCount)
            return generationCount, expandCount ,node

        for nextNode in expandNode(node):
            # if was expanded before, skip
            start = time()
            if tuple(nextNode.status) not in expandedNodes:
                expandCount += 1
                
                if isTreeNeed:
                    # add the node to graph
                    tree.addNode(nextNode.status)
                    tree.setParent(nextNode.parent.status, nextNode.status)
                
                pq.put((evaluateNode(nextNode,function), nextNode))


    print("Generated nodes:", generationCount)
    print("Expanded nodes:", expandCount)
    print("There is no solution")
    

def judgeSolution(l):
    sum = 0
    tempList = l.copy()
    del tempList[tempList.index(9)]
    for i in range(len(tempList)):
        for j in range(i):
            if tempList[i] < tempList[j]:
                sum += 1

    if sum % 2 == 0:
        return True
    else:
        return False


def pathGetting(node):
    path=[]
    #print("Path to goal:")
    while node.parent != None:
        #print(node)
        path.insert(0,node.status)
        node = node.parent
    print(node)
    return path

def clear():
    for object in expandedNodes:
        del object
    expandedNodes.clear()
    
    
    
def solve(isTreeNeed,function):
    clear()
    timestart = time()
    strFunctions=function.split()
    #! use eval function to transform the string to function name
    function=eval(strFunctions[0].lower()+strFunctions[1])
    
    randomList = goal.copy()
    shuffle(randomList)                     # shuffle the list randomly
    
    #! expandedNodes.add(tuple(randomList)) can not add!
    isSolvable=True
    
    if isTreeNeed:
        randomList=[4,1,2,5,8,3,7,9,6]  # small tree
        
    #randomList = [5, 9, 4, 2, 7, 6, 1, 8, 3] # 5093
    print("Start:", randomList)
    if judgeSolution(randomList) != judgeSolution(goal):
        print("The initial list is not solvable.")
        isSolvable=False
        path=[randomList]
        #! worng!
        #//path=randomList
        generationCount=expandCount=timeTotal=None

    if isSolvable:
        #function = manhattanDistance  # heuristic function

        print(function(randomList))
        generationCount,expandCount,node = search(randomList, function,isTreeNeed)

        path=pathGetting(node)
        print(path)
        #pathGetting(goal)

        print(randomList, goal)
        timeTotal = time()-timestart
        print("total time used:", timeTotal)

    if isTreeNeed:
        tree.highlightSolutionPath(node)
        tree.create()
        
    return {'path':path, 'time':timeTotal, 'isSolvable':isSolvable,'generationCount':generationCount, 'expandCount':expandCount,'time':timeTotal}