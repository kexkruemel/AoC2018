#!/usr/bin/env python2.7
import sys
import numpy
import datetime
from operator import itemgetter

def dist(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

start = datetime.datetime.now()

if len(sys.argv) > 1:
    app = "test"
    sumthreshold = 32
else:
    app = "final"
    sumthreshold = 10000

file_name = "006_" + app + ".txt"
file = open(file_name, 'r')
coordinates = []
for line in file:
    coordinates.append(map(int,line.split(","))+[0])

min_corner =  [min([x[0] for x in coordinates]),min([x[1] for x in coordinates])]
max_corner =  [max([x[0] for x in coordinates]),max([x[1] for x in coordinates])]

inregion = 0

#loop through all interesting fields
for x in range(min_corner[0],max_corner[0]+1):
        for y in range(min_corner[1],max_corner[1]+1):
            #loop through points and find distace
            closest = numpy.Inf
            distance = numpy.Inf
            distsum = 0 #2
            for i,point in enumerate(coordinates):
                curr_distance = dist(point,[x,y])
                distsum += curr_distance
                if curr_distance == distance:
                    closest = -numpy.Inf #no point closest
                elif curr_distance < distance:
                    closest = i
                    distance = curr_distance
            #print "Distsum = %i" %distsum
            if distsum < sumthreshold:
                inregion += 1

            if closest != -numpy.Inf:
                if ((x == min_corner[0]) | (x == max_corner[0]) | (y == min_corner[1]) | (y == max_corner[1])):
                    #is corner an goe to inf
                    coordinates[closest][2] = -numpy.Inf
                if coordinates[closest][2] != -numpy.Inf:
                    coordinates[closest][2] += 1

print "Biggest non-inf area: %i" %max([x[2] for x in coordinates])
print "Cells with distance under threshold: %i" %inregion
print "Took %s" %str(datetime.datetime.now()-start)
