#
# Advent of Code 2022
# Bryan Clair
#
# Day 22
#
import sys
sys.path.append("..")
import os
import math
import aocutils

args = aocutils.parse_args()

inputlines = open(args.file).read()
maplines, path = inputlines.split('\n\n')
path = path.strip()
maplines = maplines.split('\n')

# load aux file with same name as input file except .py extension
gluefile = os.path.splitext(args.file)[0] + '.py'
wrapmap = eval(open(gluefile).read())
# sanity check on the wrap map
for m in wrapmap:
    assert(wrapmap[wrapmap[m]] == m)
    

# Build the map
map = aocutils.Grid()
map.scan(maplines)
# remove the spaces
kill = []
for p in map:
    if map[p] == ' ':
        kill.append(p)
for p in kill:
    map.pop(p)

# set up some basic map information
xmin, ymin, xmax, ymax = map.bounds()
squareside = math.gcd(1+xmax-xmin,1+ymax-ymin)
startx = maplines[0].index('.') # start location for the path

dirs = [aocutils.Point(p) for p in [(1,0),(0,-1),(-1,0),(0,1)]]
alphadirs = ['R','D','L','U']


def edgewrap(pos, dir):
    """Wrap around edge of map, moving dir from position pos"""
    while True:
        nextpos = pos - dir
        try:
            map[nextpos]
            pos = nextpos
        except KeyError:
            # hit edge
            return (pos, dir)

def cubewrap(pos, dir):
    """Wrap around cube, moving dir from position pos"""
    # sx,sy are which face of the cube
    sx,sy = pos.x // squareside, pos.y // squareside
    # x,y are position within that face
    x,y = pos.x % squareside, pos.y % squareside
    # side is which side of the face we're departing (R, D, L, U)
    side = alphadirs[dirs.index(dir)]

    # find new face and which side of it we're entering
    nsx,nsy,nside = wrapmap[(sx,sy,side)]

    # which way we're now moving
    ndir = dirs[alphadirs.index(nside)]*(-1)

    # calculate new location npos within the map

    # how far along the edge we are
    if side == 'U' or side == 'D':
        where = x
    else:
        where = y
    if side + nside not in ['UR','RU','DL','LD','UD','DU','LR','RL']:
        # reverse the location on the edge
        where = (squareside - 1) - where

    # compute new position within new face
    if nside == 'U':
        nx = where
        ny = (squareside - 1)
    elif nside == 'D':
        nx = where
        ny = 0
    elif nside == 'R':
        ny = where
        nx = (squareside - 1)
    elif nside == 'L':
        ny = where
        nx = 0

    # convert back to map coordinates
    npos = aocutils.Point(nsx*squareside + nx, nsy*squareside + ny)
    
    return (npos, ndir)

def move(pos, dir, dist, wrap_fun):
    while dist > 0:
        nextpos = pos + dir
        try:
            v = map[nextpos]
            nextdir = dir
        except KeyError:
            nextpos, nextdir = wrap_fun(pos,dir)
            v = map[nextpos]

        if v == '#':
            break # done moving

        assert(v == '.')
        
        pos = nextpos
        dir = nextdir
        
        dist = dist - 1

    return (pos,dir)

def solve(wrap_fun):
    tracemap = aocutils.Grid(map)
    pos = aocutils.Point((startx, ymax))
    dir = dirs[0]

    c=0
    while c < len(path):
        tracemap[pos] = alphadirs[dirs.index(dir)]
        
        if path[c] == 'R':
            w = dirs.index(dir)
            dir = dirs[(w + 1) % 4]
            c += 1
        elif path[c] == 'L':
            w = dirs.index(dir)
            dir = dirs[(w - 1) % 4]
            c += 1
        else:
            end = c+1
            try:
                while path[end].isdigit():
                    end += 1
            except IndexError:
                pass
            dist = int(path[c:end])
            pos, dir = move(pos, dir, dist, wrap_fun)
            c = end

    if args.verbose > 1:
        print()
        tracemap.display()
            
    row = ymax - pos.y + 1
    col = pos.x + 1
    facing = dirs.index(dir)
    return 1000*row+4*col+facing

print('part 1:',solve(edgewrap))
print('part 2:',solve(cubewrap))


