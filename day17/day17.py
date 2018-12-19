## Advent of Code 2018: Day 17
## https://adventofcode.com/2018/day/17
## Jesse Williams
## Answers: [Part 1]: 30737, [Part 2]: 24699

import re
import numpy as np
from enum import Enum

class Tile(Enum):
    Sand = 0
    Clay = 1
    WaterFlowing = 2
    WaterResting = 3
    WaterSource = -1

def toMapCoords(matrixCoords):
    global SHIFT
    return (matrixCoords[1] + SHIFT[1], matrixCoords[0] + SHIFT[0])  # also flip (row,col) components to (x,y)
def toMatrixCoords(mapCoords):
    global SHIFT
    return (mapCoords[1] - SHIFT[1], mapCoords[0] - SHIFT[0])  # also flip (x,y) components to (row,col)

def renderMap(map, startAt=0, stopAt=0, label=''):
    #print('\nx: {}..{},  y: {}..{}\n'.format(SHIFT[0], SHIFT[0]+map.shape[1]-1, SHIFT[1], SHIFT[1]+map.shape[0]-1))
    print('\n' + label)
    for i in range(startAt, map.shape[0]):
        rowStr = ''
        for entry in map[i, :]:
            if entry == Tile.Sand.value:
                rowStr += '.'  # sand
            elif entry == Tile.Clay.value:
                rowStr += '#'  # clay
            elif entry == Tile.WaterFlowing.value:
                rowStr += '|'  # water (flowing)
            elif entry == Tile.WaterResting.value:
                rowStr += '~'  # water (at rest)
            elif entry == Tile.WaterSource.value:
                rowStr += '+'  # water source
            else:
                rowStr += 'ERROR'  # shouldn't happen
        print(rowStr)

        if (0 < stopAt <= i):
            break  # if a stopping point was given, stop printing after this many lines

def getConnectedWaterTileRange(tile, map):
    # Returns a tuple containing the range of x-coords of the horizontally-connected section of water
    tileX, tileY = tile

    connectedRangeLeft, connectedRangeRight = tileX, tileX
    left, right = 1, 1

    while True:  # extend to the left
        if (toMatrixCoords((tileX-left, tileY))[1] > 0) and map[toMatrixCoords((tileX-left, tileY))] == Tile.WaterFlowing.value:
            connectedRangeLeft = tileX-left
            left += 1
        else: break

    while True:  # extend to the right
        if (toMatrixCoords((tileX+right, tileY))[1] < map.shape[1]) and map[toMatrixCoords((tileX+right, tileY))] == Tile.WaterFlowing.value:
            connectedRangeRight = tileX+right
            right += 1
        else: break

    return (connectedRangeLeft, connectedRangeRight)


def simulateStep(map, activeWaterTiles):
    for (tileX, tileY) in activeWaterTiles:
        ## Policy 0: Bottom of map  ##
        # Check if we've reached the bottom of the map before attempting to check entries below
        if tileY+1 >= map.shape[0]:
            continue

        ## Policy 1: Move down ##
        # Check to see if water can fall
        elif map[toMatrixCoords((tileX, tileY+1))] == Tile.Sand.value:
            # If there is sand below, shift our active water tile downward
            activeWaterTiles.append((tileX, tileY+1))
            map[toMatrixCoords((tileX, tileY+1))] = Tile.WaterFlowing.value
            activeWaterTiles.remove((tileX, tileY))
        elif map[toMatrixCoords((tileX, tileY+1))] in [Tile.Clay.value, Tile.WaterResting.value]:
            # If there is clay or resting water below, we may need to start moving sideways (jump to next policy).

            ## Policy 2: Move sideways ##
            # In this policy, only handle a water tile that is directly below a flowing water tile.
            if map[toMatrixCoords((tileX, tileY-1))] == Tile.WaterFlowing.value:
                (connectedRangeLeft, connectedRangeRight) = getConnectedWaterTileRange((tileX, tileY), map)

                if toMatrixCoords((connectedRangeLeft-1, tileY))[1] < 0: pass  # Before checking to the left, make sure we're not at the border. If we are, then skip this check.
                elif map[toMatrixCoords((connectedRangeLeft-1, tileY))] == Tile.Sand.value and map[toMatrixCoords((connectedRangeLeft, tileY+1))] in [Tile.Clay.value, Tile.WaterResting.value]:  # left
                    activeWaterTiles.append((connectedRangeLeft-1, tileY))
                    map[toMatrixCoords((connectedRangeLeft-1, tileY))] = Tile.WaterFlowing.value

                if toMatrixCoords((connectedRangeRight+1, tileY))[1] >= map.shape[1]: pass  # Before checking to the right, make sure we're not at the border. If we are, then skip this check.
                elif map[toMatrixCoords((connectedRangeRight+1, tileY))] == Tile.Sand.value and map[toMatrixCoords((connectedRangeRight, tileY+1))] in [Tile.Clay.value, Tile.WaterResting.value]:  # right
                    activeWaterTiles.append((connectedRangeRight+1, tileY))
                    map[toMatrixCoords((connectedRangeRight+1, tileY))] = Tile.WaterFlowing.value

                if toMatrixCoords((connectedRangeLeft-1, tileY))[1] < 0 or toMatrixCoords((connectedRangeRight+1, tileY))[1] >= map.shape[1]: pass
                elif map[toMatrixCoords((connectedRangeLeft-1, tileY))] == Tile.Clay.value and map[toMatrixCoords((connectedRangeRight+1, tileY))] == Tile.Clay.value:
                    # If we've hit clay on both sides at this level, convert all connected activeWaterTiles to static water tiles and replace the active tile with the stream above.
                    for x in range(connectedRangeLeft, connectedRangeRight+1):
                        try:
                            activeWaterTiles.remove((x, tileY))  # if two streams converge in the same pool, we will try to double-delete some tiles
                        except ValueError:
                            pass
                        map[toMatrixCoords((x, tileY))] = Tile.WaterResting.value

                        if map[toMatrixCoords((x, tileY-1))] == Tile.WaterFlowing.value and (x, tileY-1) not in activeWaterTiles:
                            # Since we're clearing all active tiles, make sure to re-activate ALL flowing streams above the current pool.
                            activeWaterTiles.append((x, tileY-1))
    return map, activeWaterTiles

if __name__ == "__main__":
    patt_X_range = re.compile(r"y=(\d+),\sx=(\d+)..(\d+)")
    patt_Y_range = re.compile(r"x=(\d+),\sy=(\d+)..(\d+)")

    allCoords = []
    mapSizeX, mapSizeY = [500, 500], [0, 0]
    mapSizeY_Adjustment = 100  # this is used to measure the distance from the water source to the lowest y-coord in the scan data (clay)
    with open('day17_input.txt') as f:
        line = f.readline()

        while line:
            if patt_X_range.match(line):
                y, x0, x1 = tuple(map(int, patt_X_range.match(line).groups()))
                for x in range(x0, x1+1):
                    allCoords.append((x, y))
                if x0 < mapSizeX[0]: mapSizeX[0] = x0
                if x1 > mapSizeX[1]: mapSizeX[1] = x1
                if y > mapSizeY[1]: mapSizeY[1] = y
                if y-1 < mapSizeY_Adjustment: mapSizeY_Adjustment = y-1

            else:
                x, y0, y1 = tuple(map(int, patt_Y_range.match(line).groups()))
                for y in range(y0, y1+1):
                    allCoords.append((x, y))
                if x < mapSizeX[0]: mapSizeX[0] = x
                if x > mapSizeX[1]: mapSizeX[1] = x
                if y1 > mapSizeY[1]: mapSizeY[1] = y1
                if y0-1 < mapSizeY_Adjustment: mapSizeY_Adjustment = y0-1

            line = f.readline()

    mapRange = (mapSizeY[1] - mapSizeY[0] + 1, mapSizeX[1] - mapSizeX[0] + 3)  # (rows, cols) = (y, x). Give a 1-unit buffer on both sides in the x direction.
    SHIFT = (mapSizeX[0] - 1, mapSizeY[0])  # stores the left-most and top-most coords on the map coord system

    #### Map Rules ####
    # -1 = water source (only one of these, at map coords (500, 0))
    # 0 = sand (empty space)
    # 1 = clay
    # 2 = water (flowing)
    # 3 = water (at rest)
    ###################

    map = np.zeros(mapRange)

    # Fill map with initial data (default 0s represent sand, 1s represent clay)
    for coord in allCoords:
        map[toMatrixCoords(coord)] = Tile.Clay.value
    # Insert water source
    map[toMatrixCoords((500, 0))] = Tile.WaterSource.value

    initialMap = map.copy()  # save copy of initial map state

    t = 0
    #renderMap(map, label='t = {}'.format(t), stopAt=1)

    activeWaterTiles = [(500, 0)]  # These are water tiles that may still be able to flow. Initialize with water source.
    lastActiveWaterTiles = [(0, 0)]
    while True:
        t += 1

        map, activeWaterTiles = simulateStep(map, activeWaterTiles)

        if lastActiveWaterTiles == activeWaterTiles:
            # If the active water tiles did not change this step, we're done.
            break
        else:
            lastActiveWaterTiles = activeWaterTiles.copy()


        if t % 1000 == 0:
            # Rough tracking based on the last-added active water tile
            activeRow = toMatrixCoords(activeWaterTiles[-1])[0]  # find row of the active tile
            renderMap(map, startAt=activeRow-10, stopAt=activeRow+10, label='t = '+str(t))

    renderMap(map, label='t = '+str(t))  # show final map

    # Count water tiles
    values, counts = np.unique(map, return_counts=True)  # find all unique values in matrix and get their occurence counts
    tileCounts = dict(zip(values, counts))  # organize into {value: count} dict

    waterTileTotal = tileCounts[Tile.WaterResting.value] + tileCounts[Tile.WaterFlowing.value] - mapSizeY_Adjustment
    print('After {} timesteps, a total of {} tiles on the map were reached by water, {} by resting water and {} by flowing water.'.format(t-1, waterTileTotal, tileCounts[Tile.WaterResting.value], tileCounts[Tile.WaterFlowing.value]-mapSizeY_Adjustment))
