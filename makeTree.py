import argparse
import os
import shutil
import glob
import formula
import json

tmp = 'trees/tmp/'

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

    if os.path.exists(args.treeDirPath):
        if os.path.exists(tmp):
            shutil.rmtree(tmp)
        os.makedirs(tmp)
        for file in glob.glob('*', root_dir=args.treeDirPath):
            os.rename(args.treeDirPath + file, tmp + file)
        print('Directory already exists, existing files moved to ' + tmp)
    else:
        os.makedirs(args.treeDirPath)

    with open(args.treeDirPath + 'base.json', 'w') as base:
        base.write('''"''' + args.letter + '''"''')
    rule_json = json.loads(tree.to_json())
    with open(args.treeDirPath + args.letter + '.json', 'w') as rule:
        rule.write(json.dumps(rule_json, indent=4))
    print(tree)
