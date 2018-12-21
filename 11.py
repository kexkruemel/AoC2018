#!/usr/bin/env python2.7
import sys
import re
import numpy as np
import datetime
import copy

start = datetime.datetime.now()

if len(sys.argv) > 1:
    serial = 18
else:
    serial = 9221

grid = [[0 for _ in range(300)] for _ in range(300)]

for y,row in enumerate(grid):
    for x,cell in enumerate(row):
        rack_id = x+10
        powerlevel = rack_id * y
        powerlevel += serial
        powerlevel *= rack_id
        powerlevel = (powerlevel%1000 - powerlevel%100)/100
        powerlevel -= 5

        grid[x][y] = powerlevel

max = 0
max_coords=[0,0]

for x in range(298):
    for y in range(298):
        power = sum(grid[x][y:y+3]) + sum(grid[x+1][y:y+3]) + sum(grid[x+2][y:y+3])
        if power > max:
            max = power
            max_coords = [x,y]
            print ("Found new max of %i at coordinates %s" %(max,max_coords))

max = 0
max_coords=[0,0]
max_size = 0

for i in range(300):
    print "Check for size %i" %i
    for x in range(300-i):
        for y in range(300-i):
            power = 0
            for j in range(i):
                power += sum(grid[x+j][y:y+i])
            if power > max:
                max = power
                max_coords = [x,y]
                max_size = i
                print ("Found new max of %i at coordinates %s with size %i" %(max,max_coords,max_size))

print "Took %s" %str(datetime.datetime.now()-start)
