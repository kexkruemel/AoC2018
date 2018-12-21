#!/usr/bin/env python3
import sys
import re
import numpy as np
from copy import deepcopy

import datetime


start = datetime.datetime.now()

if len(sys.argv) > 1:
    steps = int(sys.argv[1])
else:
    steps = 30

app = "final"

def printcave(cave,save = False):
    if save:
        file = open("outfile.txt", 'w')
    for line in cave:
        printstring = ""
        for i,char in enumerate(line):
            if i > 450:
                printstring  += char
        if save: file.write(printstring + "\n")
    else: print (printstring)


def set_stream(cave,pos):
    cave[pos[1]][pos[0]] = "|"

def set_water(cave,pos):
    cave[pos[1]][pos[0]] = "~"

def get_item(cave,pos):
    return cave[pos[1]][pos[0]]

def fill(cave,pos, streams, streamid, dir):
    if dir == -1:
        print ("fill left")
    elif dir == +1:
        print ("fill right")
    else:
        print ("Invalid dir")
        return False #no overflow
    next_pos = deepcopy(pos)
    while 1:
        next_pos = (next_pos[0]+dir,next_pos[1])
        if get_item(cave,next_pos) == ".": #sand =>
            set_water(cave,next_pos)
            if (get_item(cave,(next_pos[0]+dir,next_pos[1]+1)) != "#") and (get_item(cave,(next_pos[0],next_pos[1]+1)) == "#"): #there's a  wall or already water
                print ("overflow")
                streams.append((next_pos[0]+dir,next_pos[1]))
                set_stream(cave,(next_pos[0]+dir,next_pos[1]))
                return True # overflow
        elif get_item(cave,next_pos) == "|": #delete this stream and return to other one
            set_water(cave,next_pos)
            if get_item(cave,(pos[0],pos[1]-1)) != "|":#if is top of stream delete this one
                print ("Reached top of stream")
                del streams[streamid] #remove this stream
            if next_pos not in streams: streams.append(next_pos) #add the old stream
            return False # no overflow
        else:
            return False #no overflow

file_name = "17_" + app + ".txt"
file = open(file_name, 'r')

search = re.compile(r"(.)=(.*), (.)=(.*)\.\.(.*)")

instructions = []

for line in file:
    instructions.append(search.match(line).groups())

#make canvas
x_max = max([int(i[1]) for i in instructions if i[0] == "x"] + [int(i[4]) for i in instructions if i[2] == "x"])
y_max = max([int(i[1]) for i in instructions if i[0] == "y"] + [int(i[4]) for i in instructions if i[2] == "y"])
print (x_max,y_max)

cave = [["." for _ in range(x_max+1)] for _ in range(y_max+1)]

#add clay
for item in instructions:
    if item[0] == "x":
        xmax = xmin = int(item[1])
        ymin = int(item[3])
        ymax = int(item[4])
    elif item[0] == "y":
        ymax = ymin = int(item[1])
        xmin = int(item[3])
        xmax = int(item[4])
    for x in range(xmin,xmax+1):
        for y in range (ymin,ymax+1):
            cave[y][x] = "#"

set_stream(cave,(500,0))

streams = [(500,0)]

for i in range(steps):
    for n,pos in enumerate(streams):
        overflow = False
        set_stream(cave,pos)
        next_pos = (pos[0],pos[1]+1)
        if next_pos[1] > y_max:
            del streams[n]
            break
        if get_item(cave,next_pos) == ".": #stream trickels down
            streams[n] = next_pos
        elif get_item(cave,next_pos) == "#" or get_item(cave,next_pos) == "~": #stream fills up
            #print ("fill")
            overflow = False
            if fill(cave, pos, streams, n, -1): #left
                overflow = True
            if fill(cave, pos, streams, n, +1): #right
                overflow = True

            if overflow:
                set_water(cave,pos)
                del streams[n]
            if not overflow:
                #set back stream by one
                set_water(cave,pos)
                streams[n] = (pos[0],pos[1]-1)

    print streams
    if len(streams) == 0:
        break


printcave(cave,True)





print ("Took %s" %str(datetime.datetime.now()-start))
