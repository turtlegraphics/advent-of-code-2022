#
# Advent of Code 2022
# Bryan Clair
#
# Day 15
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

import re
parser = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

class Row:
    def __init__(self,y):
        self.y = y         # y coord of this row
        self.beacons = set()  # x coords of beacons in this row
        self.ranges = []   # ranges of impossibility in this row

    def mark(self, s, b, dist):
        if b.y == self.y:
            self.beacons.add(b.x)
            
        v = abs(s.y - self.y)
        if v <= dist:
            x0 = s.x - (dist - v)
            x1 = s.x + (dist - v)
            self._addrange(x0,x1)

    def _addrange(self,x0,x1):
        # add a range, keeping contiguous ranges
        # print('add',x0,x1)
        # find the rightmost range with x coordinate less than x0
        try:
            i = 0
            while self.ranges[i][0] < x0:
                i += 1
        except IndexError:
            pass
        if (i == 0) or (x0 > self.ranges[i-1][1]+1):
            self.ranges.insert(i,[x0,x1])
        else:
            i -= 1
            # combine with range[i]
            self.ranges[i][1] = max(self.ranges[i][1],x1)

        # now see if the ith range needs to combine with i+1:
        try:
            while self.ranges[i][1] >= self.ranges[i+1][0]-1:
                self.ranges[i][1] = max(self.ranges[i][1],self.ranges[i+1][1])
                del self.ranges[i+1]
        except IndexError:
            pass

    def is_beacon(self):
        # return True if this row could contain a beacon
        return len(self.ranges) > 1
    
    def count(self):
        """Return count (slowly) for part 1"""
        row = {}
        for r in self.ranges:
            x0,x1 = r
            for x in range(x0,x1+1):
                row[x] = 1

        for bx in self.beacons:
            row[bx] = 0

        sum = 0
        for k,v in row.items():
            sum += v
        return sum
    
        
sensors = []
beacons = []
dists = []

for line in inputlines:
    vals = parser.match(line).groups()
    sx,sy,bx,by = [int(v) for v in vals]
    s = aocutils.Point(sx,sy)
    sensors.append(s)
    b = aocutils.Point(bx,by)
    beacons.append(b)
    dists.append(s.mandist(b))

if args.file == 'input.txt':
    the_row = 2000000
    max_coord = 4000000
elif args.file == 'test.txt':
    the_row = 10
    max_coord = 20
else:
    print('not prepared for that input file')
    quit()
    
part1 = Row(the_row)
for s,b,d in zip(sensors, beacons, dists):
    part1.mark(s,b,d)    
print('part 1:',part1.count())

print('solving part 2')
for y in range(max_coord+1):
    if y % 100000 == 0:
        print((max_coord - y)//100000,'..',end='',flush=True)
    r = Row(y)
    for s,b,d in zip(sensors, beacons, dists):
        r.mark(s,b,d)
    if r.is_beacon():
        print()
        print('found at row',y)
        print(r.ranges)
        x = r.ranges[0][1]+1
        print('part 2:',x*4000000 + y) # tuning always uses 4000000
        quit()
