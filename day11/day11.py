## Advent of Code 2018: Day 11
## https://adventofcode.com/2018/day/11
## Jesse Williams
## Answers: [Part 1]: (21,53), [Part 2]: (233,250,12)

import math, time
import numpy as np

INPUT = 6548

def getPowerLevels(fuelGrid, serialNum):
    for j in range(1, 301):
        for i in range(1, 301):
            rackID = i+10
            powerLevel = rackID * j
            powerLevel += serialNum
            powerLevel *= rackID
            powerLevel = math.floor(powerLevel/100) % 10
            powerLevel -= 5

            fuelGrid[i-1,j-1] = powerLevel
    return fuelGrid

if __name__ == "__main__":
    fuelGrid = np.zeros((300, 300))
    fuelGrid = getPowerLevels(fuelGrid, INPUT)

    ## Part 1
    t_s = time.time()
    maxPower = [0, (0,0)]  # holds the value and coords of the largest power square
    for j in range(1, 301-3):
        for i in range(1, 301-3):
            totalPower = sum(list(fuelGrid[i-1:i+2, j-1:j+2].ravel()))  # find sum of all fuel levels in 3x3 square
            if totalPower > maxPower[0]:
                maxPower[0] = totalPower
                maxPower[1] = (i, j)
    t_e = time.time() - t_s

    print('The 3x3 square with the largest total power {} begins at ({}, {}). [Took {} seconds]'.format(maxPower[0], maxPower[1][0], maxPower[1][1]), t_e)

    ## Part 2
    t_s = time.time()
    maxPower = [0, (0,0), 1]  # holds the value, coords, and size of the largest power square
    for squareSize in range(1, 301):
        for j in range(1, 301-squareSize):
            for i in range(1, 301-squareSize):
                totalPower = sum(list(fuelGrid[i-1 : i-1+squareSize,  j-1 : j-1+squareSize].ravel()))  # find sum of all fuel levels in nxn square
                if totalPower > maxPower[0]:
                    maxPower[0] = totalPower
                    maxPower[1] = (i, j)
                    maxPower[2] = squareSize
        if squareSize%10 == 0: print('Currently checking all {0}x{0} squares...'.format(squareSize))
    t_e = time.time() - t_s

    print('The the largest total power {0} is in an {1}x{1} square beginning at ({2}, {3}). [Took {4} seconds]'.format(maxPower[0], maxPower[2], maxPower[1][0], maxPower[1][1], t_e))
