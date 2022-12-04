#
# Advent of Code 2022
# Bryan Clair
#
# Day 04
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

import re
parser = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")

contain = 0
overlap = 0
for line in inputlines:
    print(line,)
    v1,v2,w1,w2 = [int(x) for x in parser.match(line).groups()]
    if (v1 <= w1) and (w2 <= v2):
        contain += 1
        overlap += 1
        print('v big:',v1,v2,w1,w2)
    elif (w1 <= v1) and (v2 <= w2):
        contain += 1
        overlap += 1
        print('w big:',v1,v2,w1,w2)
    elif (v1 <= w1) and (w1 <= v2):
        overlap += 1
    elif (w1 <= v1) and (v1 <= w2):
        overlap += 1
    else:
        print('nope')

print(contain)
print(overlap)

