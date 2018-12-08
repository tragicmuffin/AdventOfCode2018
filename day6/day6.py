## Advent of Code 2018: Day 6
## https://adventofcode.com/2018/day/6
## Jesse Williams
## Answers: [Part 1]: , [Part 2]:

import re, pickle
import numpy as np
import matplotlib.pyplot as plt

def voronoiStep(coordMatrix, coordDict):
    # Takes a matrix and expands each entry in all Manhattan directions, clearing the entry if a collision is found(?)
    allStepCoords = []  # keeps track of all coords added so far this step to check for collisions
    collisions = []
    for label in coordDict:
        newCoords = []
        for (x, y) in coordDict[label]:
            step_EW = [x-1, x+1]
            step_NS = [y-1, y+1]
            for m in step_EW:
                if (m, y) in allStepCoords:
                    collisions.append((m, y))
                elif (m, y) not in coordDict[label] and (m, y) not in newCoords:
                    newCoords.append((m, y))
                    # Check if this new coord is inside any other areas. If so, remove it.
                    for otherLabel in coordDict:
                        if otherLabel == label: continue
                        if (m, y) in coordDict[otherLabel]:
                            newCoords.remove((m, y))

            for n in step_NS:
                if (x, n) in allStepCoords:
                    collisions.append((x, n))
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
            if (x, y) in collisions:
                coordMatrix[x, y] = 0
            else:
                coordMatrix[x, y] = label
    return coordMatrix, coordDict

def voronoiFinished(coordMatrix):
    # Finished when no -1's remain
    if (-1 in list(coordMatrix.flatten())):
        return False
    else:
        return True

def createCoordMatrix(seedCoordList):
    # Find size of box
    SE_padding = 50
    X, Y = 0, 0
    for (x, y) in seedCoordList:
        if x > X: X = x
        if y > Y: Y = y

    # Initialize array
    size = max([X+SE_padding, Y+SE_padding])  # make a square grid SE_padding px larger than the largest coordinate
    matrix = np.zeros((size, size))
    matrix.fill(-1)

    # Insert seed coords
    coordDict = {}
    label = 1
    for (x, y) in seedCoordList:
        matrix[x, y] = label
        label += 1
        coordDict[label] = [(x, y)]

    return matrix, coordDict

def expandMatrix(matrix, scale):
    # Expands a matrix by a given (int) scale for rendering
    if scale == 1: return matrix
    (m, n) = matrix.shape
    matrix = np.repeat(matrix, scale, axis=0)
    matrix = np.repeat(matrix, scale, axis=1).reshape(scale*m, scale*n)
    return matrix

def initializeRender(coordMatrix, scale):
    dpi = 80
    margin = 0.05  # % of the width/height of the figure

    plt.ion()
    plt.axis('off')
    plt.tight_layout()

    coordMatrix = expandMatrix(coordMatrix, scale)
    xpixels, ypixels = coordMatrix.shape

    fig = plt.figure(figsize=(ypixels/dpi, xpixels/dpi), dpi=dpi)
    return fig

frame = 1
def updateRender(coordMatrix, scale, fig, realtime=True):
    colors = 'hot'
    coordMatrix = expandMatrix(coordMatrix, scale)
    fig.figimage(coordMatrix, cmap=colors)
    if realtime:
        fig.canvas.draw()
        fig.canvas.flush_events()
    global frame
    plt.savefig('img/voronoi_frame{}.png'.format(frame))
    frame += 1


if __name__ == "__main__":

    try:
        with open('day6_matrix.p', 'rb') as f_matrix:
            coordMatrix = pickle.load(f_matrix)
        with open('day6_dict.p', 'rb') as f_dict:
            coordDict = pickle.load(f_dict)
    except:
        coordList = []
        with open('day6_input.txt') as f:
            pattern = re.compile(r"(\d+),\s(\d+)")
            while True:
                line = f.readline()
                if line == '': break
                matches = pattern.match(line)
                coordList.append(tuple([int(i) for i in matches.groups()]))
        coordMatrix, coordDict = createCoordMatrix(coordList)

    scale = 1
    fig = initializeRender(coordMatrix, scale)
    done = False
    i = 0
    updateRender(coordMatrix, scale, fig, realtime=False)
    while not done:
        i += 1
        coordMatrix, coordDict = voronoiStep(coordMatrix, coordDict)
        updateRender(coordMatrix, scale, fig, realtime=False)

        with open('day6_matrix.p', 'wb') as f_matrix:
            pickle.dump(coordMatrix, f_matrix)
        with open('day6_dict.p', 'wb') as f_dict:
            pickle.dump(coordDict, f_dict)

        if voronoiFinished(coordMatrix):
            done = True
