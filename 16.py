#!/usr/bin/env python3
import sys
import re
import numpy as np
from copy import deepcopy

import datetime


start = datetime.datetime.now()

if len(sys.argv) > 1:
    app = "test"
else:
    app = "final"

def compute_instruction(instruction,before,A,B,C):
    #addr (add register) stores into register C the result of adding register A and register B.
    if instruction == "addr":
        return before[0:C] + [before[A] + before[B]] + before[C+1:]

    #addi (add immediate) stores into register C the result of adding register A and value B.
    if instruction == "addi":
        return before[0:C] + [before[A]+B] + before[C+1:]

    #mulr (multiply register) stores into register C the result of multiplying register A and register B.
    if instruction == "mulr":
        return before[0:C] + [before[A] * before[B]] + before[C+1:]

    #muli (multiply immediate) stores into register C the result of multiplying register A and value B.
    if instruction == "muli":
        return before[0:C] + [before[A]*B] + before[C+1:]

    #banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
    if instruction == "banr":
        return before[0:C] + [before[A] & before[B]] + before[C+1:]

    #bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
    if instruction == "bani":
        return before[0:C] + [before[A]&B] + before[C+1:]

    #borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
    if instruction == "borr":
        return before[0:C] + [before[A] | before[B]] + before[C+1:]

    #bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
    if instruction == "bori":
        return before[0:C] + [before[A]|B] + before[C+1:]

    #setr (set register) copies the contents of register A into register C. (Input B is ignored.)
    if instruction == "setr":
        return before[0:C] + [before[A]] + before[C+1:]

    #seti (set immediate) stores value A into register C. (Input B is ignored.)
    if instruction == "seti":
        return before[0:C] + [A] + before[C+1:]

    #gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
    if instruction == "gtir":
        if A > before[B]:
            set = 1
        else: set = 0
        return before[0:C] + [set] + before[C+1:]

    #gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
    if instruction == "gtri":
        if before[A] > B:
            set = 1
        else: set = 0
        return before[0:C] + [set] + before[C+1:]

    #gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
    if instruction == "gtrr":
        if before[A] > before[B]:
            set = 1
        else: set = 0
        return before[0:C] + [set] + before[C+1:]

    #eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
    if instruction == "eqir":
        if A == before[B]:
            set = 1
        else: set = 0
        return before[0:C] + [set] + before[C+1:]

    #eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
    if instruction == "eqri":
        if before[A] == B:
            set = 1
        else: set = 0
        return before[0:C] + [set] + before[C+1:]

    #eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
    if instruction == "eqrr":
        if before[A] == before[B]:
            set = 1
        else: set = 0
        return before[0:C] + [set] + before[C+1:]



def check_instruction(before, instruction, after,possibilities,instruction_list):
    Opcode = instruction[0]
    A = instruction[1]
    B = instruction[2]
    C = instruction[3]

    count = 0

    for name in instruction_list:
        if after == compute_instruction(name,before,A,B,C):
            count +=1
        else:
            if name in possibilities[Opcode]: possibilities[Opcode].remove(name)

    return count



file_name = "16_" + app + ".txt"
file = open(file_name, 'r')

instr=[ re.compile(r"Before: \[(.), (.), (.), (.)") ,
        re.compile(r"(.*) (.) (.) (.)"),
        re.compile(r"After:  \[(.), (.), (.), (.)"),
        0]
more_than_three = 0

instruction_list = ["addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori", "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr"]
possibilities = {i:deepcopy(instruction_list) for i in range(len(instruction_list))}

code = False
lines = []

for i,line in enumerate(file):
    if code == False and i%4 != 3:
        if instr[i%4].match(line) == None:
            code = True #now begins code part
        else:
            #print (list(map(int,instr[i%4].match(line).groups())))
            if i%4 == 0: #begin
                before = list(map(int,instr[i%4].match(line).groups()))
            elif i%4 == 1:
                instruction = list(map(int,instr[i%4].match(line).groups()))
            elif i%4 == 2:
                after = list(map(int,instr[i%4].match(line).groups()))
                #print (before,instruction,after)
                if (check_instruction(before, instruction, after,possibilities,instruction_list)) >=3:
                    more_than_three += 1
    elif code == True:
        if instr[1].match(line) != None:
            lines.append(list(map(int,instr[1].match(line).groups())))

print (more_than_three)
#print (possibilities)

#sort out possibilities:
while 1:
    one_left = False
    for key in possibilities:
        if len(possibilities[key]) == 1: #which means that this one is set
            to_delete = possibilities[key][0]
            #print ("delete %s fom other than %i" %(to_delete, key))
            for key2 in possibilities:
                if key != key2 and to_delete in possibilities[key2]:
                    possibilities[key2].remove(to_delete)
        elif  len(possibilities[key]) > 1:
            one_left = True
    if not one_left: break
    #print (possibilities)

print (possibilities)

register = [0,0,0,0]
for line in lines:
    instruction = possibilities[line[0]]
    #print (instruction[0])
    A = line[1]
    B = line[2]
    C = line[3]
    register = compute_instruction(instruction[0],register,A,B,C)

print (register)

print ("Took %s" %str(datetime.datetime.now()-start))
