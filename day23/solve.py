#
# Advent of Code 2022
# Bryan Clair
#
# Day 23
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

grove = aocutils.Grid()
grove.scan(inputlines)

spread = {
    'N' : [(0,1),(-1,1),(1,1)],
    'S' : [(0,-1),(-1,-1),(1,-1)],
    'W' : [(-1,0),(-1,1),(-1,-1)],
    'E' : [(1,0),(1,1),(1,-1)]
    }

class Elf:
    def __init__(self, id, p):
        self.id = id
        self.pos = aocutils.Point(p)
        self.proposal = None
        
    def __str__(self):
        out = str(self.id) + ':' + str(self.pos)
        return out

    def move(self):
        if self.proposal:
            grove[self.pos] = '.'
            self.pos = self.proposal
            self.proposal = None
            grove[self.pos] = '#'
            return True
        return False
            
    def propose(self, order):
        allclear = True
        proposal = None
        for dir in order:
            check = spread[dir]
            dirclear = True
            for d in check:
                dp = aocutils.Point(d)
                try:
                    what = grove[self.pos + dp]
                    if what == '#':
                        dirclear = False
                        allclear = False
                except KeyError:
                    pass # ok, nothing there
            if dirclear:
                if not proposal:
                    proposal = dir
        if allclear:
            proposal = None
        if proposal:
            self.proposal = self.pos + aocutils.Point(spread[proposal][0])
        else:
            self.proposal = None
        return self.proposal
        
elves = []
elfid = 0
for p in grove:
    if grove[p] == '#':
        elves.append(Elf(elfid,p))
        elfid += 1

order = ['N','S','W','E']


def elfstep(order):
    badspots = []
    for e in elves:
        spot = e.propose(order)
        if spot is None:
            continue
        
        try:
            grove[spot]
        except KeyError:
            # extend the forest
            grove[spot] = '.'
            
        if grove[spot] == '.':
            grove[spot] = '+'
        else:
            # print('spot',spot,'gs:',grove[spot])
            assert(grove[spot] == '+')
            grove[spot] = 'X'
            badspots.append(spot)

    for e in elves:
        if e.proposal is None:
            continue
        if grove[e.proposal] == 'X':
            e.proposal = None

    for p in badspots:
        grove[p] = '.'  # clear the X's

    anyone_moved = False
    for e in elves:
        if e.move():
            anyone_moved = True
    return anyone_moved

def part1free():
    big = 1000000
    xmin = big
    xmax = -big
    ymin = big
    ymax = -big
    for e in elves:
        x,y = e.pos
        if x > xmax:
            xmax = x
        if x < xmin:
            xmin = x
        if y > ymax:
            ymax = y
        if y < ymin:
            ymin = y

    # print('x',xmin,xmax,'y',ymin,ymax)
    # grove.display()

    empty = 0
    for x in range(xmin,xmax+1):
        for y in range(ymin,ymax+1):
            try:
                if grove[x,y] == '.':
                    empty += 1
            except KeyError:
                empty += 1

    return empty
    
round = 1
moved = True
while moved:
    moved = elfstep(order)
    if args.debug:
        print('round',round,order)
        grove.display()
    first = order.pop(0)
    order.append(first)
    if round == 10:
        print('part 1:',part1free())
    round += 1
    if (round % 100 == 0):
        print(1+(1000-round)//100,end='..',flush=True)
print()
print('part 2:',round-1)
