#!/usr/bin/env python2.7
import sys
import datetime
from operator import itemgetter

if len(sys.argv) > 1:
    app = "test"
else:
    app = "final"

file_name = "004_" + app + ".txt"

xmax = 0
ymax = 0

min_vals = []
size_vals = []

file = open(file_name, 'r')

data = []

for line in file:
    date = line.split(" ")[0].strip("[")
    y = int(date.split("-")[0])
    m = int(date.split("-")[1])
    d = int(date.split("-")[2])

    time = line.split(" ")[1].strip("]")
    hou = int(time.split(":")[0])
    min = int(time.split(":")[1])

    text = line.split(" ")[2:]

    data.append([datetime.datetime(y,m,d,hou,min), text])

data.sort()

guards = {}
curr_guard = 0

for item in data:
    if item[1][0] == "Guard":
        # guard change
        curr_guard =  int(item[1][1][1:])
        state = 0 #awake
        state_time = 0

        if curr_guard not in guards:
            guards[curr_guard] = [0 for _ in range(60)]
    else:
        # save times
        old_state_time = state_time
        state_time = item[0].minute #only need minutes
        for i in range(old_state_time,state_time):
            guards[curr_guard][i] += state
         #save new awake state_time
        if item[1][0] == "wakes":
            state = 0 #awake
        if item[1][0] == "falls":
            state = 1 #asleep

max = 0
max_guard = 0

# check most minutes asleep
for item in guards:
    hours = sum(guards[item])
    if hours > max:
        max = hours
        max_guard = item

#check max from this guard
max = 0
max_hour = 0
for i in range(len(guards[max_guard])):
    if guards[max_guard][i] > max:
        max = guards[max_guard][i]
        max_hour = i
print max_hour*max_guard

max = 0
max_hour = 0
max_guard = 0
for item in guards:
    for i in range(len(guards[item])):
        if guards[item][i] > max:
            max = guards[item][i]
            max_hour = i
            max_guard = item

print max_hour*max_guard
