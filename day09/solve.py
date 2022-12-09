#
# Advent of Code 2022
# Bryan Clair
#
# Day 09
#
import sys
sys.path.append("..")
import aocutils
from aocutils import Point, Grid

args = aocutils.parse_args()

dirs = {
    'R':Point(1,0),
    'L':Point(-1,0),
    'U':Point(0,1),
    'D':Point(0,-1)
}

def solve(numk):
    knots = []
    for k in range(numk):
        knots.append(Point(0,0))
    visited = Grid()
    tail = numk-1
    visited[knots[tail]] = '#'

    for line in inputlines:
        dir,amt = line.split()
        dir = dirs[dir]
        amt = int(amt)

        for i in range(amt):
            knots[0] += dir
            for k in range(numk-1):
                # knot k+1 needs to follow knot k
                if knots[k+1].dist(knots[k]) > 1.5:
                    td = knots[k]-knots[k+1]
                    if abs(td.x) == 2:
                        td.x = td.x//2
                    if abs(td.y) == 2:
                        td.y = td.y//2
                    knots[k+1] += td
            visited[knots[tail]] = '#'
            #visited.display()
            #print()

    count = 0
    for g in visited:
        if visited[g] == '#':
            count += 1
    return count

inputlines = [x.strip() for x in open(args.file).readlines()]

print('part 1:',solve(2))
print('part 2:',solve(10))
