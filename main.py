from processNode import processNode
from jsonParser import load_tree
from subprocess import run
import argparse

# Args
parser = argparse.ArgumentParser(
        prog='Tree Generator',
        description='Displays and analyses a tree to a specified depth')
parser.add_argument('treeDirPath',
                    help='Tree directory')
parser.add_argument('processDepth',
                    help='Depth to generate', type=int)
parser.add_argument('-p', '--parentseq',
                    help='Parent seq toggle', action='store_true')
parser.add_argument('-no', '--nooutput',
                    help='Visual output toggle', action='store_true')
parser.add_argument('-fun', '--function',
                    help='Graphvis function to use', default='dot')
parser.add_argument('-fmt', '--format',
                    help='File format for output', default='png')
args = parser.parse_args()

treeDirPath = args.treeDirPath
processDepth = args.processDepth
graphFunction = args.function
fileFormat = args.format
output = not args.nooutput
printParents = args.parentseq

# Initialise tree
tree = load_tree(treeDirPath + "base.json")
nameCount = 1

# Take stock of node counts
overallSum = 0
sumList = []
rowList = []
parentList = []

# Expand nodes in tree
for i in range(processDepth):  # TODO: finite limits
    nodes = tree.filter_nodes(lambda node: tree.depth(node) == i)
    nodes = sorted(nodes, key=lambda node: node.identifier)
    nodeIds = [node.identifier for node in nodes]  # To avoid dict redef

    for nodeId in nodeIds:
        nameCount = processNode(tree, nodeId, nameCount, treeDirPath)

        # Form parentList
        if tree.parent(nodeId) is not None:
            parentList.append(tree.parent(nodeId).tag)

    rowList.append(len(nodeIds))
    overallSum += rowList[i]
    sumList.append(overallSum)

# Calculate ratios between successive rows
ratioList = [rowList[i + 1] / rowList[i]
             for i in range(len(rowList) - 1)]

# Number remaining nodes
nodes = tree.filter_nodes(lambda node: tree.depth(node) == processDepth)
nodes = sorted(nodes, key=lambda node: node.identifier)
for node in nodes:
    node.tag = nameCount
    nameCount += 1


# Clean up stragglers
nodes = tree.filter_nodes(lambda node: tree.depth(node) == processDepth + 1)
nodes = sorted(nodes, key=lambda node: node.identifier)
nodeIds = [node.identifier for node in nodes]  # To avoid dict redef

for nodeId in nodeIds:
    tree.remove_node(nodeId)


# Outputs
print("Cumulative sequence:")
print(sumList)
print("Row sequence:")
print(rowList)
print("Ratio sequence:")
print(ratioList)
if printParents:
    print("Parent sequence:")
    print(parentList)

if output:
    tree.to_graphviz("output/output.gv")
    run([graphFunction, "-T" + fileFormat, "-y", "output/output.gv", "-o", "output/output." + fileFormat])
