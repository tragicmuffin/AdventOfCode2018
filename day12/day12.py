## Advent of Code 2018: Day 12
## https://adventofcode.com/2018/day/12
## Jesse Williams
## Answers: [Part 1]: 3059, [Part 2]: 3650000001776

import re, time, math

def maskHash(pots):
    hash = 0
    exp = 4
    for char in pots:
        if char == '#':
            hash += 2**exp
        exp -= 1
    return hash

def advanceGeneration(state, rules):
    nextState = '..'
    for idx in range(2, len(state)-2):
        pots = state[idx-2:idx+3]  # capture 5 pots around the current pot
        hash = maskHash(pots)  # hash the 5-pot state to compare to a rule
        if rules[hash] == 1:
            nextState += '#'
        else:
            nextState += '.'
    nextState += '..'
    return nextState

def shiftState(state):
    # Find average index of living plant cluster
    low = state.find('#')
    high = state.rfind('#')
    avg = int((high+low)/2)
    if avg > int(len(state)/2):
        # Shift right
        shift = avg - int(len(state)/2)  # calculate shift amount
        state = state[shift:] + '.'*shift
        return state, shift

    else:
        return state, 0


if __name__ == "__main__":
    rulesStr = []

    with open('day12_input.txt') as f:
        pattern = re.compile(r"initial state: (.*)")
        initialStateStr = f.readline()
        matches = pattern.match(initialStateStr)
        initialState = matches.groups()[0]

        _ = f.readline()
        rule = f.readline()
        while rule:
            rulesStr.append(rule[:-1])
            rule = f.readline()

    # We define a 5-bit mask where '.'=0 and '#'=1 and create a list of dict entries {s: r} where s is the 5-bit state (as an int) and r is the 1-bit result.
    rules = {}
    for rule in rulesStr:
        ruleState = maskHash(rule[0:5])

        if rule[9] == '#': ruleResult = 1
        else: ruleResult = 0

        rules[ruleState] = ruleResult

        for n in range(32):  # if there are any undefined rules, define them as '.'=0
            if n not in rules:
                rules[n] = 0

    ## Part 1
    # Extend initial state string arbitrarily in both directions. We only need to know this offest when calculating sums of pot numbers.
    offsetStr = '.'*int(len(initialState)/2)
    offset = len(offsetStr)
    state = offsetStr + initialState + offsetStr

    print('\n')
    generations = 20
    for _ in range(generations):
        print(state)
        state = advanceGeneration(state, rules)

    # Find sum of all occupied pot numbers
    potSum = 0
    for i, pot in enumerate(state):
        if pot == '#':
            potSum += i - offset

    print('\nThe sum of the numbers of all pots is {}\n\n'.format(potSum))


    ## Part 2
    # This system stabilizes into a fixed pattern at generation 125, with all plants shifting 1 pot to the right on each subsequent generation.
    # Thus, measuring the sum of all pot numbers on generation 125, we only need to find the number of living plants N and add N*(500000000000-125) to that sum.

    # Extend initial state string arbitrarily in both directions. We only need to know this offest when calculating sums of pot numbers.
    t_s = time.time()

    offsetStr = '.'*int(len(initialState)/2)
    offset = len(offsetStr)
    state = offsetStr + initialState + offsetStr

    totalShift = 0
    targetGenerations = 50000000000
    generations = 125
    for gen in range(generations):
        if gen % 1 == 0:
            t_e = time.time() - t_s
            #print('[{}]{}  |  G: {}  (T+{} s)'.format(totalShift, state, gen, math.floor(t_e)))
        state = advanceGeneration(state, rules)

        state, shift = shiftState(state)  # shifts list to follow living plants
        totalShift += shift

    # Find sum of all occupied pot numbers, and also count the number of active pots
    potSum = 0
    potCount = 0
    for i, pot in enumerate(state):
        if pot == '#':
            potSum += i - offset + totalShift
            potCount += 1
    shiftedPotSum = potSum + potCount*(targetGenerations-generations)

    t_e = time.time() - t_s
    print('\nThe sum of the numbers of all pots is {}. (Took {} seconds)'.format(shiftedPotSum, math.floor(t_e)))
