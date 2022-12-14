#
# Advent of Code 2022
# Bryan Clair
#
# Day 13
#
import sys
sys.path.append("..")
import aocutils
import functools


args = aocutils.parse_args()

inputfile = open(args.file).read().strip()
pairs = [[eval(line) for line in pair.split('\n')] for pair in inputfile.split('\n\n')]

def compare(left, right):
    try:
        return right - left
    except TypeError:
        pass
    
    if not isinstance(left, list):
        left = [left]
    if not isinstance(right, list):
        right = [right]

    for l, r in zip(left,right):
        v = compare(l,r)
        if v != 0:
            return v
        
    # tied, break it based on which list is longer
    return len(right) - len(left)

good = 0
for index, pair in enumerate(pairs, start = 1):
    left, right = pair
    if compare(left,right) > 0:
        good += index

print('part 1:',good)

allvals = [p for pair in pairs for p in pair]
allvals.append([[2]])
allvals.append([[6]])

allvals.sort(key = functools.cmp_to_key(compare), reverse=True)

sol = 1
for index, val in enumerate(allvals, start = 1):
    if val == [[2]] or val == [[6]]:
        sol *= index

print('part 2:',sol)

# From learnpython.com
#
#   It is challenging to find a case where cmp cannot be replaced by key.
#   Because performance-wise functools.cmp_to_key(func) is very slow compared
#   to key, it only should be used as a last resort to implement a custom sort
#   function in Python.
#
