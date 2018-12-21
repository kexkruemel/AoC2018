#!/usr/bin/env python2.7
import sys
import datetime
from operator import itemgetter
import datetime

start = datetime.datetime.now()

def react(data):
    while 1:
        old_size = len(data)
        for i in range(97,123):
            data = data.replace((chr(i)+chr(i-32)), "")
            data = data.replace(chr(i-32)+chr(i), "")
        if len(data) == old_size: #no more deletes
            return data

if len(sys.argv) > 1:
    app = "test"
else:
    app = "final"

file_name = "005_" + app + ".txt"

#1
file = open(file_name, 'r')
data = file.readline().strip("\n")
min_len = len(data) # for #2
data = react(data)
print len(data)

#2
file = open(file_name, 'r')

for i in range(97,123):
    file.seek(0)
    data = file.readline().strip("\n")
    data = data.replace(chr(i), "") #remove lowercase char
    data = data.replace(chr(i-32), "") #remove uppercase char
    data = react(data)
    if len(data) < min_len:
        print "New min for char %c: %i" %(chr(i),len(data))
        min_len = len(data)

print min_len
print "Took %s" %str(datetime.datetime.now()-start)
