#!/usr/bin/env python2.7
import sys
import re
import numpy as np
import datetime

start = datetime.datetime.now()

if len(sys.argv) > 1:
    players = int(sys.argv[1])
    marble = int(sys.argv[2])

print ("Playing with %i Players to marble %i" %(players,marble))

circle = [0,1]
current = 1
points = {}

for i in range(2,marble+1):


    #print current, len(circle), circle

    if i%23 == 0:
        current = (current-7)%len(circle)
        won_points = i + circle[current]
        #print ("Player %i gets %i+%i points" %(i%players,i,circle[current]))
        circle = circle[:current] + circle[current+1:]
        if i%players not in points:
            points[i%players] = won_points
        else:
            points[i%players] += won_points

    else:
        #add to circle
        current = (current + 2)%len(circle)
        if current != 0:
            circle = circle[:current] + [i] + circle[current:]
        else:
            circle = circle + [i]
            current = len(circle)-1

    if i%5000 == 0:
        print i
        winner = max(points, key=points.get)
        #print ("Winner after %i marbles is player %i with %i points" %(i,winner,points[winner]))

#print points
winner = max(points, key=points.get)
print ("Winner is player %i with %i points" %(winner,points[winner]))

print "Took %s" %str(datetime.datetime.now()-start)
