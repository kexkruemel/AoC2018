#!/usr/bin/env python2.7
import sys
import re
import numpy as np
import datetime
import copy

start = datetime.datetime.now()

def print_stars(points):
    canvas,offset = initialise_canvas(points)

    for point in points:
        canvas[point[1]-offset[1]][point[0]-offset[0]] = "#"

    for row in canvas:
        printstring = ""
        for item in row:
            printstring += item
        print printstring

    return min

def initialise_canvas(points):
    [min_x,max_x,min_y,max_y] = get_size(points)

    canvas= [["." for _ in range(min_x,max_x+1)] for _ in range(min_y,max_y+1)]
    offset = [min_x,min_y]

    return canvas,offset

def get_size(points):
    min_x = min([x[0] for x in points])
    min_y = min([x[1] for x in points])
    max_x = max([x[0] for x in points])
    max_y = max([x[1] for x in points])
    return [min_x,max_x,min_y,max_y]

def move_stars(points):
    for point in points:
        point[0] += point[2]
        point[1] += point[3]

if len(sys.argv) > 1:
    app = "test"
else:
    app = "final"

file_name = "10_" + app + ".txt"
file = open(file_name, 'r')
prog = re.compile("position=<(.*),(.*)> velocity=<(.*),(.*)>")

points = []

for line in file:
    x = int(prog.match(line).groups()[0])
    y = int(prog.match(line).groups()[1])
    vx = int(prog.match(line).groups()[2])
    vy = int(prog.match(line).groups()[3])
    points.append([x,y,vx,vy])

i = 0
while 1:
    move_stars(points)
    i += 1
    #check
    [min_x,max_x,min_y,max_y] = get_size(points)

    if max_y-min_y == 9:
        print i
        #print max_y-min_y
        break




print_stars(points)
print "Took %s" %str(datetime.datetime.now()-start)
