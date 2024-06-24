from jsonParser import load_tree
from glob import glob


# Expansion function pointers
def generateNodeDict(treeDirPath):
    global nodeList
    # [-6] extracts the ? letter
    nodeList = [file[-6] for file in glob(treeDirPath + "/?.json")]


nodeList = None


# Expansion rules
def processNode(tree, nodeId, nameCount, treeDirPath):
    node = tree.get_node(nodeId)

    if nodeList is None:
        generateNodeDict(treeDirPath)

    if node.tag in nodeList:
        load_tree(treeDirPath + node.tag + ".json", tree, tree.get_node(nodeId))
    elif node.tag != 'O':
        return nameCount  # Don't touch untagged nodes

    node.tag = nameCount
    return nameCount + 1
