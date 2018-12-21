#!/usr/bin/env python2.7
import sys
import re
import numpy as np
import datetime
from collections import deque

start = datetime.datetime.now()

if len(sys.argv) > 1:
    players = int(sys.argv[1])
    marble = int(sys.argv[2])

print ("Playing with %i Players to marble %i" %(players,marble))

circle = deque([0])
points = {}

for i in range(1,marble+1):


    #print current, len(circle), circle

    if i%23 == 0:
        circle.rotate(-7)
        won_points = i + circle.pop()
        #print ("Player %i gets %i+%i points" %(i%players,i,circle[current]))
        if i%players not in points:
            points[i%players] = won_points
        else:
            points[i%players] += won_points

    else:
        #add to circle
        circle.rotate(2)
        circle.append(i)

    # if i%5000 == 0:
    #     print i
    #     winner = max(points, key=points.get)
        #print ("Winner after %i marbles is player %i with %i points" %(i,winner,points[winner]))

#print points
winner = max(points, key=points.get)
print ("Winner is player %i with %i points" %(winner,points[winner]))

print "Took %s" %str(datetime.datetime.now()-start)
