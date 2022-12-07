#
# Advent of Code 2022
# Bryan Clair
#
# Day 07
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

system = {}

def dump(cwd = '',depth=0):
    print('  '*depth,cwd,'(dir)')
    for (size, name) in system[cwd]:
        if size == 'dir':
            dump(cwd+'/'+name,depth+1)
        else:
            print('  '*(depth+1),name,size)

part1sum = 0

def totsize(cwd = '',depth=0):
    global part1sum
    mysize = 0
    # print('  '*depth,cwd,'(dir)')
    for (size, name) in system[cwd]:
        if size == 'dir':
            mysize += totsize(cwd+'/'+name,depth+1)
        else:
            # print('  '*(depth+1),name,size)
            mysize += size
    # print('  '*depth,cwd,'has size',mysize)
    if mysize < 100000:
        part1sum += mysize
    return mysize

bestdir = 70000000
def findkill(cwd = '',depth=0):
    global needed
    global bestdir
    mysize = 0
    # print('  '*depth,cwd,'(dir)')
    for (size, name) in system[cwd]:
        if size == 'dir':
            mysize += findkill(cwd+'/'+name,depth+1)
        else:
            # print('  '*(depth+1),name,size)
            mysize += size
    # print('  '*depth,cwd,'has size',mysize)
    if mysize >= needed and mysize < bestdir:
        bestdir = mysize
    return mysize

for line in inputlines:
    if line[0] == '$':
        command = line[2:].split()
        if command[0] == 'cd':
            if command[1] == '/':
                cwd = ''
            elif command[1] == '..':
                cwd = cwd.rsplit('/',1)[0]
            else:
                cwd += '/' + command[1]
    else: # part of output of ls
        if cwd not in system.keys():
            system[cwd] = []
        size, name = line.split()
        if size != 'dir':
            size = int(size)
        system[cwd].append( (size, name) )

# dump()
used = totsize()
print('part1:',part1sum)

freespace = 70000000 - used
needed    = 30000000 - freespace
# print('need to delete at least',needed)
findkill()
print('part2:',bestdir)
