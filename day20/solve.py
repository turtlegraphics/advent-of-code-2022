#
# Advent of Code 2022
# Bryan Clair
#
# Day 20
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

vals = [int(x.strip()) for x in open(args.file).readlines()]
N = len(vals)

initial = [x for x in enumerate(vals)]
mix = list(initial)

for p in initial:
    n,x = p
    i = mix.index(p)
    mix.pop(i)
    j = (i + x) % (N-1)
    mix.insert(j,p)

zero = (vals.index(0),0)
coords = [mix[(i + mix.index(zero)) % N][1] for i in [1000,2000,3000]]

print('part 1:',sum(coords))

key = 811589153
initial = [(n,x*key) for (n,x) in enumerate(vals)]
mix = list(initial)

for _ in range(10):
    for p in initial:
        n,x = p
        i = mix.index(p)
        mix.pop(i)
        j = (i + x) % (N-1)
        mix.insert(j,p)

coords = [mix[(i + mix.index(zero)) % N][1] for i in [1000,2000,3000]]

print('part 2:',sum(coords))


    
