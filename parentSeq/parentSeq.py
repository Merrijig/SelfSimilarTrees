from sys import argv
from glob import glob
from readFunc import createSeqFunc

if len(argv) != 3:
    print("Please use as follows")
    print("python parentSeq.py <ruleDirPath> <seqLength>")
    exit()

# Arguments
ruleDirPath = argv[1]
seqLength = int(argv[2])


seqArr = {}
for count, ruleFile in enumerate(glob(ruleDirPath, "seq?Rule.txt")):
    # -9 to find the letter in the filename
    letter = ruleFile[-9]

    # Create a tuple containing the sequence function and its array
    seqArr.append(letter,
                  (createSeqFunc(ruleDirPath + "seq" + letter + "Rule.txt"), []))


for n in range(seqLength):
    seqArr.append(seqFunc(n, seqArr))

print(seqArr)
