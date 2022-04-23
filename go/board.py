from cmath import inf
from heapq import heappush, heappop
# from copy import deepcopy

from time import time

BLACK = 'X'
WHITE = '@'
EMPTY = 'O'  # not zero 0
MAXSIZE = 15

EASY = 0.5
NORMAL = 1
HARD = 2
MASTER = 3
# MAXDEPTH=level*2
# MAXGREEDY=level*10

global Searched
Searched = 0

global Scored
Scored = 0


def deepcopy(s):
    #! this deepcopy unfold will reduce 80% time cost
    new = []
    new = [[s[0][0], s[0][1], s[0][2], s[0][3], s[0][4], s[0][5], s[0][6], s[0][7], s[0][8], s[0][9], s[0][10], s[0][11], s[0][12], s[0][13], s[0][14]],
           [s[1][0], s[1][1], s[1][2], s[1][3], s[1][4], s[1][5], s[1][6], s[1][7],
            s[1][8], s[1][9], s[1][10], s[1][11], s[1][12], s[1][13], s[1][14]],
           [s[2][0], s[2][1], s[2][2], s[2][3], s[2][4], s[2][5], s[2][6], s[2][7],
            s[2][8], s[2][9], s[2][10], s[2][11], s[2][12], s[2][13], s[2][14]],
           [s[3][0], s[3][1], s[3][2], s[3][3], s[3][4], s[3][5], s[3][6], s[3][7],
               s[3][8], s[3][9], s[3][10], s[3][11], s[3][12], s[3][13], s[3][14]],
           [s[4][0], s[4][1], s[4][2], s[4][3], s[4][4], s[4][5], s[4][6], s[4][7],
            s[4][8], s[4][9], s[4][10], s[4][11], s[4][12], s[4][13], s[4][14]],
           [s[5][0], s[5][1], s[5][2], s[5][3], s[5][4], s[5][5], s[5][6], s[5][7],
            s[5][8], s[5][9], s[5][10], s[5][11], s[5][12], s[5][13], s[5][14]],
           [s[6][0], s[6][1], s[6][2], s[6][3], s[6][4], s[6][5], s[6][6], s[6][7],
            s[6][8], s[6][9], s[6][10], s[6][11], s[6][12], s[6][13], s[6][14]],
           [s[7][0], s[7][1], s[7][2], s[7][3], s[7][4], s[7][5], s[7][6], s[7][7],
            s[7][8], s[7][9], s[7][10], s[7][11], s[7][12], s[7][13], s[7][14]],
           [s[8][0], s[8][1], s[8][2], s[8][3], s[8][4], s[8][5], s[8][6], s[8][7],
            s[8][8], s[8][9], s[8][10], s[8][11], s[8][12], s[8][13], s[8][14]],
           [s[9][0], s[9][1], s[9][2], s[9][3], s[9][4], s[9][5], s[9][6], s[9][7],
            s[9][8], s[9][9], s[9][10], s[9][11], s[9][12], s[9][13], s[9][14]],
           [s[10][0], s[10][1], s[10][2], s[10][3], s[10][4], s[10][5], s[10][6], s[10][7],
            s[10][8], s[10][9], s[10][10], s[10][11], s[10][12], s[10][13], s[10][14]],
           [s[11][0], s[11][1], s[11][2], s[11][3], s[11][4], s[11][5], s[11][6], s[11][7],
            s[11][8], s[11][9], s[11][10], s[11][11], s[11][12], s[11][13], s[11][14]],
           [s[12][0], s[12][1], s[12][2], s[12][3], s[12][4], s[12][5], s[12][6], s[12][7],
            s[12][8], s[12][9], s[12][10], s[12][11], s[12][12], s[12][13], s[12][14]],
           [s[13][0], s[13][1], s[13][2], s[13][3], s[13][4], s[13][5], s[13][6], s[13][7],
            s[13][8], s[13][9], s[13][10], s[13][11], s[13][12], s[13][13], s[13][14]],
           [s[14][0], s[14][1], s[14][2], s[14][3], s[14][4], s[14][5], s[14][6], s[14][7],
            s[14][8], s[14][9], s[14][10], s[14][11], s[14][12], s[14][13], s[14][14]]
           ]
    # for i in range(15):
    #     t=[s[i][0],s[i][1],s[i][2],s[i][3],s[i][4],s[i][5],s[i][6],s[i][7],s[i][8],s[i][9],s[i][10],s[i][11],s[i][12],s[i][13],s[i][14]]
    #     new.append(t)

    return new


def getValidPieces(lines, flag):
    """partion lines to valid pieces by opponent chess

    Args:
        lines (list[str]): list of lines of string
        flag (str): BLACK or WHITE

    Returns:
        list[str]: list of valid string pieces
    """
    opponentFlag = BLACK if flag == WHITE else WHITE
    validLines = []
    for line in lines:
        # ignore the line which only have one chess of mine
        if line.count(flag) <= 1:
            continue

        validLines += line.split(opponentFlag)

    #! validLines may include empty or just one chess of mine.
    #! NO needs to delete them, due to waste time.
    #! let them be processed in the regular matching process.
    # print((validLines))
    return validLines


def getScore(validLines, level):
    global Scored
    Scored += 1
    # matching
    S2, L2, S3, L3, S4, L4, L5 = 0, 1, 2, 3, 4, 5, 6
    weight = [5, 20, 30, 100, 1000, 5000, 100000]
    # LX: X continuous
    # SX: X continuous with one direction blocked
    count = [0]*7
    for validLine in validLines:
        # let chess be the same, make code shorter
        replacedValidLine = validLine.replace('@', 'X')
        if -1 != replacedValidLine.find('XXXXX'):
            count[L5] += 1
        elif -1 != replacedValidLine.find('OXXXXO'):
            count[L4] += 1
        elif -1 != replacedValidLine.find('XOXXXOX'):
            count[L4] += 1
        elif -1 != replacedValidLine.find('XXOXXOXX'):
            count[L4] += 1
        elif replacedValidLine.startswith('XXXXO'):
            count[S4] += 1
        elif replacedValidLine.endswith('OXXXX'):
            count[S4] += 1
        elif -1 != replacedValidLine.find('XOXXX'):
            count[S4] += 1
        elif -1 != replacedValidLine.find('XXXOX'):
            count[S4] += 1
        elif -1 != replacedValidLine.find('XXOXX'):
            count[S4] += 1
        elif -1 != replacedValidLine.find('OOXXXO'):
            count[L3] += 1
        elif -1 != replacedValidLine.find('OXXXOO'):
            count[L3] += 1
        elif -1 != replacedValidLine.find('OXXOXO'):
            count[L3] += 1
        elif -1 != replacedValidLine.find('OXOXXO'):
            count[L3] += 1
        elif -1 != replacedValidLine.find('XOXOXOX'):
            count[L3] += 1

        elif level >= NORMAL:

            if replacedValidLine == 'OXXXO$':
                count[S3] += 1
            elif replacedValidLine.startswith('XXXOO'):
                count[S3] += 1
            elif replacedValidLine.endswith('OOXXX'):
                count[S3] += 1
            elif replacedValidLine.startswith('XXOXO'):
                count[S3] += 1
            elif replacedValidLine.endswith('OXOXX'):
                count[S3] += 1
            elif replacedValidLine.startswith('XOXXO'):
                count[S3] += 1
            elif replacedValidLine.endswith('OXXOX'):
                count[S3] += 1
            elif -1 != replacedValidLine.find('XOOXXOOX'):
                count[S3] += 2
            elif -1 != replacedValidLine.find('XOOXX'):
                count[S3] += 1
            elif -1 != replacedValidLine.find('XXOOX'):
                count[S3] += 1
            elif -1 != replacedValidLine.find('XOXOX'):
                count[S3] += 1

            elif level >= HARD:

                if -1 != replacedValidLine.find('OOXXOO'):
                    count[L2] += 1
                elif -1 != replacedValidLine.find('OXOXOO'):
                    count[L2] += 1
                elif -1 != replacedValidLine.find('OOXOXO'):
                    count[L2] += 1
                elif -1 != replacedValidLine.find('OXOOXO'):
                    count[L2] += 1

                elif level >= MASTER:

                    if -1 != replacedValidLine.find('XOOOX'):
                        count[S2] += 1
                    elif replacedValidLine.startswith('XOOXO'):
                        count[S2] += 1
                    elif replacedValidLine.endswith('OXOOX'):
                        count[S2] += 1
                    elif replacedValidLine.startswith('XOXOO'):
                        count[S2] += 1
                    elif replacedValidLine.endswith('OOXOX'):
                        count[S2] += 1
                    if replacedValidLine.startswith('XXOOO'):
                        count[S2] += 1
                    elif replacedValidLine == 'OXXOO':
                        count[S2] += 1
                    elif replacedValidLine == 'OOXXO':
                        count[S2] += 1
                    elif replacedValidLine.endswith('OOOXX'):
                        count[S2] += 1
    score = 0
    for i in range(len(count)):
        score += count[i]*weight[i]

    # print(count,score)
    return score


def getValidSteps(status, centre: tuple, flag, level):
    validSteps = []

    validPos = [[0]*MAXSIZE for _ in range(MAXSIZE)]
    for x in range(MAXSIZE):
        for y in range(MAXSIZE):
            if status[x][y] != EMPTY:
                for k1 in range(-3, 4):
                    for k2 in range(-3, 4):
                        if 0 < x+k1 < MAXSIZE and 0 < y+k2 < MAXSIZE and status[x+k1][y+k2] == EMPTY:
                            validPos[x+k1][y+k2] = 1

    for x in range(MAXSIZE):
        for y in range(MAXSIZE):
            if validPos[x][y] == 1:
                validSteps.append((x, y))

    # centreX,centreY=centre  # only search around centre step 3
    # for x in range(centreX-5,centreX+6):
    #     if x<0 or x>MAXSIZE-1:
    #         continue
    #     for y in range(centreY-5,centreY+6):
    #         if y<0 or y>MAXSIZE-1:
    #             continue

    #         if status[x][y]==EMPTY:
    #             validSteps.append((x,y))

    # print("validSteps:",len(validSteps))

    greedyList = []
    for step in validSteps:
        greedyStatus = deepcopy(status)
        greedyStatus[step[0]][step[1]] = flag
        greedyBoard = board(greedyStatus, curStepPos=step, level=level)

        blackLines = getValidPieces(greedyBoard.getAllLines(), BLACK)
        bs = getScore(blackLines, level)
        whiteLines = getValidPieces(greedyBoard.getAllLines(), WHITE)
        ws = getScore(whiteLines, level)

        greedyScore = ws-bs
        heappush(greedyList, (-greedyScore, step))

    searchList = []
    count = 0
    while greedyList:
        if count == level*10:   # MAXGREEDY=level*10
            break
        searchList.append(heappop(greedyList)[1])
        count += 1

    return searchList


def getLine(status):
    l = []
    for line in status:
        l.append(''.join(line))    # make a string
    return l


def getColumn(s):
    l = []
    l.append(''.join([s[0][0], s[1][0], s[2][0], s[3][0], s[4][0], s[5][0], s[6][0],
             s[7][0], s[8][0], s[9][0], s[10][0], s[11][0], s[12][0], s[13][0], s[14][0]]))
    l.append(''.join([s[0][1], s[1][1], s[2][1], s[3][1], s[4][1], s[5][1], s[6][1],
             s[7][1], s[8][1], s[9][1], s[10][1], s[11][1], s[12][1], s[13][1], s[14][1]]))
    l.append(''.join([s[0][2], s[1][2], s[2][2], s[3][2], s[4][2], s[5][2], s[6][2],
             s[7][2], s[8][2], s[9][2], s[10][2], s[11][2], s[12][2], s[13][2], s[14][2]]))
    l.append(''.join([s[0][3], s[1][3], s[2][3], s[3][3], s[4][3], s[5][3], s[6][3],
             s[7][3], s[8][3], s[9][3], s[10][3], s[11][3], s[12][3], s[13][3], s[14][3]]))
    l.append(''.join([s[0][4], s[1][4], s[2][4], s[3][4], s[4][4], s[5][4], s[6][4],
             s[7][4], s[8][4], s[9][4], s[10][4], s[11][4], s[12][4], s[13][4], s[14][4]]))
    l.append(''.join([s[0][5], s[1][5], s[2][5], s[3][5], s[4][5], s[5][5], s[6][5],
             s[7][5], s[8][5], s[9][5], s[10][5], s[11][5], s[12][5], s[13][5], s[14][5]]))
    l.append(''.join([s[0][6], s[1][6], s[2][6], s[3][6], s[4][6], s[5][6], s[6][6],
             s[7][6], s[8][6], s[9][6], s[10][6], s[11][6], s[12][6], s[13][6], s[14][6]]))
    l.append(''.join([s[0][7], s[1][7], s[2][7], s[3][7], s[4][7], s[5][7], s[6][7],
             s[7][7], s[8][7], s[9][7], s[10][7], s[11][7], s[12][7], s[13][7], s[14][7]]))
    l.append(''.join([s[0][8], s[1][8], s[2][8], s[3][8], s[4][8], s[5][8], s[6][8],
             s[7][8], s[8][8], s[9][8], s[10][8], s[11][8], s[12][8], s[13][8], s[14][8]]))
    l.append(''.join([s[0][9], s[1][9], s[2][9], s[3][9], s[4][9], s[5][9], s[6][9],
             s[7][9], s[8][9], s[9][9], s[10][9], s[11][9], s[12][9], s[13][9], s[14][9]]))
    l.append(''.join([s[0][10], s[1][10], s[2][10], s[3][10], s[4][10], s[5][10], s[6][10],
             s[7][10], s[8][10], s[9][10], s[10][10], s[11][10], s[12][10], s[13][10], s[14][10]]))
    l.append(''.join([s[0][11], s[1][11], s[2][11], s[3][11], s[4][11], s[5][11], s[6][11],
             s[7][11], s[8][11], s[9][11], s[10][11], s[11][11], s[12][11], s[13][11], s[14][11]]))
    l.append(''.join([s[0][12], s[1][12], s[2][12], s[3][12], s[4][12], s[5][12], s[6][12],
             s[7][12], s[8][12], s[9][12], s[10][12], s[11][12], s[12][12], s[13][12], s[14][12]]))
    l.append(''.join([s[0][13], s[1][13], s[2][13], s[3][13], s[4][13], s[5][13], s[6][13],
             s[7][13], s[8][13], s[9][13], s[10][13], s[11][13], s[12][13], s[13][13], s[14][13]]))
    l.append(''.join([s[0][14], s[1][14], s[2][14], s[3][14], s[4][14], s[5][14], s[6][14],
             s[7][14], s[8][14], s[9][14], s[10][14], s[11][14], s[12][14], s[13][14], s[14][14]]))

    # for column in range(MAXSIZE):
    #     temp = []
    #     for line in range(MAXSIZE):
    #         temp.append(s[line][column])
    #     l.append(''.join(temp))
    return l


def getDiagonal1(s):
    l = []
    #! this for loop unfold can save 20% time
    l.append(''.join([s[0][10], s[1][11], s[2][12], s[3][13], s[4][14]]))
    l.append(
        ''.join([s[0][9], s[1][10], s[2][11], s[3][12], s[4][13], s[5][14]]))
    l.append(''.join([s[0][8], s[1][9], s[2][10], s[3]
             [11], s[4][12], s[5][13], s[6][14]]))
    l.append(''.join([s[0][7], s[1][8], s[2][9], s[3][10],
             s[4][11], s[5][12], s[6][13], s[7][14]]))
    l.append(''.join([s[0][6], s[1][7], s[2][8], s[3][9], s[4]
             [10], s[5][11], s[6][12], s[7][13], s[8][14]]))
    l.append(''.join([s[0][5], s[1][6], s[2][7], s[3][8], s[4]
             [9], s[5][10], s[6][11], s[7][12], s[8][13], s[9][14]]))
    l.append(''.join([s[0][4], s[1][5], s[2][6], s[3][7], s[4][8],
             s[5][9], s[6][10], s[7][11], s[8][12], s[9][13], s[10][14]]))
    l.append(''.join([s[0][3], s[1][4], s[2][5], s[3][6], s[4][7], s[5]
             [8], s[6][9], s[7][10], s[8][11], s[9][12], s[10][13], s[11][14]]))
    l.append(''.join([s[0][2], s[1][3], s[2][4], s[3][5], s[4][6], s[5][7],
             s[6][8], s[7][9], s[8][10], s[9][11], s[10][12], s[11][13], s[12][14]]))
    l.append(''.join([s[0][1], s[1][2], s[2][3], s[3][4], s[4][5], s[5][6], s[6][7],
             s[7][8], s[8][9], s[9][10], s[10][11], s[11][12], s[12][13], s[13][14]]))
    l.append(''.join([s[0][0], s[1][1], s[2][2], s[3][3], s[4][4], s[5][5], s[6][6], s[7]
             [7], s[8][8], s[9][9], s[10][10], s[11][11], s[12][12], s[13][13], s[14][14]]))
    l.append(''.join([s[1][0], s[2][1], s[3][2], s[4][3], s[5][4], s[6][5], s[7][6],
             s[8][7], s[9][8], s[10][9], s[11][10], s[12][11], s[13][12], s[14][13]]))
    l.append(''.join([s[2][0], s[3][1], s[4][2], s[5][3], s[6][4], s[7][5],
             s[8][6], s[9][7], s[10][8], s[11][9], s[12][10], s[13][11], s[14][12]]))
    l.append(''.join([s[3][0], s[4][1], s[5][2], s[6][3], s[7][4], s[8]
             [5], s[9][6], s[10][7], s[11][8], s[12][9], s[13][10], s[14][11]]))
    l.append(''.join([s[4][0], s[5][1], s[6][2], s[7][3], s[8][4],
             s[9][5], s[10][6], s[11][7], s[12][8], s[13][9], s[14][10]]))
    l.append(''.join([s[5][0], s[6][1], s[7][2], s[8][3], s[9]
             [4], s[10][5], s[11][6], s[12][7], s[13][8], s[14][9]]))
    l.append(''.join([s[6][0], s[7][1], s[8][2], s[9][3],
             s[10][4], s[11][5], s[12][6], s[13][7], s[14][8]]))
    l.append(''.join([s[7][0], s[8][1], s[9][2], s[10][3],
             s[11][4], s[12][5], s[13][6], s[14][7]]))
    l.append(''.join([s[8][0], s[9][1], s[10][2],
             s[11][3], s[12][4], s[13][5], s[14][6]]))
    l.append(''.join([s[9][0], s[10][1], s[11]
             [2], s[12][3], s[13][4], s[14][5]]))
    l.append(''.join([s[10][0], s[11][1], s[12][2], s[13][3], s[14][4]]))
    # for column in range(4, MAXSIZE):
    #     leftUp = []
    #     for i in range(column+1):
    #         leftUp.append(status[column-i][i])
    #     l.append(''.join(leftUp))
    # for line in range(MAXSIZE-5):
    #     leftUp = []
    #     for j in range(MAXSIZE-1, line, -1):
    #         leftUp.append(status[j][line+MAXSIZE-j])
    #     l.append(''.join(leftUp))

    return l


def getDiagonal2(s):
    l = []
    l.append(''.join([s[0][4], s[1][3], s[2][2], s[3][1], s[4][0]]))
    l.append(''.join([s[0][5], s[1][4], s[2][3], s[3][2], s[4][1], s[5][0]]))
    l.append(''.join([s[0][6], s[1][5], s[2][4],
             s[3][3], s[4][2], s[5][1], s[6][0]]))
    l.append(''.join([s[0][7], s[1][6], s[2][5], s[3]
             [4], s[4][3], s[5][2], s[6][1], s[7][0]]))
    l.append(''.join([s[0][8], s[1][7], s[2][6], s[3][5],
             s[4][4], s[5][3], s[6][2], s[7][1], s[8][0]]))
    l.append(''.join([s[0][9], s[1][8], s[2][7], s[3][6], s[4]
             [5], s[5][4], s[6][3], s[7][2], s[8][1], s[9][0]]))
    l.append(''.join([s[0][10], s[1][9], s[2][8], s[3][7], s[4][6],
             s[5][5], s[6][4], s[7][3], s[8][2], s[9][1], s[10][0]]))
    l.append(''.join([s[0][11], s[1][10], s[2][9], s[3][8], s[4][7],
             s[5][6], s[6][5], s[7][4], s[8][3], s[9][2], s[10][1], s[11][0]]))
    l.append(''.join([s[0][12], s[1][11], s[2][10], s[3][9], s[4][8], s[5][7],
             s[6][6], s[7][5], s[8][4], s[9][3], s[10][2], s[11][1], s[12][0]]))
    l.append(''.join([s[0][13], s[1][12], s[2][11], s[3][10], s[4][9], s[5][8],
             s[6][7], s[7][6], s[8][5], s[9][4], s[10][3], s[11][2], s[12][1], s[13][0]]))
    l.append(''.join([s[0][14], s[1][13], s[2][12], s[3][11], s[4][10], s[5][9], s[6][8],
             s[7][7], s[8][6], s[9][5], s[10][4], s[11][3], s[12][2], s[13][1], s[14][0]]))
    l.append(''.join([s[1][14], s[2][13], s[3][12], s[4][11], s[5][10], s[6][9],
             s[7][8], s[8][7], s[9][6], s[10][5], s[11][4], s[12][3], s[13][2], s[14][1]]))
    l.append(''.join([s[2][14], s[3][13], s[4][12], s[5][11], s[6][10], s[7][9],
             s[8][8], s[9][7], s[10][6], s[11][5], s[12][4], s[13][3], s[14][2]]))
    l.append(''.join([s[3][14], s[4][13], s[5][12], s[6][11], s[7][10],
             s[8][9], s[9][8], s[10][7], s[11][6], s[12][5], s[13][4], s[14][3]]))
    l.append(''.join([s[4][14], s[5][13], s[6][12], s[7][11], s[8][10],
             s[9][9], s[10][8], s[11][7], s[12][6], s[13][5], s[14][4]]))
    l.append(''.join([s[5][14], s[6][13], s[7][12], s[8][11], s[9]
             [10], s[10][9], s[11][8], s[12][7], s[13][6], s[14][5]]))
    l.append(''.join([s[6][14], s[7][13], s[8][12], s[9][11],
             s[10][10], s[11][9], s[12][8], s[13][7], s[14][6]]))
    l.append(''.join([s[7][14], s[8][13], s[9][12], s[10]
             [11], s[11][10], s[12][9], s[13][8], s[14][7]]))
    l.append(''.join([s[8][14], s[9][13], s[10][12],
             s[11][11], s[12][10], s[13][9], s[14][8]]))
    l.append(''.join([s[9][14], s[10][13], s[11]
             [12], s[12][11], s[13][10], s[14][9]]))
    l.append(''.join([s[10][14], s[11][13], s[12][12], s[13][11], s[14][10]]))
    # for y in range(MAXSIZE - 4):
    #     leftDown = []
    #     for i in range(MAXSIZE-y):
    #         leftDown.append(status[y+i][i])
    #     l.append(''.join(leftDown))
    # for x in range(MAXSIZE - 5):
    #     leftDown = []
    #     for j in range(MAXSIZE-x-1):
    #         leftDown.append(status[j][x+j+1])
    #     l.append(''.join(leftDown))
    return l


class board:

    status = [['O']*15 for _ in range(15)]
    previous = None
    curStepPos = (None, None)    # (x,y)

    def __init__(self, status, level, previous=None, curStepPos=(None, None)) -> None:
        self.status = status
        self.previous = previous
        self.curStepPos = curStepPos
        self.level = level
        self.maxDepth = level*2

    def isFinish(self) -> bool:
        """judge is the game is finished

        Returns:
            bool: true is finished
        """

        curX, curY = self.curStepPos
        flag = self.status[curX][curY]

        # check row
        while True:
            if curX-1 >= 0 and self.status[curX-1][curY] == flag:
                curX -= 1
            else:
                break
        count = 1
        while True:
            if curX+1 <= MAXSIZE-1 and self.status[curX+1][curY] == flag:
                count += 1
                curX += 1
            else:
                break
        if count >= 5:
            return True

        # check line
        while True:
            if curY-1 >= 0 and self.status[curX][curY-1] == flag:
                curY -= 1
            else:
                break
        count = 1
        while True:
            if curY+1 <= MAXSIZE-1 and self.status[curX][curY+1] == flag:
                count += 1
                curY += 1
            else:
                break
        if count >= 5:
            return True

        # check diagonal
        while True:
            if curX-1 >= 0 and curY-1 >= 0 and self.status[curX-1][curY-1] == flag:
                curX -= 1
                curY -= 1
            else:
                break
        count = 1
        while True:
            if curX+1 <= MAXSIZE-1 and curY+1 <= MAXSIZE-1 and self.status[curX+1][curY+1] == flag:
                count += 1
                curX += 1
                curY += 1
            else:
                break
        if count >= 5:
            return True

        return False

    def getAllLines(self):
        # read every lines in the board
        lines = []

        # get every line
        lines += getLine(self.status)
        # for line in range(MAXSIZE):
        #     lines.append(''.join(self.status[line]))    # make a string

        # get every column
        lines += getColumn(self.status)
        # for column in range(MAXSIZE):
        #     temp = []
        #     for line in range(MAXSIZE):
        #         temp.append(self.status[line][column])
        #     lines.append(''.join(temp))

        # get every diagonal which is from left-up to right-down and length greater than 4
        lines += getDiagonal1(self.status)
        # for column in range(4, MAXSIZE):
        #     leftUp = []
        #     for i in range(column+1):
        #         leftUp.append(self.status[column-i][i])
        #     lines.append(''.join(leftUp))
        # for line in range(MAXSIZE-5):
        #     leftUp = []
        #     for j in range(MAXSIZE-1, line, -1):
        #         leftUp.append(self.status[j][line+MAXSIZE-j])
        #     lines.append(''.join(leftUp))

        # get every diagonal which is from left-down to right-up and length greater than 4
        lines += getDiagonal2(self.status)
        # for y in range(MAXSIZE - 4):
        #     leftDown = []
        #     for i in range(MAXSIZE-y):
        #         leftDown.append(self.status[y+i][i])
        #     lines.append(''.join(leftDown))
        # for x in range(MAXSIZE - 5):
        #     leftDown = []
        #     for j in range(MAXSIZE-x-1):
        #         leftDown.append(self.status[j][x+j+1])
        #     lines.append(''.join(leftDown))

        # print("total lines:",len(lines))
        return lines

    def evaluate(self) -> int:
        """evaluate the score of current board, always for the white

        Returns:
            int: score for white
        """

        lines = self.getAllLines()

        #! all score is for white player(AI)
        blackValidLines = getValidPieces(lines, BLACK)
        blackScore = getScore(blackValidLines, self.level)
        whiteValidLines = getValidPieces(lines, WHITE)
        whiteScore = getScore(whiteValidLines, self.level)

        score = whiteScore-blackScore
        # print("blackScore:",blackScore,"whiteScore:",whiteScore,"score:",score)
        return score

    def search(self):
        value, nexStepPos, a, b = self.maxValue(-inf, inf, 0)
        print("value:", value, "nexStepPos:", nexStepPos,
              "a:", a, "b:", b, "depth:", self.maxDepth)
        return nexStepPos

    def maxValue(self, alpha, beta, depth):
        if self.isFinish():
            return self.evaluate(), self.curStepPos, alpha, beta
        # if reach the maximum depth, return current score
        if depth >= self.maxDepth:
            global Searched
            Searched += 1
            return self.evaluate(), self.curStepPos, alpha, beta

        value = -inf
        nexStepPos = (None, None)

        for stepPos in getValidSteps(self.status, self.curStepPos, WHITE, level=self.level):
            x, y = stepPos
            nextStatus = deepcopy(self.status)
            # ! white is next step. if black, will cause the opponent to win
            nextStatus[x][y] = WHITE
            nextBoard = board(nextStatus, self.level, self, stepPos)

            thisValue, _, _, _ = nextBoard.minValue(alpha, beta, depth+1)
            # print("d:",depth,"Pos:",stepPos,"Value:",thisValue,"a:",alpha,"b:",beta)

            if thisValue > alpha:
                alpha = thisValue
                nexStepPos = stepPos
                value = thisValue
                if alpha >= beta:
                    break
            # if thisValue>value:
            #     value=thisValue
            #     nexStepPos=stepPos  #! the next step is not from minValue function. Because that is the best step after THIS step

            # if thisValue>=beta:
            #     return thisValue,stepPos,alpha,beta

            # alpha=max(alpha,value)

        # print("DONEdepth:",depth,"maxValue:",value,"nexStepPos:",nexStepPos,"alpha:",alpha,"beta:",beta)
        return value, nexStepPos, alpha, beta

    def minValue(self, alpha, beta, depth):
        if self.isFinish():
            return self.evaluate(), self.curStepPos, alpha, beta
        # if reach the maximum depth, return current score
        if depth >= self.maxDepth:
            global Searched
            Searched += 1
            return self.evaluate(), self.curStepPos, alpha, beta

        value = inf
        nexStepPos = (None, None)

        for stepPos in getValidSteps(self.status, self.curStepPos, BLACK, level=self.level):
            x, y = stepPos
            nextStatus = deepcopy(self.status)
            nextStatus[x][y] = BLACK
            nextBoard = board(nextStatus, self.level, self, stepPos)

            thisValue, _, _, _ = nextBoard.maxValue(alpha, beta, depth+1)
            # print("d:",depth,"Pos:",stepPos,"Value:",thisValue,"a:",alpha,"b:",beta)

            if thisValue < value:
                value = thisValue
                nexStepPos = stepPos

            if thisValue <= alpha:
                return thisValue, stepPos, alpha, beta

            beta = min(beta, value)

        # print("minValue:",value,"nexStepPos:",nexStepPos,"alpha:",alpha,"beta:",beta,"depth:",depth)
        return value, nexStepPos, alpha, beta


a = board([
    ['@', '@', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['@', '@', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'X']
], curStepPos=(14, 14), level=HARD)
startTime = time()
a.evaluate()
a.search()
print("time:", time()-startTime)
print("Searched:", Searched, "Scored:", Scored, "Level:", a.level)
