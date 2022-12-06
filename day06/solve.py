#
# Advent of Code 2022
# Bryan Clair
#
# Day 06
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

line = inputlines[0]
for i in range(len(line)-14):
    code = line[i:i+14]
    if len(set(list(code))) == 14:
        print(i+14)
        break


    



    
