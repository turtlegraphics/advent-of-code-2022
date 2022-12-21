#
# Advent of Code 2022
# Bryan Clair
#
# Day --
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

monkeys = {}
for line in inputlines:
    name,yell = line.split(': ')
    if yell[0].isdigit():
        monkeys[name] = int(yell)
    else:
        monkeys[name] = yell.split()

def calc(who):
    yell = monkeys[who]
    if isinstance(yell,int):
        return yell
    left = calc(yell[0])
    right = calc(yell[2])
    if yell[1] == '+':
        return left + right
    if yell[1] == '-':
        return left - right
    if yell[1] == '/':
        return left // right
    if yell[1] == '*':
        return left * right
    
print('part 1:',calc('root'))

root = monkeys['root']

# turns out, right hand side doesn't depend on 'humn'
# and left hand side is strictly decreasing in 'humn'


step = 1
v = 0  # really good initial guess :-)

while True:
    monkeys['humn'] = v
    left = calc(root[0])
    right = calc(root[2])
    # print(step,v,left,right,right-left)
    if (left == right):
        print('part 2:',v)
        quit()
    if (left < right):
        if step > 0:
            step = -1
        v += step
    else:
        if step < 0:
            step  = 1
        v += step
    step *= 2
