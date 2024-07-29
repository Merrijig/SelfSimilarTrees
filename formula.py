import roman
from uuid import uuid4
from treelib import Tree


def base(numeral, ref_letter):
    global glob_count
    tree = Tree()
    length = roman.to_num(numeral)

    new_id = uuid4()
    tree.create_node(tag="O",
                     identifier=new_id,
                     parent=None)
    parent = tree.get_node(new_id)

    for i in range(length - 1):
        new_id = uuid4()
        tree.create_node(tag="O",
                         identifier=new_id,
                         parent=parent)
        parent = tree.get_node(new_id)

    # Allow for stub trees
    if length >= 1:
        tree.create_node(tag=ref_letter,
                         identifier=uuid4(),
                         parent=parent)

    return tree


def vee(tree1, tree2):
    tree1.merge(tree1.root, tree2)
    return tree1


def plus(tree1, tree2, ref_letter):
    for leaf in tree1.leaves():
        if leaf.tag != ref_letter:
            continue

        # Change ids to avoid repetition
        for node in tree2.all_nodes():
            tree2.update_node(node.identifier, identifier=uuid4())

        leaf.tag = "O"
        tree1.merge(leaf.identifier, tree2)

    return tree1


def get_sub_exp(formula):
    brac_count = 0
    for i, letter in enumerate(formula):
        if letter == '(':
            brac_count += 1
        elif letter == ')':
            brac_count -= 1

        if brac_count <= 0:
            return i

    print("ERROR: Brackets unterminated")  # TODO: Better error handling
    return False


def interpret(formula, ref_letter):
    exp1 = get_sub_exp(formula)
    if exp1 is False:
        return False

    # More than one exp present; break down recursively
    if exp1 != 0:
        char = formula[exp1 + 1]
        if char == 'v':
            return vee(interpret(formula[1:exp1], ref_letter),
                       interpret(formula[exp1 + 3:-1], ref_letter))
        elif char == '+':
            return plus(interpret(formula[1:exp1], ref_letter),
                        interpret(formula[exp1 + 3:-1], ref_letter),
                        ref_letter)
        else:
            print("weird weird weird weird")
            return False

    # Base case
    return base(formula, ref_letter)


def generate(tree):
    pass
