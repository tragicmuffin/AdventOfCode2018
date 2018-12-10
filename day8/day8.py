## Advent of Code 2018: Day 8
## https://adventofcode.com/2018/day/8
## Jesse Williams
## Answers: [Part 1]: 36566, [Part 2]: 30548

class Node(object):
    def __init__(self, chs, mds):
        self.header = (chs, mds)  # number of child nodes and metadata entries as specified in the node header
        self.childNodes = []      # list of all child nodes (instances of Node class)
        self.metadataList = []    # list of metadata entries (ints)

    def getMetadataSum(self):
        # Returns the sum of all metadata in this node and all child nodes.
        Sum = 0
        for node in self.childNodes:
            Sum += node.getMetadataSum()
        Sum += sum(self.metadataList)
        return Sum

    def getNodeValue(self):
        value = 0
        children = self.header[0]
        if children == 0:  # no child nodes
            return sum(self.metadataList)
        else:
            for mdEntry in self.metadataList:
                if (0 < mdEntry <= children):  # (if mdEntry > children or mdEntry == 0, nothing is added to the value)
                    value += self.childNodes[mdEntry-1].getNodeValue()
        return value


def readNode(tree, ptr, n):
    newNodes = []
    for _ in range(n):
        (children, metadata) = (tree[ptr], tree[ptr+1])
        newNode = Node(children, metadata)
        ptr += 2

        newChildNodes, ptr = readNode(tree, ptr, children)  # if there were no children, loop inside this function will pass
        newNode.childNodes += newChildNodes

        # At the end of each iteration (after we return from any recursion), read the metadata at the end of the node.
        newNode.metadataList = tree[ptr : ptr+metadata]
        ptr += metadata

        newNodes.append(newNode)
    return newNodes, ptr


if __name__ == "__main__":
    with open('day8_input.txt') as f:
        treeStr = f.read()
        tree = [int(s) for s in treeStr.split()]

    # Start the recursive chain with the pointer at 0 and the number of children at 1 (the root node).
    # The main call to this function will return the root node object with all other child nodes nested inside.
    rootNode = readNode(tree, 0, 1)[0][0]

    ## Part 1
    print('\nThe sum of all metadata entries in the tree is {}.'.format(rootNode.getMetadataSum()))

    ## Part 2
    print('\nThe "value" of the root node is {}.'.format(rootNode.getNodeValue()))
