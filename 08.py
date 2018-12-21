#!/usr/bin/env python2.7
import sys
import re
import numpy
import datetime
from collections import deque

def handle_node(numbers,sum):
    no_child_nodes = numbers.pop(0)
    no_meta_data = numbers.pop(0)
    for i in range(no_child_nodes): #if there are no child nodes this will not be done
        sum = handle_node(numbers,sum)

    add = get_metadata(numbers,no_meta_data)
    sum += add
    return sum

def handle_node2(numbers,val):
    no_child_nodes = numbers.pop(0)
    no_meta_data = numbers.pop(0)
    #print "This node has %i no_child_nodes and %i no_meta_data" %(no_child_nodes,no_meta_data)

    if no_child_nodes == 0:
        val = get_metadata(numbers,no_meta_data)

    else:
        child_val = []
        children = []

        for i in range(no_child_nodes):
            #print "Handling node %i" %i
            child_val.append(handle_node2(numbers,val))
        #print child_val
        for j in range(no_meta_data):
            child = numbers.pop(0)
            children.append(child)
            #print child
            if child < len(child_val)+1:
                #print ("Checking value of child %i" %child_val[child-1])
                val += child_val[child-1]

        print child_val , children
    print "This node has value %i" %val
    return val

def get_metadata(numbers,no_meta_data):
    sum = 0
    for n in range(no_meta_data):
        sum += numbers.pop(0)
    return sum

start = datetime.datetime.now()

if len(sys.argv) > 1:
    app = "test"
else:
    app = "final"

file_name = "08_" + app + ".txt"
file = open(file_name, 'r')
numbers = map(int,file.readline().split(" "))


#1
print handle_node(numbers,0)

file_name = "08_" + app + ".txt"
file = open(file_name, 'r')
numbers = map(int,file.readline().split(" "))
#2
print handle_node2(numbers,0)

print "Took %s" %str(datetime.datetime.now()-start)
