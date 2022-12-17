#
# Advent of Code 2022
# Bryan Clair
#
# Day 17
#
import sys
sys.path.append("..")
from aocutils import Point, Grid, parse_args

args = parse_args()
jet_pattern = open(args.file).read().strip()

blockstr = """
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""

blocks = [Grid() for b in range(5)]
for b,g in zip(blocks, blockstr.split('\n\n')):
    b.scan(g.split())
    dots = []
    for p in b:
        if b[p] == '.':
            dots.append(p)
    for p in dots:
        b.pop(p)

class Chamber():
    def __init__(self,jets):
        self.chamber = Grid()
        for x in range(7):
            self.chamber[x,0] = '-'
        self.jets = jets
        self.j = 0

    def fit(self, b, pos):
        """True if b fits in chamber position pos"""
        for pt in b:
            loc = pos+Point(pt)
            x,y = loc
            if x < 0 or x > 6:
                return False
            if loc in self.chamber:
                return False
        return True
    
    def add(self, b, pos):
        """Add b to the chamber at position pos"""
        for pt in b:
            loc = pos + Point(pt)
            assert(loc.x >= 0 and loc.x <= 6)
            assert(loc not in self.chamber)
            self.chamber[loc] = '#'

    def drop(self, b):
        bpos = Point(2, self.chamber.ymax + 4)
        down = Point(0,-1)
        left = Point(-1,0)
        right = Point(1,0)
        while self.fit(b,bpos):
            if self.jets[self.j] == '<':
                if self.fit(b, bpos + left):
                    bpos += left
            if self.jets[self.j] == '>':
                if self.fit(b, bpos + right):
                    bpos += right
            self.j = (self.j + 1) % len(self.jets)
            assert(self.fit(b, bpos))
            bpos += down

        self.add(b,bpos - down)
        return (bpos - down).x

    def height(self):
        return self.chamber.ymax
    
    def display(self):
        self.chamber.display(blank='.')
        
xvals = [0,0,0,0,0]
patterns_seen = {}
deltah = {}
deltas = {}

chamber = Chamber(jet_pattern)
step = 0
while step < 3000:
    xvals[step % 5] = chamber.drop(blocks[step % 5])
    step += 1

    # check if we've seen this pattern of five x values in the past
    
    if step % 5 == 0:
        pattern = tuple(xvals)
        if pattern in patterns_seen:
            # we've seen it before, record the number of steps elapsed
            # and the change in height.  Keep track of those numbers
            # in a frequency table deltas or deltah
            lasts, lasth = patterns_seen[pattern]
            
            ds = step - lasts
            if ds in deltas:
                deltas[ds] += 1
            else:
                deltas[ds] = 0

            dh = chamber.height() - lasth
            if dh in deltah:
                deltah[dh] += 1
            else:
                deltah[dh] = 0

        patterns_seen[pattern] = (step, chamber.height())
        
    if step == 2022:
        print('part 1:',chamber.height())

# find the steps elapsed / height changes that happened the most,
# these correspond to the repeating behavior

smod = max(deltas, key=deltas.get)
hmod = max(deltah, key=deltah.get)
print('pattern repeats after every',smod,'steps, gaining height',hmod)

total_steps = 1000000000000
loops = (total_steps // smod)  # works for my input, might need to subtract 1
remain = total_steps - smod*loops
assert(total_steps == smod*loops + remain)

chamber = Chamber(jet_pattern)
step = 0
while step < remain:
    chamber.drop(blocks[step % 5])
    step += 1
    
print('part 2:', chamber.height() + loops * hmod)
