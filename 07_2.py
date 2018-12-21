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
    workers = 2
    offset = 0
else:
    app = "final"
    workers = 5
    offset = 60

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
workerlist = [[0,''] for _ in range(workers)]
time = 0
while 1:
    #check if someone finished
    for worker in workerlist:
        if worker[0] != 0:
            worker[0] -= 1
        #check if it is done with an old work
        if worker[0] == 0 and worker[1] != '':
            print ("Worker done with task %s" %worker[1])
            solution = solution + worker[1]
            for key in dependency:
                if worker[1] in dependency[key]:
                    #delete dependency
                    dependency[key].remove(worker[1])
            worker[1] = ''

    #find out which chars are free
    update_freelist(freelist,charlist,dependency)

    done = True
    #hand out work
    for worker in workerlist:
        if (len(freelist) > 0) and (worker[0] == 0):
            next = freelist.pop()
            charlist.remove(next)
            print ("Handing out %s" %next)
            worker[0] = offset + ord(next)-64 #'A' = 65 and should be 1
            worker[1] = next
        if worker[0] != 0:
            done = False


    if done: break

    time += 1
    print workerlist

print solution, time
print "Took %s" %str(datetime.datetime.now()-start)
