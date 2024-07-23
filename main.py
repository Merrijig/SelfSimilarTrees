import argparse
import numpy as np
from tabulate import tabulate
from processNode import processNode
from jsonParser import load_tree
from subprocess import run
from treeData import TreeData
from format import print_title

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
parser.add_argument('-v', '--vis',
                    help='Visual output toggle', action='store_true')
parser.add_argument('-r', '--extrarowdata',
                    help='Extra row data toggle', action='store_true')
parser.add_argument('-nc', '--nocumsum',
                    help='Cumulative sum toggle', action='store_true')
parser.add_argument('-nr', '--norows',
                    help='Row sum toggle', action='store_true')
parser.add_argument('-am', '--arithmean',
                    help='Arithmetic mean ratio toggle', action='store_true')
parser.add_argument('-gm', '--geommean',
                    help='Geometric mean ratio toggle', action='store_true')
parser.add_argument('-nra', '--noratio',
                    help='Row ratio toggle', action='store_true')
parser.add_argument('-fun', '--function',
                    help='Graphvis function to use', default='dot')
parser.add_argument('-isf', '--intsf',
                    help='Sig figs for integer values', default='8')
parser.add_argument('-fdp', '--floatdp',
                    help='Decimal places for float values', default='10')
parser.add_argument('-fmt', '--format',
                    help='File format for output', default='png')
args = parser.parse_args()

max_trust = 15

treeDirPath = args.treeDirPath
processDepth = args.processDepth
float_format = f".{args.floatdp}f"
int_format = f".{args.intsf}g"

# Take stock of node counts
overall_sum = 0

# Quantities for table
table = {"Row Sums": []}
if not args.nocumsum:
    table["Cumulative Sums"] = []
if args.parentseq:
    parent_list = []

# Expand nodes in tree when neccesary
if args.vis or args.parentseq:
    # Initialise tree
    tree = load_tree(treeDirPath + "base.json")
    nameCount = 1
    for i in range(processDepth):  # TODO: finite limits
        nodes = tree.filter_nodes(lambda node: tree.depth(node) == i)
        nodes = sorted(nodes, key=lambda node: node.identifier)
        nodeIds = [node.identifier for node in nodes]  # To avoid dict redef

        for nodeId in nodeIds:
            nameCount = processNode(tree, nodeId, nameCount, treeDirPath)

            # Form parent_list
            if args.parentseq and tree.parent(nodeId) is not None:
                parent_list.append(tree.parent(nodeId).tag)

        table["Row Sums"].append(len(nodeIds))
        overall_sum += table["Row Sums"][i]
        if "Cumulative Sums" in table:
            table["Cumulative Sums"].append(overall_sum)

        # Number remaining nodes
        nodes = tree.filter_nodes(lambda node:
                                  tree.depth(node) == processDepth)
        nodes = sorted(nodes, key=lambda node: node.identifier)
        for node in nodes:
            node.tag = nameCount
        nameCount += 1

        # Clean up stragglers
        nodes = tree.filter_nodes(lambda node:
                                  tree.depth(node) == processDepth + 1)
        nodes = sorted(nodes, key=lambda node: node.identifier)
        nodeIds = [node.identifier for node in nodes]  # To avoid dict redef

        for nodeId in nodeIds:
            tree.remove_node(nodeId)
else:
    # Use rules-based numeric expansion in linear time (wrt depth)
    treeData = TreeData(processDepth, treeDirPath)
    treeData.process_rows()
    row_data = treeData.get_row_data()

    # Analyse
    for row in row_data:
        sum = 0
        for node_type, num in row.items():
            sum += num
        table["Row Sums"].append(sum)

    if "Cumulative Sums" in table:
        table["Cumulative Sums"].append(table["Row Sums"][0])
        for row in table["Row Sums"][1:]:
            table["Cumulative Sums"].append(table["Cumulative Sums"][-1] + row)


# Calculate ratios between successive rows
table["Row Ratios"] = [table["Row Sums"][i + 1] / table["Row Sums"][i]
                       for i in range(len(table["Row Sums"]) - 1)]
table["Row Ratios"].insert(0, "inf")
if args.arithmean:
    table["Ratio Avg (Arith)"] = [table["Row Ratios"][1]]
    for i, row_ratio in enumerate(table["Row Ratios"][2:], 1):
        table["Ratio Avg (Arith)"].append(((table["Ratio Avg (Arith)"][i - 1] * i)
                                           + float(row_ratio))
                                          / (i + 1))
    table["Ratio Avg (Arith)"].insert(0, "inf")
if args.geommean:
    table["Ratio Avg (Geom)"] = [table["Row Ratios"][1]]
    for i, row_ratio in enumerate(table["Row Ratios"][2:], 1):
        # Use logs to avoid overflow
        mean = np.exp((np.log(table["Ratio Avg (Geom)"][i - 1]) * i
                       + np.log(float(row_ratio)))
                      / (i + 1))
        table["Ratio Avg (Geom)"].append(mean)
    table["Ratio Avg (Geom)"].insert(0, "inf")


# Outputs
if args.norows:
    del table["Row Sums"]
if args.noratio:
    del table["Row Ratios"]
print_title("BASIC ROW DATA")
print(tabulate(table, headers="keys", floatfmt=float_format, intfmt=int_format))
if args.extrarowdata:
    print_title("TYPES OF NODE IN EACH ROW")
    print(tabulate(row_data, headers="keys", intfmt=int_format))
if args.parentseq:
    print("Parent sequence:")
    print(parent_list)
if int(args.floatdp) > max_trust:
    print_title("WARNING")
    print(f"Floating point arithmetic can not be trusted past {max_trust} d.p.")

if args.vis:
    tree.to_graphviz("output/output.gv")
    run([args.function, "-T" + args.format, "-y", "output/output.gv", "-o", "output/output." + args.format])
