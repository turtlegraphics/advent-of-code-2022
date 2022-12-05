#
# Advent of Code 2022
# Bryan Clair
#
# Day 05
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

import re
parser = re.compile(r"move (\d+) from (\d+) to (\d+)") # or whatever

inputstacks = [
    'RSLFQ',
    'NZQGPT',
    'SMQB',
    'TGZJHCBQ',
    'PHMBNFS',
    'PCQNSLVG',
    'WCF',
    'QHGZWVPM',
    'GZDLCNR'
    ]

def dump():
    for i in range(len(stacks)):
        out = str(i)
        for v in stacks[i]:
            out += '['+v+']'
        print(out)

def last():
    out = ''
    for i in range(len(stacks)):
        out += stacks[i][-1]
    return out

def move(froms, tos):
    what = stacks[froms-1].pop()
    stacks[tos-1].append(what)

def move2(count, froms, tos):
    what = stacks[froms-1][-count:]
    stacks[froms-1] = stacks[froms-1][:-count]
    stacks[tos-1] = stacks[tos-1]+what
    
stacks = [list(s) for s in inputstacks]
gap = False
for line in inputlines:
    if gap:
        count,froms,tos = [int(x) for x in parser.match(line).groups()]
        for i in range(count):
            move(froms,tos)
    else:
        if not line:
            gap = True

print('part 1:',last())

stacks = [list(s) for s in inputstacks]
gap = False
for line in inputlines:
    if gap:
        count,froms,tos = [int(x) for x in parser.match(line).groups()]
        move2(count,froms,tos)
    else:
        if not line:
            gap = True

print('part 2:',last())
