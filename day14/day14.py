## Advent of Code 2018: Day 14
## https://adventofcode.com/2018/day/14
## Jesse Williams
## Answers: [Part 1]: 8176111038, [Part 2]: 20225578

INPUT = 890691


def createNewRecipes(recipes, elves):
    newRcpSum = recipes[elves[0]] + recipes[elves[1]]  # add current recipes together
    newRcpDigits = list(map(int, list(str(newRcpSum))))  # separate digits into a list
    return newRcpDigits

def chooseNewCurrentRecipes(recipes, elves):
    newElves = [0, 0]
    for i, elf in enumerate(elves):
        newElves[i] = (elves[i] + (1 + recipes[elves[i]])) % len(recipes)
    return newElves

if __name__ == "__main__":
    ## Part 1
    recipes = [3, 7]
    elves = [0, 1]  # stores the index of the current recipe for each elf

    numRecipes = INPUT
    numRecipesMade = 0
    numExtraRecipes = 10
    while numRecipesMade < numRecipes + numExtraRecipes:
        newRecipes = createNewRecipes(recipes, elves)  # create new recipes and add them to the end of the list
        recipes += newRecipes
        elves = chooseNewCurrentRecipes(recipes, elves)  # update the current recipe for each elf
        numRecipesMade += len(newRecipes)

    extraRecipes = recipes[numRecipes:numRecipes+numExtraRecipes]

    print('The next {} recipes after an initial {} are: {}'.format(numExtraRecipes, numRecipes, ''.join(map(str, extraRecipes))))

    ## Part 2
    # Since adding two single digit numbers together can result in either a 1- or 2-digit number, we check both possibilities
    recipes = [3, 7]
    elves = [0, 1]  # stores the index of the current recipe for each elf

    done = False
    targetSequenceInt = INPUT
    targetSequence = list(map(int, list(str(targetSequenceInt))))
    while not done:
        recipes += createNewRecipes(recipes, elves)  # create new recipes and add them to the end of the list
        elves = chooseNewCurrentRecipes(recipes, elves)  # update the current recipe for each elf

        if (recipes[-len(targetSequence):] == targetSequence):
            recipesToLeft = len(recipes[:-len(targetSequence)])
            done = True
        elif (recipes[-len(targetSequence)-1:-1] == targetSequence):
            recipesToLeft = len(recipes[:-len(targetSequence)-1])
            done = True

    print("There are {} recipes to the left of the first instance of the sequence '{}'.".format(recipesToLeft, targetSequenceInt))
