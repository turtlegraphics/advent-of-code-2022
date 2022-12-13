#
# Advent of Code 2022
# Bryan Clair
#
# Day 12
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

def elevation(c):
    if c == 'S':
        c = 'a'
    if c == 'E':
        c = 'z'
    return ord(c) - ord('a')

def distance(p,q):
    """Return distance from neighboring points p to q in the terrain."""
    elp = elevation(terrain[p])
    elq = elevation(terrain[q])
    if elq > elp + 1:
        return 100000
    else:
        return 1
    
terrain = aocutils.Grid()
terrain.scan(inputlines)
terrain.display()
for p in terrain:
    if terrain[p] == 'S':
        path_start = p
    if terrain[p] == 'E':
        path_end = p

print(path_start,path_end)

dist, prev = terrain.dijkstra(path_start, path_end, distance)
length = dist[path_end]
print('part 1:',length)

# part 2

# this is complete garbage, takes forever to run, trivial to improve

best = length
bestpoint = path_start

acount = 0
for p in terrain:
    if terrain[p] == 'a':
        acount += 1

print('to check:',acount)

complete = 0
for p in terrain:
    if terrain[p] == 'a':
        acount -= 1
        if acount % 50 == 0:
            print('to check:',acount)
        # let's try it!
        dist, prev = terrain.dijkstra(p, path_end, distance)
        length = dist[path_end]
        if length < best:
            best = length
            betspoint = p
            print('newbest:',best)

print('part 2:',best)


