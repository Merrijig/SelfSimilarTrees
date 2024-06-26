from processNode import generateNodeList
from jsonParser import load_tree


class TreeData(object):
    def __init__(self, processDepth, treeDirPath):
        self.processDepth = processDepth

        self.treeDirPath = treeDirPath
        self.rulesDict = dict.fromkeys(generateNodeList(treeDirPath), 0)
        self.nodeDictTemplate = dict(self.rulesDict)
        self.nodeDictTemplate["O"] = 0
        self.rows = [dict(self.nodeDictTemplate) for i in range(processDepth)]
        for key in self.rulesDict.keys():
            self.generate_rule(key)

        self.load_base()

    def load_base(self):
        base_tree = load_tree(self.treeDirPath + "base.json")
        for i in range(base_tree.depth() + 1):  # Inclusive +1
            nodes = base_tree.filter_nodes(lambda node:
                                           base_tree.depth(node) == i)
            for node in nodes:
                self.rows[i][node.tag] += 1

    def generate_rule(self, node_type):
        level_rules = []
        rule_tree = load_tree(self.treeDirPath + node_type + ".json")
        for i in range(1, rule_tree.depth() + 1):  # Inclusive +1
            level_rule = dict(self.nodeDictTemplate)
            nodes = rule_tree.filter_nodes(lambda node:
                                           rule_tree.depth(node) == i)
            for node in nodes:
                level_rule[node.tag] += 1

            level_rules.append(level_rule)

        self.rulesDict[node_type] = level_rules

    def process_rows(self):
        for src_depth in range(self.processDepth):
            for input_type, level_rules in self.rulesDict.items():
                for i, level_rule in enumerate(level_rules):
                    if src_depth + i + 1 >= self.processDepth:
                        break
                    for output_type, increment in level_rule.items():
                        self.rows[src_depth + i + 1][output_type] += (
                                self.rows[src_depth][input_type] * increment
                                )

    def get_row_data(self):
        return self.rows
