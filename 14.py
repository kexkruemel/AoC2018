#!/usr/bin/env python3
import sys
import re
import datetime
import copy

start = datetime.datetime.now()

if len(sys.argv) > 1:
    improve_after = "51589"
    test = True
else:
    improve_after = "170641"
    test = False

elf_one = 0
elf_two = 1

recipes = "37"



while 1:
    new_recipe = int(recipes[elf_one]) + int(recipes[elf_two])
    no_recipes = int((len(recipes)-2)/2)

    recipes += str(new_recipe)

    if test:
        printstring = ""
        for j,item in enumerate(recipes):
            if j == elf_one:
                printstring += "("+str(item)+")" + " "
            elif j == elf_two:
                printstring += "["+str(item)+"]" + " "
            else:
                printstring += str(item)+ " "

    elf_one = (elf_one + 1 + int(recipes[elf_one]))%len(recipes)
    elf_two = (elf_two + 1 + int(recipes[elf_two]))%len(recipes)

    #print (printstring)
    if len(recipes)%100000  == 0:
        print (len(recipes))

    #if len(recipes) > no_recipes+10:
    solution = ""
    for d in recipes[no_recipes:no_recipes+10]:
        solution += str(d)
    #print (solution)
    #print (solution.find(str(improve_after)))

    # if len(recipes) == (2*improve_after)+2:
    #     print (solution)
    #     break
    if solution.find(improve_after) >= 0:
        print ("Found %s in %i" %(solution,recipes.find(improve_after)))
        break




print ("Took %s" %str(datetime.datetime.now()-start))
