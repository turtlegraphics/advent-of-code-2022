#
# Advent of Code 2022
# Bryan Clair
#
# Day 11
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

class Monkey:
    def __init__(self, num, operation, testval, whotrue, whofalse):
        self.items = []
        self.num = num
        self.operation = operation
        self.testval = testval
        self.whotrue = whotrue
        self.whofalse = whofalse
        self.inspections = 0
        
    def __str__(self):
        return 'Monkey '+str(self.num)+' has '+ str(self.items)

    def append(self, item):
        self.items.append(item)

    def throw(self):
        for item in self.items:
            self.inspections += 1
            old = item
            new = eval(self.operation)
            if args.part == 1:
                new = new // 3
            else:
                new = new % modulus
            if new % self.testval == 0:
                target = self.whotrue
            else:
                target = self.whofalse
            monkeys[target].append(new)

        self.items = []
        
monkeys = []

l=0
modulus = 1

while l < len(inputlines):
    line = inputlines[l]
    l += 1
    assert(line[0:6] == 'Monkey')
    num = int(line.split()[1].strip(':'))
        
    line = inputlines[l]
    l += 1
    v = line.split()[2:]
    worry = [int(x.strip(',')) for x in v]

    line = inputlines[l]
    l += 1
    operation = line.split(maxsplit=3)[-1]
    
    line = inputlines[l]
    l += 1
    test = int(line.split()[-1])
    modulus *= test
    
    line = inputlines[l]
    l += 1
    whotrue = int(line.split()[-1])
    line = inputlines[l]
    l += 1
    whofalse = int(line.split()[-1])

    m = Monkey(num, operation, test, whotrue, whofalse)
    for i in worry:
        m.append(i)
    monkeys.append(m)
    
    l += 1

print('Solving part',args.part)

rounds = [20,10000]
for round in range(rounds[args.part-1]):
    for m in monkeys:
        m.throw()
    
insp = []
for m in monkeys:
    insp.append(m.inspections)
insp.sort(reverse=True)

print('part',args.part,':',insp[0]*insp[1])
