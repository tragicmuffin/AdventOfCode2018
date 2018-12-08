## Advent of Code 2018: Day 6
## https://adventofcode.com/2018/day/6
## Jesse Williams
## Answers: [Part 1]: , [Part 2]:

import re, pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

FRAME = 1
NUM_COORDS = 0
EMPTY_LABEL = 0
COLLISIONS = []

def voronoiStep(coordMatrix, coordDict):
    # Takes a matrix and expands each entry in all Manhattan directions, clearing the entry if a collision is found(?)
    allStepCoords = []  # keeps track of all coords added so far this step to check for collisions
    global COLLISIONS
    for label in coordDict:
        newCoords = []
        for (x, y) in coordDict[label]:
            step_EW = [x-1, x+1]
            step_NS = [y-1, y+1]

            for m in step_EW:
                if (m, y) in allStepCoords and (m, y) not in COLLISIONS:  # if this coord has been a collision, skip it
                    COLLISIONS.append((m, y))
                elif (m, y) not in coordDict[label] and (m, y) not in newCoords:
                    newCoords.append((m, y))
                    # Check if this new coord is inside any other areas. If so, remove it.
                    for otherLabel in coordDict:
                        if otherLabel == label: continue
                        if (m, y) in coordDict[otherLabel]:
                            newCoords.remove((m, y))

            for n in step_NS:
                if (x, n) in allStepCoords and (x, n) not in COLLISIONS:  # if this coord has been a collision, skip it
                    COLLISIONS.append((x, n))
                elif (x, n) not in coordDict[label] and (x, n) not in newCoords:
                    newCoords.append((x, n))
                    # Check if this new coord is inside any other areas. If so, remove it.
                    for otherLabel in coordDict:
                        if otherLabel == label: continue
                        if (x, n) in coordDict[otherLabel]:
                            newCoords.remove((x, n))

        # If two labels reached the same coord point this step, that point is an equal distance to both, and so should be dropped
        coordDict[label] += newCoords  # add new coord points into list of coords
        allStepCoords += newCoords

    # Add new coords to matrix, setting collisions to 0
    for label in coordDict:
        for (x, y) in coordDict[label]:
            if (x, y) in COLLISIONS:
                coordMatrix[x, y] = 0
            else:
                coordMatrix[x, y] = label
    return coordMatrix, coordDict

def voronoiFinished(coordMatrix):
    # Finished when no EMPTY_LABEL's remain
    if (EMPTY_LABEL in list(coordMatrix.flatten())):
        return False
    else:
        return True

def createCoordMatrix(seedCoordList):
    global EMPTY_LABEL

    # Find size of box
    SE_padding = 35
    X, Y = 0, 0
    for (x, y) in seedCoordList:
        if x > X: X = x
        if y > Y: Y = y

    # Initialize array
    size = max([X+SE_padding, Y+SE_padding])  # make a square grid SE_padding px larger than the largest coordinate
    matrix = np.zeros((size, size))
    matrix.fill(EMPTY_LABEL)

    # Insert seed coords
    coordDict = {}
    label = 1
    for (x, y) in seedCoordList:
        matrix[x, y] = label
        coordDict[label] = [(x, y)]
        label += 1

    return matrix, coordDict

def measureAreas(coordMatrix, coordDict):
    areaDict = {}
    coordMatrixList = list(coordMatrix.flatten())
    for label in coordDict:
        areaDict[label] = coordMatrixList.count(label)
    return areaDict

def expandMatrix(matrix, scale):
    # Expands a matrix by a given (int) scale for rendering
    if scale == 1: return matrix
    (m, n) = matrix.shape
    matrix = np.repeat(matrix, scale, axis=0)
    matrix = np.repeat(matrix, scale, axis=1).reshape(scale*m, scale*n)
    return matrix

def initializeRender(coordMatrix, scale):
    # Make modified colormap
    colorMap = cm.get_cmap('plasma', NUM_COORDS+2)
    newcolors = colorMap(np.linspace(0, 1, NUM_COORDS+2))
    collisionColor = np.array([0.25, 0.25, 0.25, 0.5])
    emptyColor = np.array([212/256, 234/256, 231/256, 1])
    newcolors[:1, :] = collisionColor
    newcolors[EMPTY_LABEL, :] = emptyColor
    newColorMap = ListedColormap(newcolors)

    dpi = 80
    margin = 0.05  # % of the width/height of the figure

    plt.ion()
    plt.axis('off')
    plt.tight_layout()

    coordMatrix = expandMatrix(coordMatrix, scale)
    xpixels, ypixels = coordMatrix.shape

    fig = plt.figure(figsize=(ypixels/dpi, xpixels/dpi), dpi=dpi)
    return fig, newColorMap

def updateRender(coordMatrix, scale, fig, colormap, realtime=True):
    coordMatrix = expandMatrix(coordMatrix, scale)
    fig.figimage(coordMatrix, cmap=colormap)
    if realtime:
        fig.canvas.draw()
        fig.canvas.flush_events()
    global FRAME
    plt.savefig('img/voronoi_frame{}.png'.format(FRAME))
    FRAME += 1


if __name__ == "__main__":
    try:
        with open('day6_snapshot.p', 'rb') as f:
            (FRAME, coordMatrix, coordDict, COLLISIONS) = pickle.load(f)
        # Set global size variables. These help determine where "empty" number should be for colormapping.
        NUM_COORDS = len(coordDict)
        EMPTY_LABEL = NUM_COORDS+1
    except:
        coordList = []
        with open('day6_input.txt') as f:
            pattern = re.compile(r"(\d+),\s(\d+)")
            while True:
                line = f.readline()
                if line == '': break
                matches = pattern.match(line)
                coordList.append(tuple([int(i) for i in matches.groups()]))

        # Set global size variables. These help determine where "empty" number should be for colormapping.
        NUM_COORDS = len(coordList)
        EMPTY_LABEL = NUM_COORDS+1
        coordMatrix, coordDict = createCoordMatrix(coordList)

    scale = 1
    fig, colormap = initializeRender(coordMatrix, scale)
    done = False
    i = 0
    updateRender(coordMatrix, scale, fig, colormap, realtime=False)
    while not done:
        i += 1
        coordMatrix, coordDict = voronoiStep(coordMatrix, coordDict)
        updateRender(coordMatrix, scale, fig, colormap, realtime=False)

        with open('day6_snapshot.p', 'wb') as f:
            pickle.dump((FRAME, coordMatrix, coordDict, COLLISIONS), f)

        if voronoiFinished(coordMatrix):
            done = True

    areaDict = measureAreas(coordMatrix, coordDict)
    #for label in areaDict:
    #    print('{}: {}'.format(label, areaDict[label]))

    largestArea = list(filter(lambda x:x[1] == min(areaDict.values()), areaDict.items()))[0]
    print('Coordinate point with label {} has the largest area at {}.'.format(largestArea[0], largestArea[1]))
