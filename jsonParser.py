import json
from uuid import uuid4
from treelib import Tree

tree_dict = {}


# Wrapper function for loading pre-existing (base) tree
def load_tree(file_path, tree=None, parent=None):
    # Make a NEW default tree every time (as opposed to inline syntax)
    if not tree:
        tree = Tree()
    # Don't load the file every time
    if file_path in tree_dict:
        json_tree = tree_dict[file_path]
    else:
        with open(file_path) as f:
            json_tree = json.load(f)
            tree_dict[file_path] = json_tree

    instantiate_subtree(json_tree, tree, parent)

    return tree


# Recursive function call for tree loading
def instantiate_subtree(json_tree, tree, parent=None):
    # Case where only one node is in tree
    if isinstance(json_tree, str):
        tree.create_node(tag=json_tree, identifier=uuid4(), parent=parent)
        return

    k, value = list(json_tree.items())[0]

    # Create root
    if parent is None:
        new_id = uuid4()
        tree.create_node(tag=str(k), identifier=new_id)
        parent = tree.get_node(new_id)

    for counter, value in enumerate(json_tree[k]['children']):
        # Base case
        if isinstance(json_tree[k]['children'][counter], str):
            tree.create_node(tag=value,
                             identifier=uuid4(),
                             parent=parent)
        # Recursive Case
        else:
            new_id = uuid4()
            tree.create_node(tag=list(value)[0],
                             identifier=new_id,
                             parent=parent)
            instantiate_subtree(json_tree[k]['children'][counter],
                                tree,
                                tree.get_node(new_id))
