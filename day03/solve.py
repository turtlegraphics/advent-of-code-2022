#
# Advent of Code 2022
# Bryan Clair
#
# Day 03
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

parser = re.compile(r"name:\s*(\w+)\s*val:\s*(\d+)") # or whatever


def priority(v):
    if v.islower():
        return ord(v) - ord('a') + 1
    else:
        return ord(v) - ord('A') + 27

tot = 0
for line in inputlines:
    first = set(line[:len(line)//2])
    second = set(line[len(line)//2:])
    both = first.intersection(second)
    tot += priority(list(both)[0])

print(tot)

tot = 0
group = 0
while group < len(inputlines):
    badge = set(inputlines[group])
    badge = badge.intersection(set(inputlines[group+1]))
    badge = badge.intersection(set(inputlines[group+2]))
    tot += priority(list(badge)[0])
    group += 3
print(tot)
    
    

    
