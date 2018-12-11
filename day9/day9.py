## Advent of Code 2018: Day 9
## https://adventofcode.com/2018/day/9
## Jesse Williams
## Answers: [Part 1]: 375465, [Part 2]: 3037741441

import re

def playGame(NUM_PLAYERS, NUM_MARBLES):
    players = [0]*NUM_PLAYERS
    currentPlayer = 0
    currentMarble = 0  # position of the "current marble"

    # Turn 0
    circle = [0]

    # Turn 1
    currentPlayer = 0
    circle.append(1)
    currentMarble = 1

    # Turn n
    print('\nStarting a game with {} marbles...'.format(NUM_MARBLES))
    for n in range(2, NUM_MARBLES):
        currentPlayer = (currentPlayer + 1) % NUM_PLAYERS

        if n % 23 == 0:
            players[currentPlayer] += n
            idx = (currentMarble - 7) % len(circle)
            players[currentPlayer] += circle[idx]
            circle.pop(idx)
            if idx < len(circle)-1:
                currentMarble = idx
            else:
                currentMarble = 0
        else:
            idx = (currentMarble + 2) % len(circle)
            circle.insert(idx, n)
            currentMarble = idx

        if n % 10000 == 0:
            print('Played {} turns...'.format(n))


    return players

if __name__ == '__main__':
    pattern = re.compile(r"(\d+) players; last marble is worth (\d+) points")
    with open('day9_input.txt') as f:
        matches = pattern.match(f.read())
        NUM_PLAYERS = int(matches.groups()[0])
        NUM_MARBLES = int(matches.groups()[1])

    ## Part 1
    result = playGame(NUM_PLAYERS, NUM_MARBLES)
    highScore = max(result)
    print('Game finished. The highest scoring Elf in this game is #{} with a score of {}.\n'.format(result.index(highScore)+1, highScore))

    ## Part 2
    result = playGame(NUM_PLAYERS, NUM_MARBLES*100)
    highScore = max(result)
    print('Game finished. The highest scoring Elf in this game is #{} with a score of {}.\n'.format(result.index(highScore)+1, highScore))
