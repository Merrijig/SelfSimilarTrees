import json
from treelib import Tree

tree_dict = {}


# Wrapper function for loading pre-existing (base) tree
def load_tree(file_path, tree=Tree(), parent=None):
    # Don't load the file every time
    if file_path in tree_dict:
        json_tree = tree_dict[file_path]
    else:
        with open(file_path) as f:
            json_tree = json.load(f)
            tree_dict[file_path] = json_tree

    recurse_tree(json_tree, tree, parent)

    return tree


# Recursive function call for tree loading
def recurse_tree(json_tree, tree, parent=None):
    # Case where only one node is in tree
    if isinstance(json_tree, str):
        tree.create_node(tag=json_tree, identifier=chr(1), parent=parent)
        return

    k, value = list(json_tree.items())[0]

    # Create root
    if parent is None:
        tree.create_node(tag=str(k), identifier=chr(1))
        parent = tree.get_node(chr(1))

    for counter, value in enumerate(json_tree[k]['children']):
        # Base case
        if isinstance(json_tree[k]['children'][counter], str):
            tree.create_node(tag=value,
                             identifier=parent.identifier + chr(counter + 1),
                             parent=parent)
        # Recursive Case
        else:
            tree.create_node(tag=list(value)[0],
                             identifier=parent.identifier + chr(counter + 1),
                             parent=parent)
            recurse_tree(json_tree[k]['children'][counter],
                         tree,
                         tree.get_node(parent.identifier + chr(counter + 1)))
