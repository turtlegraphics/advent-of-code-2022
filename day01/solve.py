#
# Advent of Code 2022
# Bryan Clair
#
# Day 01
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

tot = 0
melf = 0
elves = []
for line in inputlines:
    if line:
        v = int(line)
        tot += v
    else:
        if tot > melf:
            melf = tot
        elves.append(tot)
        tot = 0

print(melf)
elves.sort()
print(sum(elves[-3:]))
