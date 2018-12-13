## Advent of Code 2018: Day 13
## https://adventofcode.com/2018/day/13
## Jesse Williams
## Answers: [Part 1]: , [Part 2]:

import numpy as np
from enum import Enum
np.set_printoptions(threshold=np.inf, linewidth=100)

class Dir(Enum):
    EAST = 0
    NORTH = 1
    WEST = 2
    SOUTH = 3

def getDir(char):
    if char == '>':
        return Dir.EAST
    elif char == '^':
        return Dir.NORTH
    elif char == '<':
        return Dir.WEST
    elif char == 'v':
        return Dir.SOUTH

def handleCartMove(dir, map, cleanMap, coords, carts, cartsMovedThisTick, haltOnCollision=True):
    (i, j) = coords
    collisions = []

    if (i,j) not in cartsMovedThisTick:

        if dir == Dir.EAST:
            # Check for collision first
            if map[i, j+1] in ['>', 'v', '<', '^']:
                if haltOnCollision:
                    map[i, j] = cleanMap[i, j]
                    map[i, j+1] = 'X'
                else:
                    map[i, j] = cleanMap[i, j]
                    map[i, j+1] = cleanMap[i, j+1]
                    del carts[(i, j)]
                    del carts[(i, j+1)]

                collisions.append((i, j+1))

            elif map[i, j+1] == 'X':
                # A cart collided with this cart, and we are only now updating the second cart's position. So just remove the second cart.
                map[i, j] = cleanMap[i, j]

            # Check east location in map
            elif cleanMap[i, j+1] == '+':
                if carts[(i,j)]%3 == 0:  # turn left
                    map[i, j+1] = '^'
                if carts[(i,j)]%3 == 1:  # go straight
                    map[i, j+1] = '>'
                if carts[(i,j)]%3 == 2:  # turn right
                    map[i, j+1] = 'v'
                map[i, j] = cleanMap[i, j]
                carts[(i, j+1)] = carts[(i,j)] + 1  # update carts dict (increment turn counter)
                del carts[(i,j)]
                cartsMovedThisTick.append((i, j+1))

            elif cleanMap[i, j+1] == '-':
                map[i, j+1] = '>'
                map[i, j] = cleanMap[i, j]
                carts[(i, j+1)] = carts[(i,j)]  # update carts dict
                del carts[(i,j)]
                cartsMovedThisTick.append((i, j+1))

            elif cleanMap[i, j+1] == '/':
                map[i, j+1] = '^'
                map[i, j] = cleanMap[i, j]
                carts[(i, j+1)] = carts[(i,j)]  # update carts dict
                del carts[(i,j)]
                cartsMovedThisTick.append((i, j+1))

            elif cleanMap[i, j+1] == '\\':
                map[i, j+1] = 'v'
                map[i, j] = cleanMap[i, j]
                carts[(i, j+1)] = carts[(i,j)]  # update carts dict
                del carts[(i,j)]
                cartsMovedThisTick.append((i, j+1))

            else:
                print('Error.')


        elif dir == Dir.NORTH:
            # Check for collision first
            if map[i-1, j] in ['>', 'v', '<', '^']:
                if haltOnCollision:
                    map[i, j] = cleanMap[i, j]
                    map[i-1, j] = 'X'
                else:
                    map[i, j] = cleanMap[i, j]
                    map[i-1, j] = cleanMap[i-1, j]
                    del carts[(i, j)]
                    del carts[(i-1, j)]

                collisions.append((i-1, j))

            elif map[i-1, j] == 'X':
                # A cart collided with this cart, and we are only now updating the second cart's position. So just remove the second cart.
                map[i, j] = cleanMap[i, j]

            # Check north location in map
            elif cleanMap[i-1, j] == '+':
                if carts[(i,j)]%3 == 0:  # turn left
                    map[i-1, j] = '<'
                if carts[(i,j)]%3 == 1:  # go straight
                    map[i-1, j] = '^'
                if carts[(i,j)]%3 == 2:  # turn right
                    map[i-1, j] = '>'
                map[i, j] = cleanMap[i, j]
                carts[(i-1, j)] = carts[(i,j)] + 1  # update carts dict (increment turn counter)
                del carts[(i,j)]
                cartsMovedThisTick.append((i-1, j))

            elif cleanMap[i-1, j] == '|':
                map[i-1, j] = '^'
                map[i, j] = cleanMap[i, j]
                carts[(i-1, j)] = carts[(i,j)]  # update carts dict
                del carts[(i,j)]
                cartsMovedThisTick.append((i-1, j))

            elif cleanMap[i-1, j] == '/':
                map[i-1, j] = '>'
                map[i, j] = cleanMap[i, j]
                carts[(i-1, j)] = carts[(i,j)]  # update carts dict
                del carts[(i,j)]
                cartsMovedThisTick.append((i-1, j))

            elif cleanMap[i-1, j] == '\\':
                map[i-1, j] = '<'
                map[i, j] = cleanMap[i, j]
                carts[(i-1, j)] = carts[(i,j)]  # update carts dict
                del carts[(i,j)]
                cartsMovedThisTick.append((i-1, j))

            else:
                print('Error.')


        elif dir == Dir.WEST:
            # Check for collision first
            if map[i, j-1] in ['>', 'v', '<', '^']:
                if haltOnCollision:
                    map[i, j] = cleanMap[i, j]
                    map[i, j-1] = 'X'
                else:
                    map[i, j] = cleanMap[i, j]
                    map[i, j-1] = cleanMap[i, j-1]
                    del carts[(i, j)]
                    del carts[(i, j-1)]

                collisions.append((i, j-1))

            elif map[i, j-1] == 'X':
                # A cart collided with this cart, and we are only now updating the second cart's position. So just remove the second cart.
                map[i, j] = cleanMap[i, j]

            # Check west location in map
            elif cleanMap[i, j-1] == '+':
                if carts[(i,j)]%3 == 0:  # turn left
                    map[i, j-1] = 'v'
                if carts[(i,j)]%3 == 1:  # go straight
                    map[i, j-1] = '<'
                if carts[(i,j)]%3 == 2:  # turn right
                    map[i, j-1] = '^'
                map[i, j] = cleanMap[i, j]
                carts[(i, j-1)] = carts[(i,j)] + 1  # update carts dict (increment turn counter)
                del carts[(i,j)]
                cartsMovedThisTick.append((i, j-1))

            elif cleanMap[i, j-1] == '-':
                map[i, j-1] = '<'
                map[i, j] = cleanMap[i, j]
                carts[(i, j-1)] = carts[(i,j)]  # update carts dict
                del carts[(i,j)]
                cartsMovedThisTick.append((i, j-1))

            elif cleanMap[i, j-1] == '/':
                map[i, j-1] = 'v'
                map[i, j] = cleanMap[i, j]
                carts[(i, j-1)] = carts[(i,j)]  # update carts dict
                del carts[(i,j)]
                cartsMovedThisTick.append((i, j-1))

            elif cleanMap[i, j-1] == '\\':
                map[i, j-1] = '^'
                map[i, j] = cleanMap[i, j]
                carts[(i, j-1)] = carts[(i,j)]  # update carts dict
                del carts[(i,j)]
                cartsMovedThisTick.append((i, j-1))

            else:
                print('Error.')


        elif dir == Dir.SOUTH:
            # Check for collision first
            if map[i+1, j] in ['>', 'v', '<', '^']:
                if haltOnCollision:
                    map[i, j] = cleanMap[i, j]
                    map[i+1, j] = 'X'
                else:
                    map[i, j] = cleanMap[i, j]
                    map[i+1, j] = cleanMap[i+1, j]
                    del carts[(i, j)]
                    del carts[(i+1, j)]

                collisions.append((i+1, j))

            elif map[i+1, j] == 'X':
                # A cart collided with this cart, and we are only now updating the second cart's position. So just remove the second cart.
                map[i, j] = cleanMap[i, j]

            # Check north location in map
            elif cleanMap[i+1, j] == '+':
                if carts[(i,j)]%3 == 0:  # turn left
                    map[i+1, j] = '>'
                if carts[(i,j)]%3 == 1:  # go straight
                    map[i+1, j] = 'v'
                if carts[(i,j)]%3 == 2:  # turn right
                    map[i+1, j] = '<'
                map[i, j] = cleanMap[i, j]
                carts[(i+1, j)] = carts[(i,j)] + 1  # update carts dict (increment turn counter)
                del carts[(i,j)]
                cartsMovedThisTick.append((i+1, j))

            elif cleanMap[i+1, j] == '|':
                map[i+1, j] = 'v'
                map[i, j] = cleanMap[i, j]
                carts[(i+1, j)] = carts[(i,j)]  # update carts dict
                del carts[(i,j)]
                cartsMovedThisTick.append((i+1, j))

            elif cleanMap[i+1, j] == '/':
                map[i+1, j] = '<'
                map[i, j] = cleanMap[i, j]
                carts[(i+1, j)] = carts[(i,j)]  # update carts dict
                del carts[(i,j)]
                cartsMovedThisTick.append((i+1, j))

            elif cleanMap[i+1, j] == '\\':
                map[i+1, j] = '>'
                map[i, j] = cleanMap[i, j]
                carts[(i+1, j)] = carts[(i,j)]  # update carts dict
                del carts[(i,j)]
                cartsMovedThisTick.append((i+1, j))

            else:
                print('Error.')

    return map, carts, cartsMovedThisTick, collisions


def generateCleanMap(map):
    cleanMap = np.copy(map)
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i, j] in ['>', '<']:
                cleanMap[i, j] = '-'
            elif map[i, j] in ['^', 'v']:
                cleanMap[i, j] = '|'
    return cleanMap

def registerCarts(map):
    # Finds initial coordinates of all carts and creates a dict {(i, j): 0} with coords (i,j) and a turn counter initialized at 0.
    # Turn counter = 0 (mod 3): Cart turns left
    # Turn counter = 1 (mod 3): Cart goes straight
    # Turn counter = 2 (mod 3): Cart turns right
    carts = {}

    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i, j] in ['>', 'v', '<', '^']:
                carts[(i, j)] = 0
    return carts

def printMap(map, label=''):
    # Pretty prints a map
    printString = label + '\n'
    for row in map:
        printString += ''.join(list(row)) + '\n'
    printString += '\n'
    print(printString)


def runUntilCollision(map, cleanMap, maxTicks):
    # Main update loop. Scan map and move carts, returning when a collision is found.
    printMap(map, label='tick 0')

    carts = registerCarts(map)
    for tick in range(1, maxTicks+1):
        cartsMovedThisTick = []
        for i, row in enumerate(map):
            for j, block in enumerate(row):
                if block in ['>', 'v', '<', '^']:
                    dir = getDir(block)
                    map, carts, cartsMovedThisTick, collisions = handleCartMove(dir, map, cleanMap, (i, j), carts, cartsMovedThisTick, haltOnCollision=True)

                    if collisions:
                        # Handle collision
                        printMap(map, label='tick {}'.format(tick))
                        print('Collision occured at ({0[1]}, {0[0]}) on tick {1}.'.format(collisions[0], tick))
                        return

        # End of tick
        #printMap(map, label='tick {}'.format(tick))

def runUntilOneCartRemains(map, cleanMap, maxTicks):
    # Main update loop. Scan map and move carts, returning when all collisions have been cleaned up and only one cart remains.
    printMap(map, label='tick 0')

    carts = registerCarts(map)
    for tick in range(1, maxTicks+1):
        cartsMovedThisTick = []
        for i, row in enumerate(map):
            for j, block in enumerate(row):
                if block in ['>', 'v', '<', '^']:
                    dir = getDir(block)
                    map, carts, cartsMovedThisTick, collisions = handleCartMove(dir, map, cleanMap, (i, j), carts, cartsMovedThisTick, haltOnCollision=False)

                    if collisions:
                        # Handle collision
                        print('Collision occured at ({0[1]}, {0[0]}) on tick {1}. Carts removed.'.format(collisions[0], tick))

        # End of tick
        if len(cartsMovedThisTick) == 1:  # if a cart collided this tick, it will not be added to this list
            printMap(map, label='tick {}'.format(tick))
            print('At the end of tick {0}, only one cart remains at position ({1[1]}, {1[0]}).'.format(tick, cartsMovedThisTick[0]))
            return



if __name__ == "__main__":

    # Read map into numpy array
    with open('day13_input.txt') as f:
        line = f.readline()
        map = np.array([list(line[:-1])])
        while True:
            line = f.readline()
            if not line: break
            map = np.append(map, [list(line[:-1])], axis=0)
    cleanMap = generateCleanMap(map)  # create a clean copy of the map with no carts

    ## Part 1
    maxTicks = 1000
    runUntilCollision(map.copy(), cleanMap.copy(), maxTicks)

    ## Part 2
    maxTicks = 100000
    runUntilOneCartRemains(map.copy(), cleanMap.copy(), maxTicks)
