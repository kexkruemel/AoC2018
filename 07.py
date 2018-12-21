#!/usr/bin/env python2.7
import sys
import re
import numpy
import datetime
from collections import deque

def update_freelist(freelist,charlist,dependency):
    for item in charlist:
        if item not in freelist:
            if item not in dependency:
                freelist.append(item)
            elif dependency[item] == []:
                freelist.append(item)
    freelist.sort(reverse=True) #sort reverse to be able to use pop

start = datetime.datetime.now()

if len(sys.argv) > 1:
    app = "test"
else:
    app = "final"

file_name = "07_" + app + ".txt"
file = open(file_name, 'r')
prog = re.compile(r"Step (.) must be finished before step (.) can begi")
dependency = {}
charlist = set([])
for line in file:
    #update dependency list
    if prog.match(line).groups()[1] not in dependency:
        dependency[prog.match(line).groups()[1]] = [prog.match(line).groups()[0]]
    else:
        dependency[prog.match(line).groups()[1]].append(prog.match(line).groups()[0])
    #update charlist
    charlist.add(prog.match(line).groups()[0])
    charlist.add(prog.match(line).groups()[1])

solution = ""
freelist=[]
while 1:
    #find out which chars are free
    update_freelist(freelist,charlist,dependency)
    if len(freelist) == 0:
        break

    next = freelist.pop()
    solution = solution + next
    for key in dependency:
        if next in dependency[key]:
            #delete dependency
            dependency[key].remove(next)
    charlist.remove(next)

    if len(charlist) == 0:
        break

print solution
print "Took %s" %str(datetime.datetime.now()-start)
