#
# Advent of Code 2022
# Bryan Clair
#
# Day 10
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

# import re
# parser = re.compile(r"name:\s*(\w+)\s*val:\s*(\d+)") # or whatever
# name, val = parser.match(line).groups()
# val = int(val)

cycle = 0
target = 20
X = 1
strength = 0
row = 0

screen = aocutils.Grid()

for line in inputlines:
    inst = line.split()
    if inst[0] == 'noop':
        if cycle == target:
            strength += cycle * X
            target += 40
        col = cycle % 40
        pixel = aocutils.Point(col, cycle // 40)
        screen[pixel] = '#' if abs(col - X) <= 1 else '.'
        cycle += 1

    if inst[0] == 'addx':
        if cycle == target:
            strength += cycle * X
            target += 40
        col = cycle % 40
        pixel = aocutils.Point(col, cycle // 40)
        screen[pixel] = '#' if abs(col - X) <= 1 else '.'
        cycle += 1

        if cycle == target:
            strength += cycle * X
            target += 40
        col = cycle % 40
        pixel = aocutils.Point(col, cycle // 40)
        screen[pixel] = '#' if abs(col - X) <= 1 else '.'
        cycle += 1

        X += int(inst[1])
    
print('part 1:',strength)
print('part 2:')
screen.display(vflip=True)


    
