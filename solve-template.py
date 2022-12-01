#
# Advent of Code 2022
# Bryan Clair
#
# Day --
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

parser = re.compile(r"name:\s*(\w+)\s*val:\s*(\d+)") # or whatever

for line in inputlines:
    print(line)
    name, val = parser.match(line).groups()
    print(name,val)
    
