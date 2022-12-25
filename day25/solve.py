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

# import re
# parser = re.compile(r"name:\s*(\w+)\s*val:\s*(\d+)") # or whatever
# name, val = parser.match(line).groups()
# val = int(val)

sdig = {
    '=' : -2,
    '-' : -1,
    '0' : 0,
    '1' : 1,
    '2' : 2
    }

digs = ['0','1','2','=','-']

def snafu2dec(v):
    digits = [sdig[d] for d in list(v)]
    digits.reverse()
    return sum([d*(5**i) for i,d in enumerate(digits)])

def dec2snafu(v):
    val = ''
    while (v != 0):
        nextdig = digs[v % 5]
        val = nextdig + val
        v = (v - sdig[nextdig])//5
    return val

fuel = sum([snafu2dec(line) for line in inputlines])

print(dec2snafu(fuel))

    
