## Advent of Code 2018: Day 10
## https://adventofcode.com/2018/day/10
## Jesse Williams
## Answers: [Part 1]: EJZEAAPE, [Part 2]: 10054

import re
from PIL import Image

def createImage(targetBox, imgNum, lights):
    # PIL indexes images as Image[columns, rows]
    imgSizeX = targetBox[1] - targetBox[0]
    imgSizeY = targetBox[3] - targetBox[2]

    img = Image.new('1', (imgSizeX, imgSizeY), 1)  # create a white (color=1) image ('1' is 1-bit bitmap mode)
    pixels = img.load()  # initialize the pixel map

    # Shift the origin of the light coords to the center of the image
    shiftX = -targetBox[0]
    shiftY = -targetBox[2]

    for light in lights:
        pixels[light[0]+shiftX, light[1]+shiftY] = 0  # set pixel to black

    img.save('img/day10_{}.bmp'.format(imgNum))


def fitsTargetBox(lights, targetSizeX, targetSizeY):
    # Determine whether all lights fit within the target size box
    lightsXs = [light[0] for light in lights]
    lightsYs = [light[1] for light in lights]

    rangeX = max(lightsXs) - min(lightsXs)
    rangeY = max(lightsYs) - min(lightsYs)

    if rangeX < targetSizeX and rangeY < targetSizeY:
        Xm = min(lightsXs)
        if Xm % 2 != 0: Xm -= 1
        XM = max(lightsXs)
        if XM % 2 != 0: XM += 1

        Ym = min(lightsYs)
        if Ym % 2 != 0: Ym -= 1
        YM = max(lightsYs)
        if YM % 2 != 0: YM += 1

        return (Xm, XM, Ym, YM)  # returns a bounding box for the current lights
    else:
        return False


def insideTargetBox(lights, targetBox):
    lightsXs = [light[0] for light in lights]
    lightsYs = [light[1] for light in lights]

    if min(lightsXs) >= targetBox[0] and max(lightsXs) <= targetBox[1] and min(lightsYs) >= targetBox[2] and max(lightsYs) <= targetBox[3]:
        return True
    else:
        return False


if __name__ == '__main__':
    imgNum = 0
    lights = []

    with open('day10_input.txt') as f:
        pattern = re.compile(r"position=<\s*([\-]*\d+),\s+([\-]*\d+)> velocity=<\s*([\-]*\d+),\s+([\-]*\d+)>")
        line = f.readline()
        while line:
            matches = pattern.match(line)
            (posX, posY, velX, velY) = matches.groups()  # Positive X direction is right, positive Y direction is down
            lights.append([int(posX), int(posY), int(velX), int(velY)])
            line = f.readline()

    ## Part 1
    t = 0
    targetSizeX, targetSizeY = 600, 400

    # This first loop will run until all lights fall inside a box
    while not fitsTargetBox(lights, targetSizeX, targetSizeY):
        # Advance lights
        for idx, light in enumerate(lights):
            lights[idx][0] += light[2]
            lights[idx][1] += light[3]
        t += 1

        if t > 100000: # failsafe
            break

    # This second loop will continue until lights fall outside of the fixed bounding box
    targetBox = fitsTargetBox(lights, targetSizeX, targetSizeY)  # get bounding box
    while insideTargetBox(lights, targetBox):

        # Start capturing images when all lights fit within a target size box
        createImage(targetBox, imgNum, lights)
        imgNum += 1

        # Advance lights
        for idx, light in enumerate(lights):
            lights[idx][0] += light[2]
            lights[idx][1] += light[3]
        t += 1

        if t > 100000: # failsafe
            break

    print('Finished after {} timesteps, capturing {} images.'.format(t-1, imgNum))

    ## Part 2
    # Part 1 finished in 10092 timesteps, and the message appeared in the 40th image out of 78 images taken, thus it took 10092-(78-40) = 10054 seconds to appear
