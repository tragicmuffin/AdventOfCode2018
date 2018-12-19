## Advent of Code 2018: Day 18
## https://adventofcode.com/2018/day/18
## Jesse Williams
## Answers: [Part 1]: 574590, [Part 2]: 183787

import time
import numpy as np
np.set_printoptions(threshold=np.inf, linewidth=120)

def encodeSymbol(symbol):
    if symbol == '.':
        return 0
    elif symbol == '|':
        return 1
    elif symbol == '#':
        return 2
    else:
        return -1  # error

def getAdjacent(state, index):
    (i, j) = index
    adjDict = {0: 0, 1: 0, 2: 0}

    for p in range(i-1, i+2):
        for q in range(j-1, j+2):
            if (p, q) != (i, j) and 0 <= p < state.shape[0] and 0 <= q < state.shape[1]:
                # Check bounds and ignore own position
                adjDict[state[p, q]] += 1
    return adjDict

def renderState(state, label=''):
    print('\n' + label)
    for i in range(state.shape[0]):
        rowStr = ''
        for entry in state[i, :]:
            if entry == 0:
                rowStr += '.'  # open ground
            elif entry == 1:
                rowStr += '|'  # trees
            elif entry == 2:
                rowStr += '#'  # lumberyard
            else:
                rowStr += 'ERROR'  # shouldn't happen
        print(rowStr)


if __name__ == '__main__':
    # Read state
    with open('day18_input.txt') as f:
        allRows = []

        line = f.readline()
        while line:
            allRows.append(list(line)[:-1])
            line = f.readline()

    #### Matrix encoding ####
    #  . = open ground = 0  #
    #  | = trees       = 1  #
    #  # = lumberyard  = 2  #
    #########################
    allRowsEncoded = []
    for row in allRows:
        allRowsEncoded.append( list(map(encodeSymbol, row)) )  # transforms the list of string symbols to a list of integers

    initialState = np.array(allRowsEncoded)
    state = initialState.copy()

    #### Policy ################
    #  [(3+) 1] 0 -> 1
    #  [(3+) 2] 1 -> 2
    #  [(1+) 2 && (1+) 1] 2 -> 2
    #    else: 2 -> 0
    ############################

    ## Part 1
    t_s = time.time()

    mins = 10
    renderState(state, label='t = 0')
    for t in range(mins):
        nextState = state.copy()

        for j in range(state.shape[1]):
            for i in range(state.shape[0]):
                adj = getAdjacent(state, (i, j))  # returns a dict of counts of adjacent acres (not including this one)
                if state[i, j] == 0 and adj[1] >= 3:
                    nextState[i, j] = 1
                elif state[i, j] == 1 and adj[2] >= 3:
                    nextState[i, j] = 2
                elif state[i, j] == 2:
                    if adj[2] >= 1 and adj[1] >= 1:
                        nextState[i, j] = 2  # no change
                    else:
                        nextState[i, j] = 0

        state = nextState

        renderState(state, label='t = '+str(t+1))

    values, counts = np.unique(state, return_counts=True)  # find all unique values in matrix and get their occurence counts
    acreCounts = dict(zip(values, counts))  # organize into {value: count} dict

    t_e = time.time() - t_s
    print('After {} minutes, the area contains {} acres of open ground, {} acres of trees, and {} acres of lumberyard. [{} seconds]'.format(t+1, acreCounts[0], acreCounts[1], acreCounts[2], t_e))


    ## Part 2
    t_s = time.time()

    state = initialState.copy()
    targetMins = 1000000000
    mins = 2000

    resourceValues = []

    for t in range(mins):
        nextState = state.copy()

        for j in range(state.shape[1]):
            for i in range(state.shape[0]):
                adj = getAdjacent(state, (i, j))  # returns a dict of counts of adjacent acres (not including this one)
                if state[i, j] == 0 and adj[1] >= 3:
                    nextState[i, j] = 1
                elif state[i, j] == 1 and adj[2] >= 3:
                    nextState[i, j] = 2
                elif state[i, j] == 2:
                    if adj[2] >= 1 and adj[1] >= 1:
                        nextState[i, j] = 2  # no change
                    else:
                        nextState[i, j] = 0

        state = nextState

        values, counts = np.unique(state, return_counts=True)  # find all unique values in matrix and get their occurence counts
        acreCounts = dict(zip(values, counts))  # organize into {value: count} dict

        # The state automata seems to fall into a periodic pattern sometime after 500 minutes, so we start tracking after 1000 to be safe.
        if t >= 1000:
            resourceValues.append(acreCounts[1]*acreCounts[2])


    # Find period of resource value pattern
    resourceValPeriod = resourceValues[1:].index(resourceValues[0]) + 1
    targetResourceVal = resourceValues[(targetMins - 1001) % resourceValPeriod]

    t_e = time.time() - t_s
    print('\nAfter {} minutes, the area will have a resource value of {}. [{} seconds]'.format(targetMins, targetResourceVal, t_e))
