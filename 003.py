#!/usr/bin/env python2.7
import sys

if len(sys.argv) > 1:
    app = "test"
else:
    app = "final"

file_name = "003_" + app + ".txt"

xmax = 0
ymax = 0

min_vals = []
size_vals = []

file = open(file_name, 'r')

for line in file:
    min_vals_temp = line.split(" ")[2].strip(":").split(",")
    size_vals_temp = line.split(" ")[3].strip("\n").split("x")

    min_vals.append([int(i) for i in min_vals_temp])
    size_vals.append([int(i) for i in size_vals_temp])

    xmax = max(min_vals[-1][0] + size_vals[-1][0],xmax)
    ymax = max(min_vals[-1][1] + size_vals[-1][1], ymax)

fabric = [[0 for _ in range(ymax)] for _ in range(xmax)]

#iterate through all claims
for i in range(len(min_vals)):
    # iterate through list items
    for x in range(min_vals[i][0], min_vals[i][0] + size_vals[i][0]):
        for y in range(min_vals[i][1], min_vals[i][1] + size_vals[i][1]):
            fabric[x][y] += 1

overlap = 0
for line in fabric:
    for item in line:
        if item > 1: overlap += 1

print overlap

for i in range(len(min_vals)):
    # iterate through list items
    stop = 0
    for x in range(min_vals[i][0], min_vals[i][0] + size_vals[i][0]):
        for y in range(min_vals[i][1], min_vals[i][1] + size_vals[i][1]):
            if fabric[x][y] != 1:
                stop = 1
    if stop == 0: print min_vals[i]
