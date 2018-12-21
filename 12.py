#!/usr/bin/env python2.7
import sys
import re
import numpy as np
import datetime
import copy

start = datetime.datetime.now()

if len(sys.argv) > 1:
    app = "test"
else:
    app = "final"

file_name = "12_" + app + ".txt"
file = open(file_name, 'r')
initial = re.compile("initial state: (.*)")
mapping = re.compile("(.*) => (.*)")

rules={}

for line in file:
    if initial.match(line) is not None:
        plants = initial.match(line).groups()[0]
    elif mapping.match(line)is not None:
        rules[mapping.match(line).groups()[0]] = mapping.match(line).groups()[1]

index = 0
end = False
last_count = 0

for n in range(1,1000):

    #prepend and append if needed
    if "#" in plants[:4]:
        plants = "...." + plants
        index += 4
    if plants[:6] == "......":
        plants= plants[4:]
        index -= 4
    if "#" in plants[-5:]:
        plants =  plants + "...."
    new_plants = ["." for _ in range(len(plants))]

    #do mapping
    for i in range(2,len(plants)-2):
        if  plants[i-2:i+3] in rules:
            new_plants[i] = rules[plants[i-2:i+3]]
        else:
            new_plants[i] = "."

    #convert to string
    str = ""
    count = 0
    for i,item in enumerate(new_plants):
        str += item
        if item == "#": count +=(i-index)


    if n%100 == 0 or n == 20:
        print "Count = %i after %i steps - diff to last is %i" %(count, n, count - last_count)
        last_count = count


    if plants == str:
        break

    plants = copy.deepcopy(str)
    n += 1


print str
print count
