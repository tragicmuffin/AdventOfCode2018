## Advent of Code 2018: Day 7
## https://adventofcode.com/2018/day/7
## Jesse Williams
## Answers: [Part 1]: BITRAQVSGUWKXYHMZPOCDLJNFE, [Part 2]: 869

import re, string

def timer(step):
    # Calculates the amount of time a step will take to complete
    t = list(string.ascii_uppercase).index(step) + 1
    return (60 + t)

def decrementTimers(steps):
    decSteps = []
    for step in steps:
        decSteps.append( (step[0], step[1]-1) )
    return decSteps

if __name__ == "__main__":
    # These tuples have the form (prerequisite, result)
    allSteps = []
    stepOrder = []

    with open('day7_input.txt') as f:
        line = f.readline()
        while line:
            pattern = re.compile(r"Step (\w) must be finished before step (\w) can begin.")
            matches = pattern.match(line)
            allSteps.append(matches.groups())  # add step to list

            line = f.readline()

    ## Part 1
    allStepsLeft = allSteps.copy()
    done = False
    while not done:
        # Phase 1: Search for all steps that have no prereqs. Then take lowest alphebetical step.
        rootSteps = []  # a list of all steps with no prerequisites
        resultSteps = set([step[1] for step in allStepsLeft])  # pull out all result step letters
        for step in allStepsLeft:
            if step[0] not in resultSteps and step[0] not in rootSteps:
                rootSteps.append(step[0])

        stepTaken = min(rootSteps)
        stepOrder.append(stepTaken)

        # Phase 2: Remove any step with a prereq of the step last taken, since that prereq has now been filled.
        if len(allStepsLeft) == 1:
            stepOrder.append(allStepsLeft[0][1])  # add last step
            done = True
        else:
            allStepsLeft = [step for step in allStepsLeft if (step[0] != stepTaken)]

    print('\nThe correct step order is {}.'.format(''.join(stepOrder)))

    ## Part 2
    allStepsLeft = allSteps.copy()

    NUM_WORKERS = 5
    stepsActive = []  # holds tuples (step, timer) tracking the amount of time left to complete a given step

    second = 0
    while True:

        # Check if any timers have run out. If so, remove step from active list and from allStepsLeft list.
        stepsToRemove = []
        for stepAndTime in stepsActive:
            if (stepAndTime[1] == 0):
                stepsToRemove.append(stepAndTime)
                # Check here to determine if there is only one prereq left, in which case that prereq's results will be the remaining root steps.
                # However, if any steps have '.' in them, we've already handled the last step, so proceed normally.
                if len(set([step[0] for step in allStepsLeft])) == 1 and ('.' not in [step[1] for step in allStepsLeft]):
                    allStepsLeft = [(step[1], '.') for step in allStepsLeft]  # make a pseudo step list to force last step(s) into roots
                else:
                    allStepsLeft = [step for step in allStepsLeft if (step[0] != stepAndTime[0])]
        for s in stepsToRemove: stepsActive.remove(s)

        # If we've just removed the last step, we're done
        if len(allStepsLeft) == 0:
            break

        # Get all root steps
        rootSteps = []  # a list of all steps with no prerequisites
        resultSteps = set([step[1] for step in allStepsLeft])  # pull out all result step letters
        for step in allStepsLeft:
            if step[0] not in resultSteps and step[0] not in rootSteps:
                rootSteps.append(step[0])

        # Walk through the root steps, in alpha order, starting tasks for any available workers
        for step in sorted(rootSteps):
            if len(stepsActive) < NUM_WORKERS and step not in [s[0] for s in stepsActive]:  # check if there's an available worker, and if this step is already in progress
                stepsActive.append( (step, timer(step)) )

        stepsActive = decrementTimers(stepsActive)  # decrement timers on all active steps
        second += 1

    print('\nIt takes {} seconds for {} workers to complete all steps.'.format(second, NUM_WORKERS))
