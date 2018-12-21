#!/usr/bin/env python2.7
import sys
import datetime


start = datetime.datetime.now()

if len(sys.argv) > 1:
    app = "test"
else:
    app = "final"

file_name = "13_" + app + ".txt"
file = open(file_name, 'r')

directions = {"r":[1,0], "l":[-1,0], "u":[0,-1], "d":[0,1]}


def move(carts,track):
    turn_left = {"u":"l", "d":"r", "r":"u", "l":"d"}
    turn_right = {"u":"r", "d":"l", "r":"d", "l":"u"}
    carts.sort()
    for i,cart in enumerate(carts):
        is_crash = False

        new_pos =  [cart[0] + directions[cart[2]][0], cart[1] + directions[cart[2]][1]]

        if track[new_pos[1]][new_pos[0]] == "+":
            if cart[3] == 0:
                cart[2] = turn_left[cart[2]]
            if cart[3] == 2:
                cart[2] = turn_right[cart[2]]
            cart[3] = (cart[3]+1)%3 #three possible turning options
        elif track[new_pos[1]][new_pos[0]] == "/":
            if cart[2] == "r" or cart[2] == "l":
                cart[2] = turn_left[cart[2]]
            else:
                cart[2] = turn_right[cart[2]]
        elif track[new_pos[1]][new_pos[0]] == '\\':
            if cart[2] == "u" or cart[2] == "d":
                cart[2] = turn_left[cart[2]]
            else:
                cart[2] = turn_right[cart[2]]
        elif track[new_pos[1]][new_pos[0]] == ' ':
            print ("ERROR at %s" %str([new_pos[1],new_pos[0]]))

        cart[0:2] = new_pos

        for i in range(len(carts)):
            for j in range(i+1,len(carts)):
                if carts[i][0:2] == carts[j][0:2]:
                    print "CRASH at %s" %(carts[j][0:2])
                    is_crash = True
                    carts = carts[:i] + carts[i+1:j]  + carts[j+1:]

                    print "%i carts left" %len(carts)
                    if len(carts) == 1:
                        return carts
                    break


    return carts

track=[]
carts=[]

for y,line in enumerate(file):
    line = list(line.strip("\n"))
    track.append(line)
    for x,char in enumerate(line):
        if char == ">":
            carts.append([x,y,"r",0])
            line[x] = "-"
        elif char == "<":
            carts.append([x,y,"l",0])
            line[x] = "-"
        elif char == "^":
            carts.append([x,y,"u",0])
            line[x] = "|"
        elif char == "v":
            carts.append([x,y,"d",0])
            line[x] = "|"

output = open("output.txt",'a')

while True:
    # for cart in carts:
    #     output.write(str(cart[0:2]) + "\n")
    #raw_input()
    carts = move(carts,track)
    if len(carts) == 1:
        break

print ("Took %s" %str(datetime.datetime.now()-start))
