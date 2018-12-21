#!/usr/bin/env python3
import sys
import numpy as np
import datetime
import networkx as nx
from copy import deepcopy


start = datetime.datetime.now()

class Unit:
     def __init__(self, unit_type, x, y):
         self.unit_type = unit_type
         self.x = x
         self.y = y
         self.is_alive = True
         self.hp = 200
         self.attack_damage = 3

     def pos(self):
         return self.x, self.y

     def attack(self, damage):
         if self.is_alive:
              self.hp -= damage
              if self.hp <= 0:
                  self.is_alive = False

def neighbours(x, y):
    return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

def find_closest(G,units,c):

    enemies = [e for e in units if e.unit_type!=c.unit_type and e.is_alive]
    taken = [u.pos() for u in units]
    next_enemies = []
    dist = 1000
    G_tmp  = deepcopy(G)
    taken = [u for u in units if u.is_alive]
    for t in taken:
        if t != c: G_tmp.remove_node(t.pos())
    for e in enemies:
        for ep in neighbours(e.x,e.y):
            if ep in list(G_tmp.nodes) and ep not in taken:
                try:
                    if nx.shortest_path_length(G_tmp, c.pos(), ep) == dist:
                        dist = nx.shortest_path_length(G_tmp, c.pos(), ep)
                        next_enemies.append([e,ep])
                    elif nx.shortest_path_length(G_tmp, c.pos(), ep) < dist:
                        dist = nx.shortest_path_length(G_tmp, c.pos(), ep)
                        next_enemies= [[e,ep]]
                except nx.exception.NetworkXNoPath:
                    #print ("The way is shut")
                    e = 1
    if len(next_enemies) >0:
        next_enemies.sort(key=lambda x: (x[1][1], x[1][0])) #sort first by x value to get y-internal sorting right
        return next_enemies[0]
    else:
        return None

def move(G,c,ep,units):
    move_to = []
    G_tmp  = deepcopy(G)
    taken = [u.pos() for u in units if u.is_alive]
    for t in taken:
        G_tmp.remove_node(t)
    dist = 1000
    for g in neighbours(c.x,c.y):
        if g in list(G_tmp.nodes) and g not in taken:
            try:
                if nx.shortest_path_length(G_tmp, g, ep) == dist:
                    dist = nx.shortest_path_length(G_tmp, g, ep)
                    move_to.append(g)
                if nx.shortest_path_length(G_tmp, g, ep) < dist:
                    dist = nx.shortest_path_length(G_tmp, g, ep)
                    move_to= [g]
            except nx.exception.NetworkXNoPath:
                e = 1

    if len(move_to) >0:
        move_to.sort(key=lambda x: (x[1], x[0])) #sort first by x value to get y-internal sorting right

        c.x = move_to[0][0]
        c.y = move_to[0][1]

def print_map(map,units):
    goblins=[]
    elfs=[]
    for u in units:
        if u.unit_type == "G" and u.is_alive:
            goblins.append(u.pos())
        elif u.unit_type == "E" and u.is_alive:
            elfs.append(u.pos())

    for y in range(len(map)-1):
        line = ""
        for x in range(len(map[0])):
            if (x,y) in goblins: line += "G"
            elif (x,y) in elfs: line+= "E"
            else: line+= map[y][x]
            #line+= map[y][x]
        print (line)
    print ("\n")

def choose_attack(enemies_in_range):
    enemies_in_range.sort(key=lambda x: (x.hp, x.y, x.x))

    return enemies_in_range[0]




if len(sys.argv) > 1:
    app = "test"
else:
    app = "final"

file_name = "15_" + app + ".txt"
file = open(file_name, 'r').read()

data = []
units = []


# find units
data = [list(line) for line in file.split("\n")]
for y in range(len(data)-1):
    for x in range(len(data[0])):
        char = data[y][x]
        if char in "GE":
            units.append(Unit(char,x,y))
            data[y][x] = "."

#set up graph
G = nx.Graph()
for y in range(len(data)-1):
    for x in range(len(data[0])):
        if data[y][x] == ".":
            for (x2,y2) in neighbours(x,y):
                if 0 < x2 < len(data[0]) and 0 < y2 < len(data)-1 and data[y2][x2] == ".":
                    G.add_edge((x,y),(x2,y2))


units.sort(key=lambda x: (x.y, x.x))
print_map(data,units)
done = False
complete = 0
while 1:
    if complete %10 == 0:

        for u in units:
            print ("%s at %i,%s has %i hp" %(u.unit_type, u.x, u.y, u.hp))
        input()

    alive = [u for u in units if u.is_alive]
    for i,c in enumerate(alive):
        if c.is_alive:
            is_last = False
            if done != True:
                #move
                enemies_in_range = [e for e in units if e.unit_type!=c.unit_type and e.pos() in G[c.pos()] and e.is_alive]
                if len(enemies_in_range) ==  0:
                    next_enemy = find_closest(G,units,c) #[unit,closes point]
                    if next_enemy != None:
                        move(G,c,next_enemy[1],units)
                            #check if there are enemies left:

                #attack
                enemies_in_range = [e for e in units if e.unit_type!=c.unit_type and e.pos() in G[c.pos()] and e.is_alive]
                if len(enemies_in_range) > 0:
                    to_attack = choose_attack(enemies_in_range)
                    for e in units:
                        if e == to_attack:
                            e.attack(3)
                            break

            if len([e for e in units if e.is_alive and e.unit_type != c.unit_type]) == 0:
                if i == len(alive):
                    is_last = True
                done = True
                break
    complete += 1

    units.sort(key=lambda x: (x.y, x.x))
    print_map(data,units)
    sum_goblins = 0
    sum_elfs = 0
    # for u in units:
    #     if u.unit_type == "G" and u.is_alive: sum_goblins += u.hp
    #     elif u.unit_type == "E" and u.is_alive: sum_elfs += u.hp
    #     print ("%s at %i,%s has %i hp" %(u.unit_type, u.x, u.y, u.hp))
    if done:
        for u in units:
            if u.unit_type == "G" and u.is_alive: sum_goblins += u.hp
            elif u.unit_type == "E" and u.is_alive: sum_elfs += u.hp
            print ("%s at %i,%s has %i hp" %(u.unit_type, u.x, u.y, u.hp))
        print ("No Enemies left after iteration %i with hitpoints %i and outcome %i [%i]" %(complete, max(sum_goblins,sum_elfs), max(sum_goblins,sum_elfs)*(complete),max(sum_goblins,sum_elfs)*(complete-1)))
        break





print ("Took %s" %str(datetime.datetime.now()-start))
