from treelib import Tree
from processNode import processNode

tree = Tree()
tree.create_node("I", '1')
processNode(tree, '1', 1)

with open("trees/fibTree/I.json", "w") as f:
    f.write(tree.to_json())
