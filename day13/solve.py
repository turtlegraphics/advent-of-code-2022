#
# Advent of Code 2022
# Bryan Clair
#
# Day 13
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputfile = open(args.file).read()
pairs = [x.split('\n') for x in inputfile.split('\n\n')]

def compare_lists(left,right):
    for i in range(len(left)):
        try:
            v = compare(left[i],right[i])
        except IndexError:
            return -1  # right list ran out, wrong order
        if v != 0:
            return v
    if len(right) > len(left):
        return 1  # right order
    return 0   # no decision

def compare(left, right):
    if isinstance(left, list):
        if isinstance(right, list):
            return compare_lists(left,right)
        else:
            assert(isinstance(right,int))
            return compare_lists(left,[right])
    else:
        assert(isinstance(left,int))
        if isinstance(right,list):
            return compare_lists([left],right)
        else:
            assert(isinstance(right,int))
            if (left < right):
                return 1  # right order
            if (left > right):
                return -1  # wrong order
            if (left == right):
                return 0  # no decision
    assert(False)

good = 0
for i in range(len(pairs)):
    index = i+1
    left = eval(pairs[i][0])
    right = eval(pairs[i][1])
    v = compare(left,right)
    if v == 1:
        good += index

print('part 1:',good)

allvals = []
for p in pairs:
    allvals.append(eval(p[0]))
    allvals.append(eval(p[1]))

allvals.append([[2]])
allvals.append([[6]])

import functools

allvals.sort(key = functools.cmp_to_key(compare), reverse=True)

sol = 1
for i in range(len(allvals)):
    if isinstance(allvals[i],list) and len(allvals[i]) == 1:
        if isinstance(allvals[i][0],list) and len(allvals[i][0]) == 1:
            if allvals[i][0][0] in [2,6]:
                sol *= i+1

print('part 2:',sol)

# From learnpython.com
#
#   It is challenging to find a case where cmp cannot be replaced by key.
#   Because performance-wise functools.cmp_to_key(func) is very slow compared
#   to key, it only should be used as a last resort to implement a custom sort
#   function in Python.
#
