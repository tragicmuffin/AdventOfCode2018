## Advent of Code 2018: Day 3
## https://adventofcode.com/2018/day/3
## Jesse Williams
## Answers: [Part 1]: 111935, [Part 2]: 650

import pickle

cache = True

def parseClaim(claimStr):
    # Format: '#N @ X,Y: WxH'
    claim = claimStr.split()  # ['#N', '@', 'X,Y:', 'WxH']
    cl_id = claim[0][1:]
    cl_coords = claim[2].split(',')
    cl_coords = (int(cl_coords[0]), int(cl_coords[1][:-1]))
    cl_dims = claim[3].split('x')
    cl_dims = (int(cl_dims[0]), int(cl_dims[1]))

    return [cl_id, cl_coords, cl_dims]  # [N, (X,Y), (W,H)]

def doesClaimOccupy(claim, coords):
    if (claim[1][0] <= coords[0] < claim[1][0]+claim[2][0] and claim[1][1] <= coords[1] < claim[1][1]+claim[2][1]):
        return True
    else:
        return False

def numberOfClaims(allClaims, coords):
    num = 0
    for claim in allClaims:
        # Check whether each claim occupies the input coords
        if doesClaimOccupy(claim, coords):
            num += 1
    return num

def findSizeOfFabric(allClaims):
    W, H = 0, 0
    for claim in allClaims:
        w = claim[1][0] + claim[2][0]
        h = claim[1][1] + claim[2][1]
        if (w > W): W = w
        if (h > H): H = h
    return [W, H]

def claimsOverlap(claimA, claimB):
    # Tests if two claims overlap anywhere. Claim format: [N, (X,Y), (W,H)]
    claimA_coords, claimB_coords = [], []
    for y in range(claimA[1][1], claimA[1][1]+claimA[2][1]):
        for x in range(claimA[1][0], claimA[1][0]+claimA[2][0]):
            claimA_coords.append((x, y))  # collect all coords occupied by claimA
    for y in range(claimB[1][1], claimB[1][1]+claimB[2][1]):
        for x in range(claimB[1][0], claimB[1][0]+claimB[2][0]):
            claimB_coords.append((x, y))  # collect all coords occupied by claimB

    for coords in claimA_coords:
        if coords in claimB_coords:
            return True  # Overlap

    return False  # No overlap


if __name__ == "__main__":
    # Read input file of claims, parse them, and store them in a list
    allClaims = []
    with open('day3_input.txt') as f:
        while True:
            claimStr = f.readline()
            if claimStr == '': break
            allClaims.append(parseClaim(claimStr))

    [FABRIC_WIDTH, FABRIC_HEIGHT] = findSizeOfFabric(allClaims)

    # Read count list from cache if possible, else create it again.
    claimCountDict, coordsWithOneClaim = {}, []
    try:
        with open('day3_claimCountCache.txt', 'rb') as f:
            claimCountDict = pickle.load(f)
        print('Cache loaded.')
    except:
        # For each coord point on fabric, count how many claims occupy it.
        print('Cache not found.')

        for y in range(FABRIC_HEIGHT):
            print('Scanning row {}...'.format(y))
            for x in range(FABRIC_WIDTH):
                claimCount = numberOfClaims(allClaims, (x,y))
                claimCountDict[(x,y)] = claimCount
        if cache:
            with open('day3_claimCountCache.txt', 'wb') as f:
                pickle.dump(claimCountDict, f)

    # (Part 1) Scan through claim counts and count number of overlapping coords
    numDuplicateClaims = 0
    for coords in claimCountDict:
        if claimCountDict[coords] > 1:
            numDuplicateClaims += 1
    print('Found {} square inches on fabric with multiple claims.'.format(numDuplicateClaims))

    # (Part 2) Scan through all claim pairs
    for idx, claimA in enumerate(allClaims):
        print('Checking claim #{}...'.format(claimA[0]))
        noOverlapsFlag = True
        for claimB in allClaims[:idx]+allClaims[idx+1:]:
            if claimsOverlap(claimA, claimB):  # if we find an overlap, set flag and skip the rest of the comparisons for this claimA
                noOverlapsFlag = False
                break
        if noOverlapsFlag == True:  # if this flag is still true, there were no overlaps found, and we must have the claim we're looking for
            print('Found claim with no overlap: #{}'.format(claimA[0]))
            break
