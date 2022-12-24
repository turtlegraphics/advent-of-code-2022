#
# Advent of Code 2022
# Bryan Clair
#
# Day 24
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

bdirs = {
    '>' : aocutils.Point(1,0),
    '<' : aocutils.Point(-1,0),
    'v' : aocutils.Point(0,-1),
    '^' : aocutils.Point(0,1)
    }

dirtxt = {}
for c,dir in bdirs.items():
    dirtxt[dir] = c

class Blizzard:
    def __init__(self,pos,dir,id):
        self.id = id
        self.pos = aocutils.Point(pos)
        self.dir = aocutils.Point(dir)
        self.time = 0
        
    def move(self):
        self.pos += self.dir
        self.time += 1
        if self.pos.x == 0:
            self.pos.x = xmax-1
        if self.pos.x == xmax:
            self.pos.x = 1
        if self.pos.y == 0:
            self.pos.y = ymax-1
        if self.pos.y == ymax:
            self.pos.y = 1
            
    def __str__(self):
        out = 'blizzard ' + str(self.id)
        out += ' at ' + str(self.pos)
        out += ' at time ' + str(self.time)
        return out

class Field:
    def __init__(self,lines):
        self.field = [aocutils.Grid()]
        self.field[0].scan(lines)
        self.maxtime = 0
        
        self.blizzards = []
        bid = 0
        for p in self.field[0]:
            c = self.field[0][p]
            if c in bdirs:
                self.blizzards.append(Blizzard(p,bdirs[c],bid))
                bid += 1
                
        self.blankfield = aocutils.Grid()
        for p in self.field[0]:
            c = self.field[0][p]
            if c in bdirs:
                self.blankfield[p] = '.'
            else:
                self.blankfield[p] = c
        
    def bounds(self):
        return self.field[0].bounds()

    def __getitem__(self,v):
        t,p = v
        while t > self.maxtime:
            self._nexttime()
        return self.field[t][p]

    def _nexttime(self):
        self.maxtime += 1
        self.field.append(aocutils.Grid(self.blankfield))
        for b in self.blizzards:
            b.move()
            c = self.field[-1][b.pos]
            if c == '.':
                self.field[-1][b.pos] = dirtxt[b.dir]
            elif c.isdigit():
                self.field[-1][b.pos] = str(int(c)+1)
            else:
                self.field[-1][b.pos] = '2'

    def neighbors(self,t,pos):
        """Return clear spots to move from position pos at time t."""
        nbrs = self.field[t].neighbors(pos)
        clear = []
        for n in nbrs:
            if self[t+1,n] == '.':
                clear.append(tuple(n))
        if self[t+1,pos] == '.':
            # stay put
            clear.append(tuple(pos))
        return clear
    
    def display(self,t):
        while t > self.maxtime:
            self._nexttime()
        self.field[t].display()
        
field = Field(inputlines)
xmin, ymin, xmax, ymax = field.bounds()

start = (1,ymax)
finish = (xmax-1,0)

def path_seek(pos,goal,t0):
    dist = {}
    prev = {}
    Q = set()

    start = (t0,pos)
    Q.add(start)
    dist[start] = 0
    prev[start] = None

    max_time_seen = t0

    while Q:
        if len(Q) % 10000 == 0:
            print(len(Q))

        min_dist = 100000000
        for p in Q:
            if dist[p] < min_dist:
                min_dist = dist[p]
                u = p

        ut,upos = u

        if ut > max_time_seen and args.debug:
            max_time_seen = ut
            if (max_time_seen % 10 == 0):
                print('up to time',ut)

        if upos == goal:
            return ut

        Q.remove(u)

        nbrs = field.neighbors(ut,upos)
        for v in nbrs:
            v = (ut+1,v)
            alt = dist[u] + 1

            if v in Q:
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
            else:
                Q.add(v)
                dist[v] = alt
                prev[v] = u

t0 = path_seek(start,finish,0)
print('Part 1:',t0)
t1 = path_seek(finish,start,t0)
print('  (returned to start at: '+str(t1)+')')
t2 = path_seek(start,finish,t1)
print('Part 2:',t2)
