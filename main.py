from queue import PriorityQueue
from random import shuffle
from re import template
from time import time

global expandedNodes
expandedNodes = set()

global emptyNum
emptyNum = 9

global timeCount
timeCount = 0

global timeExpand
timeExpand = 0

global timeSetAdd
timeSetAdd=0
class Node:

    def __init__(self, status, cost):
        self.status = status
        self.cost = cost
        self.parent = None

    # def __getitem__(self, i):
    #     return self.status[i]

    def __lt__(self, other):
        return self.cost < other.cost

    def __str__(self) -> str:
        return "Node:\n" + str(self.status[0:3]) + '\n'+str(self.status[3:6]) + '\n'+str(self.status[6:9])+"\nCost: " + str(self.cost)

    def setParent(self, parent):
        self.parent = parent

    def swap(self, i1, j1, i2, j2):
        self.status[(i1-1)*3+j1-1], self.status[(i2-1)*3+j2 -
                                                1] = self.status[(i2-1)*3+j2-1], self.status[(i1-1)*3+j1-1]


def twoToOne(matrix):
    # transform the matrix to one-dimensional list with deletion of boundary 0
    # oneDimensionalList = [matrix[i][j] for i in range(5)
    #                       for j in range(5)
    #                       if matrix[i][j] != 0]
    oneDimensionalList=matrix[1][1:4]+matrix[2][1:4]+matrix[3][1:4]
    
    return oneDimensionalList


def oneToTwo(list):
    # transform the list to two-dimensional list with boundary 0
    twoDimensionalList =[[0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0],
                         [0,0,0,0,0]]
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


def heuristic(status):
    # todo: write a heuristic function here, return a value

    return manhattanDistance(status)
    pass


def evaluateNode(node):
    # todo: return a value towards the goal
    # add current cost and heuristic cost
    return node.cost+heuristic(node.status)


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

    global timeExpand
    timeExpand += time()-start
    return nodes


def search(list):
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
        
        start=time()
        expandedNodes.add(tuple(node.status))
        global timeSetAdd
        timeSetAdd+=time()-start
        # print(node)

        if node.status == goal:
            print("Generated nodes:", generationCount)
            print("Expanded nodes:", expandCount)
            return node
        
        for nextNode in expandNode(node):
            # if was expanded before, skip
            start = time()
            if tuple(nextNode.status) not in expandedNodes:
                expandCount += 1
                pq.put((evaluateNode(nextNode), nextNode))
                
            global timeCount
            timeCount += time()-start

    print("Generated nodes:", generationCount)
    print("Expanded nodes:", expandCount)
    print("There is no solution")


def judgeSolution(l):
    sum = 0
    tempList=l.copy()
    del tempList[tempList.index(9)]
    for i in range(len(tempList)):
        for j in range(i):
            if tempList[i] < tempList[j]:
                sum += 1

    #l[l.index(0)] = 9
    if sum % 2 == 0:
        return True
    else:
        return False


def printPath(node):
    print("Path to goal:")
    while node.parent != None:
        print(node)
        node = node.parent
    print(node)

timestart=time()
goal = [i for i in range(1, 10)]    # create a list of numbers from 1 to 9
# [1,2,3,4,5,6,7,8,9]
randomList = goal.copy()
shuffle(randomList)                     # shuffle the list randomly
expandedNodes = set()
# expandedNodes.add(tuple(randomList))
#randomList=[9, 1, 3, 6, 7, 2, 4, 8, 5]
#randomList=[4,1,2,5,8,3,7,9,6]
#randomList = [2, 7, 6, 4, 5, 1, 3, 8, 9]
print("Start:", randomList)
if judgeSolution(randomList) != judgeSolution(goal):
    print("The initial list is not solvable.")
    exit()
    

print(manhattanDistance(randomList))
node=search(randomList)

#printPath(node)

# printPath(goal)

print(randomList, goal)
timeTotal=time()-timestart
print("timecount:", timeCount)
print("timeexpand:", timeExpand)
print("timesetadd:", timeSetAdd) 
print("total time used:",timeTotal)