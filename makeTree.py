import argparse
import os
import formula

parser = argparse.ArgumentParser(
        prog='makeTree.py',
        description='Simple tree creation utility for treeGen.py')

parser.add_argument('treeFormula',
                    help='Formula from which to construct tree')
parser.add_argument('treeDirPath', nargs='?',
                    help='Path for tree directory', default='trees/curr/')
parser.add_argument('-l', '--letter',
                    help='Letter name for recursive node', default='X')

if __name__ == '__main__':
    args = parser.parse_args()
    tree = formula.interpret(args.treeFormula, args.letter)

    try:
        os.makedirs(args.treeDirPath)
    except FileExistsError:
        # TODO: MOVE FILES
        # print('Directory already exists, existing files moved to trees/tmp')
        pass

    with open(args.treeDirPath + 'base.json', 'w') as base:
        base.write('''"''' + args.letter + '''"''')
    with open(args.treeDirPath + args.letter + '.json', 'w') as rule:
        rule.write(tree.to_json())
    print(tree)
