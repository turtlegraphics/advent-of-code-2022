#
# Advent of Code 2021
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

parser = re.compile(r"name: (\w+) val: (\d+)") # or whatever

for line in inputlines:
    print line
    name, val = parser.match(line).groups()
