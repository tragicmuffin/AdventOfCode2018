import string

def react(pair):
    # Receives a pair of units in a list and returns T if there is a reaction, F otherwise.
    if (pair[0].lower() == pair[1].lower() and pair[0] != pair[1]):
        return True  # if the units are the same letter but different case
    else:
        return False

def applyReactions(polymer):
      
      i = 0
      reactions = 0
      # Move through polymer, applying reactions, and find the reduced chain.
      while (i < len(polymer)-1):
          # Pass the next unit pair in the sliding window into react
          if (react(polymer[i:i+2])):
              # If there was a reaction, pop these elements out of list, and back the window up to check for any chained reactions
              polymer.pop(i)
              polymer.pop(i)
              i -= 1
              reactions += 1
              if (i < 0): i = 0  # in case we get to the start of the list and underflow
          else:
              # If there was no reaction, slide the window forward and continue.
              i += 1
              
      
    
if __name__ == "__main__":
    # Capture the input unit stream as a string, then convert to list
    with open('input.txt') as f:
        polymerUnreacted = f.read()
    polymerUnreacted = list(polymerUnreacted)[:-1]  # cut off the \n element
    polymerUnreactedLength = len(polymerUnreacted)

    ## Part 1 ##
    polymerReacted = applyReactions(polymerUnreacted)
    print('The un-reacted polymer has a length of {}.'.format(polymerUnreactedLength))
    print('The fully-reacted polymer has a length of {} after {} reactions.\n'.format(len(polymerReacted), reactions))
    
    ## Part 2 ##
    # Check the fully-reacted length of all polymers with one unit type (letter) subtracted
    polymerReducedLengths = {}
    for badUnit in list(string.ascii_lowercase):

        polymerReduced = polymerUnreacted
        for idx in range(len(polymerReduced))[::-1]:  # step through all indices of polymer list backwards
            if polymerReduced[idx].lower() == badUnit:
                polymerReduced.pop(idx)  # remove any units with the current bad unit type (starts at end of list to avoid index misalignment)
        polymerReducedReacted = applyReactions(polymerReduced)
        polymerReducedLengths[badUnit] = len(polymerReducedReacted)
        print('Removing all {}/{} units, the fully-reacted polymer has a length of {}.'.format(badUnit, badUnit.upper(), len(polymerReducedReacted)))

    shortestReducedPolymer = list(filter(lambda x:x[1] == min(polymerReducedLengths.values()), polymerReducedLengths.items()))[0]
    print('\n')
