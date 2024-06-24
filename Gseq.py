from sys import argv

if len(argv) < 2:
    print("Please use as follows")
    print("python Gseq.py <seqLength>")
    exit()

seqLength = int(argv[1])
seqArr = [0]

for i in range(1, seqLength + 1):
    seqArr.append(i - seqArr[seqArr[i-1]])

print(seqArr[2:])
