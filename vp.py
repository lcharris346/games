#!C:\Program Files\Python312\python
from ast import Add
from inspect import stack
import random
import copy
import argparse
from select import select
import time
import os
import sys
import matplotlib.pyplot as plt
import statistics

# Constants         1    2    3    4    5    6    7    8    9   10   11   12   13          
STACK_ELEMENTS=(    "2s","3s","4s","5s","6s","7s","8s","9s","Ts","Js","Qs","Ks","As",   
                #  14   15   16   17   18   19   20   21   22   23   24   25   26    
                "2d","3d","4d","5d","6d","7d","8d","9d","Td","Jd","Qd","Kd","Ad",
#                  27   28   29   30   31   32   33   34   35   36   37   38   39            
                "2c","3c","4c","5c","6c","7c","8c","9c","Tc","Jc","Qc","Kc","Ac",   
                 # 40   41   42   43   44   45   46   47   48   49   50   51   52       
                "2h","3h","4h","5h","6h","7h","8h","9h","Th","Jh","Qh","Kh","Ah")
STACK_ELEMENTS_DICT = { x:ii+1 for ii,x in enumerate(STACK_ELEMENTS)}
STACK=list(range(1,53))
PRIORITIES= list(range(2,15)) + list(range(2,15)) + list(range(2,15)) + list(range(2,15))
CATEGORIES=[1]*13 + [2]*13 + [3]*13 + [4]*13
    
UPDATED_SET = {"numbers": None, "sorted_numbers": None, "elements": None, "priorities": None, "sorted_priorities": None, "priorities_diffs": None, "num_zeros": 0, "num_ones": None,
                  "categories": None, "sorted_categories": None, "nume_zeros_categories": None, "sorted_numbers_categories": None,
                  "name": None, "value": 0, "addition": 0, "total_value": 0}

STACK_TYPE_HIST = {" rf": 0, " sf":  0,
                     "  q":  0, "qak":  0, " qa": 0, "qlk": 0, " ql": 0, 
                     " fh":   0, " fl":   0, "str":  0, "3ok":  0, "2pr":  0, "job": 5, " hc": 0}

VALUETABLE = {}
VALUETABLE["job"] = {" rf": 4000, " sf":  250,
                     "  q":  125, "qak":  125, " qa": 125, "qlk": 125, " ql": 125, 
                     " fh":   40, " fl":   25, "str":  20, "3ok":  15, "2pr":  10, "job": 5, " hc": 0}

VALUETABLE["b"] =   {" rf": 4000, " sf":  250,
                     "  q":  125, "qak":  400, " qa": 400, "qlk": 200, " ql": 200, 
                     " fh":   40, " fl":   25, "str":  20, "3ok":  15, "2pr":  10, "job": 5, " hc": 0}

VALUETABLE["bd"] =   {" rf": 4000, " sf":  250,
                     "  q":  400, "qak":  400, " qa": 400, "qlk": 400, " ql": 400, 
                     " fh":   40, " fl":   25, "str":  20, "3ok":  15, "2pr":  5, "job": 5, " hc": 0}

VALUETABLE["db"] = { " rf": 4000, " sf":  250,
                     "  q":  250, "qak":  800, " qa": 800, "qlk": 400, " ql": 400, 
                     " fh":   40, " fl":   25, "str":  20, "3ok":  15, "2pr":   5, "job": 5, " hc": 0}

VALUETABLE["ddb"] = {" rf": 4000, " sf":  250,
                     "  q":  250, "qak": 2000, " qa": 800, "qlk": 800, " ql": 400, 
                     " fh":   40, " fl":   25, "str":  20, "3ok":  15, "2pr":   5, "job": 5, " hc": 0}

VALUETABLE["tdb"] = {" rf": 4000, " sf":  250,
                     "  q":  250, "qak": 4000, " qa": 800, "qlk": 2000, " ql": 400, 
                     " fh":   40, " fl":   25, "str":  20, "3ok":  10, "2pr":   5, "job": 5, " hc": 0}

MAX_COST = {"cl": 5, "sptrp": 6, "stp": 6, "dstp": 7, "sstk": 10, "pstk": 10,"ultx": 10,  "fhpw": 10, "majm": 10, "php": 10, "drmcd": 10 }

CHOICES = ("", "1", "2", "3", "4", "5", "a")
NUM_SETS = (3,5,10)

KEYBOARD_CHOICES = {"c":1,"v":2,"b":3,"n":4,"m":5}
KEYBOARD_CHOICES_KEYS = KEYBOARD_CHOICES.keys()

EXIT = ("q", "quit", "e", "exit")

ADDITION = {}
ADDITION["fhpw"] = {"values": [175]*10 + [1000]*5 + [225]*25 + [150]*8 + [300]*18 + [125]*8 + [2000] + [350]*27 + [100]*10 + [500]*9 + [275]*20}
ADDITION["stp"] = {"values": [2]*81 + [3]*155 + [4]*62 +[5]*91 + [8]*34 + [10]*17}
ADDITION["sstk"] = {3:range(3,10),5:range(4,17),10:range(10,31)}
ADDITION["pstk"] = {1:{2:1,3:2},3:{2:3,3:5}, 5:{2: 4, 3: 6}, 10: {2: 6, 3: 10}}

ADDITION["ultx"] = {}
ADDITION["ultx"][3] = {" rf": 2, " sf":  2,
                     "  q":  2, "qak": 2, " qa": 2, "qlk": 2, " ql": 2, 
                     " fh":   12, " fl":   10, "str":  8, "3ok":  4, "2pr":   3, "job": 2, " hc": 1}

ADDITION["ultx"][5] = {" rf": 2, " sf":  2,
                     "  q":  3, "qak": 2, " qa": 2, "qlk": 2, " ql": 2, 
                     " fh":   12, " fl":   10, "str":  8, "3ok":  4, "2pr":   3, "job": 2, " hc": 1}

ADDITION["ultx"][10] = {" rf": 4, " sf":  4,
                     "  q":  3, "qak": 4, " qa": 4, "qlk": 4, " ql": 4, 
                     " fh":   12, " fl":   10, "str":  8, "3ok":  4, "2pr":   3, "job": 2, " hc": 1}

ADDITION["majm"] = {
                        "  q": [2]*49  + [4]*24   + [6]*19   + [8]*6 + [10]*2, 
                        "qak": [2]*49  + [4]*24   + [6]*19   + [8]*6 + [10]*2, 
                        " qa": [2]*49  + [4]*24   + [6]*19   + [8]*6 + [10]*2, 
                        "qlk": [2]*49  + [4]*24   + [6]*19   + [8]*6 + [10]*2, 
                        " ql": [2]*49  + [4]*24   + [6]*19   + [8]*6 + [10]*2, 
                        " fh": [2]*49  + [4]*24   + [7]*19   + [15]*6 + [80]*2, 
                        "3ok": [2]*2  + [5]*5   + [8]*8   + [20]*20 + [100]*100, 
                        "2pr": [2]*49 + [6]*24  + [10]*19 + [30]*6  + [100]*2, }
ADDITION["sptrp"] = {}
ADDITION["sptrp"]["job"] = {"qak":4, " qa":4, "qlk":4, " ql":4, "  q":4}
ADDITION["sptrp"]["b"]   = {"qak":3, " qa":3, "qlk":3, " ql":3, "  q":3.2}
ADDITION["sptrp"]["bd"] =  {"qak":2, " qa":2, "qlk":2, " ql":2, "  q":2}
ADDITION["sptrp"]["db"] =  {"qak":2.5, " qa":2.5, "qlk":2.5, " ql":2.5, "  q":2}
ADDITION["sptrp"]["ddb"] = {"qak":2, " qa":2, "qlk":2, " ql":2, "  q":2}
ADDITION["sptrp"]["tdb"] = {"qak":1, " qa":2, "qlk":2, " ql":2, "  q":2}

ADDITION["php"] = { " rf":  1, " sf":  1,
                    "  q":  1, "qak":  1, " qa":  1, "qlk":  1, " ql":  1, 
                    " fh":  6, " fl":  5, "str":  4, "3ok":  3, "2pr":  2, "job": 1  }

STR_DIFFS = ([1,1,1],[1,1,2],[1,2,1],[2,1,1])

DENOMS = (0.1, 0.25,0.5,1.0,2)

BUILD_OUT = open("sample.txt").readlines()

# Functions
def my_decorator(func):
    def wrapper(statement):
        choice = random.choice(range(len(BUILD_OUT)))
        line = str(statement).replace("'","") + BUILD_OUT[choice].rstrip()
        func(line)
    return wrapper

@my_decorator
def my_print(statement):
    print(statement)


def is_str(updated_set):
    result = (updated_set["priorities_diffs"] == [1,1,1,1] or updated_set["priorities_diffs"] == [1,1,1,9])
    return result

def is_fl(updated_set):
    result = all(x == updated_set["categories"][0] for x in updated_set["categories"])
    return result

def is_sf(updated_set):
    result =  (is_str(updated_set) and is_fl(updated_set))
    return result

def is_rf(updated_set):
    result = False
    if (is_sf(updated_set) and updated_set["sorted_priorities"][0] == 10):
        result = True
    return result

def is_q(updated_set):
    result = all((updated_set["num_zeros"] == 3,
                 updated_set["priorities_diffs"][1] == 0,
                 updated_set["priorities_diffs"][2] == 0))
    return result

def is_qa(updated_set):
    result = (is_q(updated_set) and  updated_set["sorted_priorities"][2] == 14)
    return result

def is_qak(updated_set):
    result = (is_qa(updated_set) and updated_set["sorted_priorities"][0] < 5)
    return result

def is_ql(updated_set):
    result = (is_q(updated_set) and updated_set["sorted_priorities"][2] < 5)
    return result

def is_qlk(updated_set):
    result = (is_ql(updated_set) and ((updated_set["sorted_priorities"][0] in (2,3,4,14) and updated_set["sorted_priorities"][0] != updated_set["sorted_priorities"][2]) or (updated_set["sorted_priorities"][4] in (2,3,4,14) and updated_set["sorted_priorities"][4] != updated_set["sorted_priorities"][2])))
    return result

def is_fh(updated_set):
    result = all((updated_set["num_zeros"] == 3,
                 updated_set["priorities_diffs"][0] == 0,
                 updated_set["priorities_diffs"][3] == 0))
    return result

def is_3ok(updated_set):
    result = (updated_set["num_zeros"] == 2 and \
                any((updated_set["priorities_diffs"][0] == 0 and updated_set["priorities_diffs"][1] == 0,
                    updated_set["priorities_diffs"][1] == 0 and updated_set["priorities_diffs"][2] == 0,
                    updated_set["priorities_diffs"][2] == 0 and updated_set["priorities_diffs"][3] == 0)))
    return result

def is_2pr(updated_set):
    result = (updated_set["num_zeros"] == 2 and \
                any((updated_set["priorities_diffs"][0] == 0 and updated_set["priorities_diffs"][2] == 0,
                    updated_set["priorities_diffs"][0] == 0 and updated_set["priorities_diffs"][3] == 0,
                    updated_set["priorities_diffs"][1] == 0 and updated_set["priorities_diffs"][3] == 0)))
    return result

def is_job(updated_set):
    result = False
    if is_pr(updated_set):
        seen = set()
        duplicates = set()
        for num in updated_set["sorted_priorities"]:
            if num in seen:
                duplicates.add(num)
            else:
                seen.add(num)
        result = (list(duplicates)[0] > 10)
    return result

def is_pr(updated_set):
    result = (updated_set["num_zeros"] == 1)
    return result

def get_5th_element(dealt_set_4_numbers, remaining_deck1):

        drmcd_number = remaining_deck1[0]
        drmcd_number_index = drmcd_number - 1

        dealt_set_4 = copy.deepcopy(UPDATED_SET)
        dealt_set_4["numbers"] = dealt_set_4_numbers
        dealt_set_4["name"] = get_set_data(dealt_set_4)
        my_print(("DEBUG:", dealt_set_4, STACK_ELEMENTS[drmcd_number_index]))

        select_priority = PRIORITIES[drmcd_number_index]
        select_category = CATEGORIES[drmcd_number_index]

        updated_category = False
        
        # quads
        if dealt_set_4["num_zeros"] == 3:

            quad_priority = dealt_set_4["sorted_priorities"][0]

            if quad_priority == 14:
                select_priority = 2

            elif quad_priority < 5:
                select_priority = 14

        # 4 to a royal flush
        elif dealt_set_4["category_diffs"] == [0,0,0] and dealt_set_4["sorted_priorities"][0] > 9:

            select_priority = [x for x in range(10,15) if x not in dealt_set_4["sorted_priorities"]][0]

            select_category = dealt_set_4["sorted_categories"][0]

            updated_category = True

        # 3 to a royal flush
        elif dealt_set_4["num_zeros_categories"] == 2 and dealt_set_4["sorted_priorities"][1] > 9:

            sorted_numbers = [x for ii,x in enumerate(dealt_set_4["sorted_numbers_categories"][:-1]) if dealt_set_4["category_diffs"][ii] == 0 ]

            sorted_numbers_categories = [x for ii,x in enumerate(dealt_set_4["sorted_numbers"][:-1]) if dealt_set_4["sorted_priorities"][ii] > 9 ]

            if set(sorted_numbers) == set(sorted_numbers_categories):

                select_priority = [x for x in range(10,15) if x not in dealt_set_4["sorted_priorities"]][0]

                select_category = [x for ii,x in enumerate(dealt_set_4["sorted_categories"][:-1]) if dealt_set_4["category_diffs"][ii] == 0 ][0]

            updated_category = True

        # 2 pair, trips
        elif dealt_set_4["num_zeros"] == 2:

            for ii, x in enumerate(dealt_set_4["sorted_priorities"][:-1]):

                # 2 pair
                if dealt_set_4["priorities_diffs"][ii] == 0:

                    select_priority = dealt_set_4["sorted_priorities"][ii]

                    #trips
                    if ii < 2 and dealt_set_4["priorities_diffs"][ii+1] == 0:
                         select_priority = dealt_set_4["sorted_priorities"][ii]
                         break

                    

        # pair
        elif dealt_set_4["num_zeros"] == 1:
            select_priority = [x for ii, x in enumerate(dealt_set_4["sorted_priorities"][:-1]) if dealt_set_4["priorities_diffs"][ii] == 0][0]

        

        # 4 to a str
        elif dealt_set_4["priorities_diffs"] == [1,1,1]:
            
            if dealt_set_4["sorted_priorities"][0] == 2:

                select_priority = dealt_set_4["sorted_priorities"][3] + 1

            else:

                select_priority = dealt_set_4["sorted_priorities"][0] - 1

        # 3 to a str
        elif dealt_set_4["sorted_priorities"][2] - dealt_set_4["sorted_priorities"][0] < 5:

            test_range = range(dealt_set_4["sorted_priorities"][0], dealt_set_4["sorted_priorities"][2] + 1)

            select_priorities = [x for x in test_range if x not in dealt_set_4["sorted_priorities"]]

            if len(select_priorities) > 0:

                select_priority = select_priorities[0]

            else:

                select_priority = dealt_set_4["sorted_priorities"][0] - 1 if dealt_set_4["sorted_priorities"][0] > 2 else dealt_set_4["sorted_priorities"][2] + 1


        elif dealt_set_4["sorted_priorities"][3] - dealt_set_4["sorted_priorities"][1] < 5:

            test_range = range(dealt_set_4["sorted_priorities"][1], dealt_set_4["sorted_priorities"][3] + 1)

            select_priorities = [x for x in test_range if x not in dealt_set_4["sorted_priorities"]]

            if len(select_priorities) > 0:

                select_priority = select_priorities[0]

            else:

                select_priority = dealt_set_4["sorted_priorities"][1] - 1 if dealt_set_4["sorted_priorities"][1] > 2 else dealt_set_4["sorted_priorities"][3] + 1

        # hc
        else:
            select_priority = dealt_set_4["sorted_priorities"][-1]

        if updated_category == False:
            # 4 to a flush
            if dealt_set_4["category_diffs"] == [0,0,0]:
                select_category = dealt_set_4["sorted_categories"][0]

            # 3 to a flush
            elif dealt_set_4["num_zeros_categories"] == 2:

                select_categories = [x for ii,x in enumerate(dealt_set_4["sorted_categories"][:-1]) if dealt_set_4["category_diffs"][ii] == 0]

                select_category = select_categories[0]


        # find elements with priority and category
        for potential_number in remaining_deck1:

            index = potential_number - 1
            potential_priority = PRIORITIES[index]
            potential_category = CATEGORIES[index]

            if potential_priority == select_priority:

                drmcd_number = potential_number

                if updated_category == True and potential_category == select_category:

                    break

        return drmcd_number

def get_set_data(updated_set):
    updated_set["elements"] = [STACK_ELEMENTS[x-1] for x in updated_set["numbers"]]
    updated_set["priorities"] = [PRIORITIES[x-1] for x in updated_set["numbers"] ]
    updated_set["sorted_priorities"] = sorted(updated_set["priorities"])
    updated_set["sorted_numbers"] = [ x for _, x in sorted(zip(updated_set["priorities"], updated_set["numbers"]))]
    updated_set["sorted_elements"] = [ x for _, x in sorted(zip(updated_set["priorities"], updated_set["elements"]))]
    updated_set["priorities_diffs"] = [next_element - current_element for current_element, next_element in zip(updated_set["sorted_priorities"], updated_set["sorted_priorities"][1:])]
    updated_set["num_zeros"] = len([x for x in updated_set["priorities_diffs"] if x == 0])
    updated_set["num_ones"] = len([x for x in updated_set["priorities_diffs"] if x == 1])
    updated_set["categories"] = [CATEGORIES[x-1] for x in updated_set["numbers"] ]
    updated_set["sorted_categories"] = sorted(updated_set["categories"])
    updated_set["category_diffs"] = [next_element - current_element for current_element, next_element in zip(updated_set["sorted_categories"], updated_set["sorted_categories"][1:])]
    updated_set["num_zeros_categories"] = len([x for x in updated_set["category_diffs"] if x == 0])
    updated_set["sorted_numbers_categories"] = [ x for _, x in sorted(zip(updated_set["categories"], updated_set["numbers"]))]

    return updated_set


def get_set_type(updated_set):
    updated_set = get_set_data(updated_set)
    name = " hc"
    value = 0

    if is_rf(updated_set):
        name = " rf"

    elif is_sf(updated_set):
            name = " sf"

    elif is_q(updated_set):
        name = "  q"

        if is_qa(updated_set):
            name = " qa"

            if is_qak(updated_set):
                name = "qak"

        elif is_ql(updated_set):
            name = " ql"

            if is_qlk(updated_set):
                name = "qlk"

    elif is_fh(updated_set):
        name = " fh"

    elif is_fl(updated_set):
        name = " fl"

    elif is_str(updated_set):
        name = "str"

    elif is_3ok(updated_set):
        name = "3ok"

    elif is_2pr(updated_set):
        name = "2pr"

    elif is_job(updated_set):
        name = "job"

    else:
        name = " hc"

    return name

######################################## CLASSES  ########################################
class Vp(object):
    def __init__(self, activity, addition_type, num_sets, credit, denom, automate, verbose, stack_type_hist = copy.deepcopy(STACK_TYPE_HIST)):
        self.activity = activity
        self.addition_type = addition_type
        self.credit = credit
        self.denom = denom
        self.automate = automate
        self.verbose = verbose
        self.valuetable = VALUETABLE[addition_type]
        self.multi = 1
        self.win = 0
        self.total_rtp = 0
        self.ctr = 1
        self.addition_ctr = 0
        self.acc_ctr = 0
        self.num_sets = num_sets
        self.set_multis = [0]*self.num_sets
        self.max_cost = self.denom * self.num_sets * MAX_COST[self.activity]
        self.cost = self.max_cost
        self.max_win = 0
        self.set_num_sets(num_sets)
        self.update_paytable()
        self.stack_type_hist = stack_type_hist
        my_print((self.activity, self.addition_type, self.num_sets, self.max_cost, self.credit))
        random.seed()

    def update_paytable(self):
        if self.activity == "cl":
            for key in VALUETABLE.keys():
                VALUETABLE[key][" fh"] = 45


    def set_num_sets(self, num_sets):
        self.num_sets = num_sets
        self.max_cost = self.denom * self.num_sets * MAX_COST[self.activity]
        self.cost = self.max_cost
        self.set_multis = [0]*self.num_sets
        my_print("num_sets:" + str(num_sets))

    def update_denom(self, denom):
        self.denom = denom
        self.max_cost = self.denom * self.num_sets * MAX_COST[self.activity]
        self.cost = self.max_cost

    def algorithm1(self, dealt_set):

        selection_numbers = []

        # sets
        if dealt_set["name"] in (" rf", " sf", "str", " fl"):

            selection_numbers = dealt_set["sorted_numbers"]

        # sets except pstk
        elif dealt_set["name"] in ("qak", "qlk", " fh"):

            selection_numbers = dealt_set["sorted_numbers"]

            if self.activity == "pstk": 

                    selection_numbers = [x for ii, x in enumerate(dealt_set["sorted_numbers"]) if dealt_set["sorted_priorities"][ii] == dealt_set["sorted_priorities"][2]]

        # 2pr w job except pstk
        elif dealt_set["name"] == "2pr":
       
            for ii in range(len(dealt_set["sorted_priorities"])-1):

                if dealt_set["sorted_priorities"][ii] == dealt_set["sorted_priorities"][ii + 1]:
                    n1 = dealt_set["sorted_numbers"][ii]
                    selection_numbers.append(n1)
                    
                    n2 = dealt_set["sorted_numbers"][ii + 1]
                    selection_numbers.append(n2)

            if self.activity != "pstk" and len(selection_numbers) == 4:

                new_sorted_priorities = [PRIORITIES[x-1] for x in selection_numbers]

                if new_sorted_priorities[0] > 10:

                    selection_numbers = selection_numbers[:2]

                elif new_sorted_priorities[2] > 10:

                    selection_numbers = selection_numbers[2:]

        # all repeat priorities
        elif dealt_set["name"] in ("job", "3ok", "  q", " qa", " ql"):

            for ii in range(len(dealt_set["sorted_priorities"])-1):

                if dealt_set["sorted_priorities"][ii] == dealt_set["sorted_priorities"][ii+1]:

                    if  dealt_set["sorted_numbers"][ii] not in selection_numbers:

                        selection_numbers.append(dealt_set["sorted_numbers"][ii])

                    selection_numbers.append(dealt_set["sorted_numbers"][ii + 1])

        # hc
        elif dealt_set["name"] == " hc":
            
            for ii in (4,3,2,1):
                # small pr
                if dealt_set["sorted_priorities"][ii] == dealt_set["sorted_priorities"][ii-1]:

                    selection_numbers = [dealt_set["sorted_numbers"][ii], dealt_set["sorted_numbers"][ii-1]]

                    break
                # face elements
                if len(selection_numbers) < 2 and dealt_set["sorted_priorities"][ii] > 10:

                    selection_numbers.append(dealt_set["sorted_numbers"][ii])

            # 3 to a rf
            if dealt_set["sorted_priorities"][2] > 9:
                    
                categories = [CATEGORIES[x-1] for x in dealt_set["sorted_numbers"][2:]]

                if ( categories[0] == categories[1] and categories[0] == categories[2]):

                    selection_numbers = dealt_set["sorted_numbers"][2:]
            
            # 4 to fl
            if len(selection_numbers) == 0 and dealt_set["num_zeros_categories"] > 2:

                    selection_numbers = dealt_set["sorted_numbers_categories"][1:4]

                    if (dealt_set["sorted_categories"][0] == dealt_set["sorted_categories"][2]):

                        selection_numbers.append(dealt_set["sorted_numbers_categories"][0])

                    else:

                        selection_numbers.append(dealt_set["sorted_numbers_categories"][4])

            # 4 to str
            if len(selection_numbers) == 0 and dealt_set["num_ones"] > 1:

                if dealt_set["priorities_diffs"][:-1] in STR_DIFFS:

                    selection_numbers = dealt_set["sorted_numbers"][:-1]

                elif dealt_set["priorities_diffs"][1:] in STR_DIFFS:

                    selection_numbers = dealt_set["sorted_numbers"][1:]

            # 3 to a sf
            if len(selection_numbers) == 0:

                for ii in range(3):
                    
                    sorted_numbers = dealt_set["sorted_numbers"][ii:ii+3]
                    sorted_priorities = dealt_set["sorted_priorities"][ii:ii+3]
                    sorted_categories = [CATEGORIES[x-1] for x in sorted_numbers]

                    if all((sorted_categories[0] == sorted_categories[1], 
                            sorted_categories[0] == sorted_categories[2],
                            sorted_priorities[0] == sorted_priorities[1] - 1,
                            sorted_priorities[1] == sorted_priorities[2] - 1,
                    )):

                        selection_numbers = sorted_numbers
                        break

            # lowest rank
            if len(selection_numbers) == 0 and dealt_set["sorted_priorities"][0] < 5:

                    selection_numbers.append(dealt_set["sorted_numbers"][0])



        return selection_numbers
       
    def get_value_cl(self):
        value = 0
        if self.verbose:
            time.sleep(0.1)
        return value

    def get_value_majm(self, addition, name):
        value = 1
        if name in addition.keys():
            value = addition[name]
            if self.verbose:
                time.sleep(0.5)
        return value
    
    def get_value_sptrp(self, addition, name):
        value = 1
        if name in addition.keys():
            value = addition[name]
            if value > 1:
                my_print((" addition"))
                #if self.verbose:
                #    input("continue...")
            if self.verbose:
                time.sleep(0.5)
        return value

    def get_value_ultx(self, name):
        value = ADDITION["ultx"][self.num_sets][name]
        return value
 
    def get_value_fhpw(self, updated_set):

        value = 0
        if updated_set["value"] >= self.valuetable[" fh"]:
            my_print((" addition"))
            addition_values = copy.deepcopy(ADDITION["fhpw"]["values"])
            random.shuffle(addition_values)
            if updated_set["value"] > self.valuetable[" fh"]:
                my_print(("  boost"))
                addition_values = [2*x for x in addition_values]

            if self.verbose:
                for ii in range(10):
                    time.sleep(0.1)
                    #os.system("cls")
                    my_print(addition_values[ii])
                time.sleep(0.5)

            value = addition_values[9]
            my_print((value))
            
        return value
    
    def get_value_stp(self):

        multi = 1
        draw = random.choice(range(15))
        
        if draw == 14:
            my_print((" addition"))
            addition_values = copy.deepcopy(ADDITION["stp"]["values"])
            random.shuffle(addition_values)

            if self.verbose:
                for ii in range(10):
                    time.sleep(0.1)
                    #os.system("cls")
                    my_print(addition_values[ii])
                time.sleep(0.5)

            multi = addition_values[9]
            my_print((multi))

        return multi

    def get_value_sstk1(self):

        self.multi = 1
        draw = random.choice(range(11))
        
        if draw == 10:
            my_print((" addition"))
            addition_values = copy.deepcopy(ADDITION["stp"]["values"])
            random.shuffle(addition_values)

            if self.verbose:
                for ii in range(10):
                    time.sleep(0.1)
                    #os.system("cls")
                    my_print(addition_values[ii])
                time.sleep(0.5)

            self.multi = addition_values[9]
            my_print((self.multi))

            if self.verbose:
                time.sleep(0.1)

        return self.multi

    def get_value_sstk2(self, held_numbers, remaining_deck):

        total_value = 0

        if self.multi > 1:

            my_print((" addition2"))
            extra_sets = random.choice(ADDITION["sstk"][self.num_sets])
            num_elements2update = 5 - len(held_numbers)
           
            for i in range(extra_sets):
                
                updated_set = copy.deepcopy(UPDATED_SET)

                updated_numbers = random.sample(remaining_deck, num_elements2update)
                updated_priorities = [ PRIORITIES[x-1] for x in updated_numbers]

                updated_set["numbers"] = held_numbers + updated_numbers
                updated_set["name"] = get_set_type(updated_set)
                updated_set["value"] = self.valuetable[updated_set["name"]]*self.multi
                total_value += updated_set["value"]

                my_print((i,  " ".join(updated_set["elements"]), updated_set["name"], updated_set["value"], total_value))

                if self.verbose:
                    time.sleep(0.1)


        return total_value

    def get_value_pstk(self, init_set_name, held_numbers, remaining_deck):

        total_value = 0

        
        held_priorities = [ PRIORITIES[x-1] for x in held_numbers]
        size_held_numbers = len(held_priorities)

        eligible = all((
                self.num_sets in (1,3,5,10),
                init_set_name in ("job", "3ok", "2pr", " fh"),
                size_held_numbers in (2, 3),
                all(x == held_priorities[0] for x in held_priorities),
                (size_held_numbers == 3 or (len(held_priorities) and held_priorities[0] > 10))
        ))

        if  eligible:
            my_print((" addition"))
            extra_sets = ADDITION["pstk"][self.num_sets][size_held_numbers]
            num_elements2update = 5 - size_held_numbers
            
           
            for i in range(extra_sets):
                
                updated_set = copy.deepcopy(UPDATED_SET)

                updated_numbers = random.sample(remaining_deck, num_elements2update)
                updated_priorities = [ PRIORITIES[x-1] for x in updated_numbers]

                updated_set["numbers"] = held_numbers + updated_numbers
                updated_set["name"] = get_set_type(updated_set)
                updated_set["value"] = self.valuetable[updated_set["name"]]
                total_value += updated_set["value"]

                my_print(( " ".join(updated_set["elements"]), updated_set["name"], updated_set["value"], total_value))

                for ii, x in enumerate(updated_numbers):
                    
                    if updated_priorities[ii] == held_priorities[0]:
                        held_numbers.append(x)
                        held_priorities.append(updated_priorities[ii])
                        num_elements2update -= 1
                        remaining_deck.pop(0)

                if self.verbose:
                    time.sleep(0.1)

        return total_value

    def get_value_php(self, init_set_name, held_numbers, remaining_deck):

        total_value = 0

        
        held_priorities = [ PRIORITIES[x-1] for x in held_numbers]
        size_held_numbers = len(held_priorities)

        eligible = all((
                self.num_sets in (1,3,5,10),
                init_set_name != " hc",
        ))

        if  eligible:
            my_print((" addition"))
            extra_sets = ADDITION["php"][init_set_name] * self.num_sets
            num_elements2update = 5 - size_held_numbers
            
           
            for i in range(extra_sets):
                
                updated_set = copy.deepcopy(UPDATED_SET)

                updated_numbers = random.sample(remaining_deck, num_elements2update)
                updated_priorities = [ PRIORITIES[x-1] for x in updated_numbers]

                updated_set["numbers"] = held_numbers + updated_numbers
                updated_set["name"] = get_set_type(updated_set)
                updated_set["value"] = self.valuetable[updated_set["name"]]
                total_value += updated_set["value"]

                my_print((i, " ".join(updated_set["elements"]), updated_set["name"], updated_set["value"], total_value))

                if self.verbose:
                    time.sleep(0.1)

        return total_value

    def get_dealt_set_drmcd(self, dealt_set, deck):

        dealt_set_4_numbers = deck[:4]
        drmcd_number = deck[4]
        remaining_deck1 = deck[4:]
        addition_ctr_incr = False

        if random.choice(range(6)) == 5:
            addition_ctr_incr = True
            
            dealt_set_4_elements = [ STACK_ELEMENTS[x-1] for x in dealt_set_4_numbers]
            my_print(" addition")

            # drmcd algorithm
            drmcd_number = get_5th_element(dealt_set_4_numbers, remaining_deck1)

            my_print((" drmcd:", dealt_set_4_elements + [STACK_ELEMENTS[drmcd_number-1]]))

            if self.verbose:
                #user_input = input("continue...")
                #if user_input in ("q", "e"):
                #    sys.exit()
                time.sleep(0.5)

        dealt_set["numbers"] = dealt_set_4_numbers + [drmcd_number]
        remaining_deck = [ x for x in remaining_deck1 if x != drmcd_number ]

        return dealt_set, remaining_deck, addition_ctr_incr

          
    def run(self):

        # init
        self.win = 0
        addition = None
        addition_ctr_incr = False

        deck = copy.deepcopy(STACK)
        random.shuffle(deck)
        dealt_set = copy.deepcopy(UPDATED_SET)

        if self.activity == "drmcd":
            dealt_set, remaining_deck, addition_ctr_incr = self.get_dealt_set_drmcd(dealt_set, deck)
            if addition_ctr_incr:
                self.addition_ctr += 1
        else:
            dealt_set["numbers"] = deck[:5]
            remaining_deck = deck[5:]

            #dealt_set["numbers"] = [1,13,26,39,52] #deck[:5]
            #remaining_deck = [x for x in deck if x not in dealt_set["numbers"] ]  #deck[5:]

        dealt_set["elements"] = [STACK_ELEMENTS[x-1] for x in dealt_set["numbers"]]
        dealt_set["name"] = get_set_type(dealt_set)

        #pre-update additions
        if self.cost == self.max_cost:

            if self.activity in ("stp", "dstp"):
                self.multi = self.get_value_stp()
                if self.multi > 1 and addition_ctr_incr == False:
                    self.addition_ctr += 1
                    addition_ctr_incr = True
            elif self.activity == "sstk":
                self.multi = self.get_value_sstk1()
                if self.multi > 1 and addition_ctr_incr == False:
                    self.addition_ctr += 1
                    addition_ctr_incr = True
            elif self.activity == "cl":
                self.get_value_cl()
            elif self.activity == "majm" and dealt_set["name"]  in ( "job", "2pr", "3ok"):
                self.addition_ctr += 1
                addition = copy.deepcopy(ADDITION["majm"])
                if dealt_set["name"] in addition.keys():
                    addition.pop(dealt_set["name"])
                for key in addition.keys():
                    addition[key] = random.choice(addition[key])
                my_print("addition")
                my_print(addition)
                if self.verbose and self.automate:
                    time.sleep(0.5)


        # select elements
        my_print((" ".join(dealt_set["elements"]), dealt_set["name"]))
        held_numbers = []

        # algorithm
        held_numbers1 = self.algorithm1(dealt_set)
            #time.sleep(0.5)

        # user input
        if self.automate == True:

            held_numbers = held_numbers1

        else:

            #my_print((dealt_set))

            # select
            user_input = input()
            user_input_list = list(user_input)
        
            # error ckecking
            for ii,x in enumerate(user_input_list):

                if x == "a":

                    held_numbers = self.algorithm1(dealt_set)
                    break

                if x in KEYBOARD_CHOICES_KEYS:

                    user_input_list[ii] = KEYBOARD_CHOICES[x]
                    continue

                if x in EXIT:

                    my_print(("INFO: Exit requested", x))
                    sys.exit()

                if x not in CHOICES:

                    my_print(("ERROR: Invalid selection. Character is not 1 - 5,q,e,a: ", x))
                    return

                if x == "":

                    user_input_list = []

            if len(held_numbers) == 0:

                size_selection = len(user_input_list)

                if size_selection > 5:

                    my_print(("ERROR: Invalid selection. Too many numbers: ", user_input))
                    return
    
                if size_selection != len(set(user_input_list)):

                    my_print(("ERROR: Invalid Selection. Repeat numbers: ", user_input))
                    return
        
                selection = [int(x) for x in user_input_list]

                held_numbers = [dealt_set["numbers"][x-1] for x in selection]

        
        if set(held_numbers1) == set(held_numbers):

            self.acc_ctr += 1

        else:

            print("mismatch!", held_numbers1, held_numbers)

        # update
        #os.system("cls")

        #dEBUG: set held elements
        #held_numbers = [13, 26, 39]
        #dealt_set["name"] = "3ok"
        #deck = copy.deepcopy(STACK)
        #remaining_deck = [x for x in deck if x not in held_numbers]
        #random.shuffle(remaining_deck)


        num_elements2update = 5 - len(held_numbers)

        for i in range(self.num_sets):

            # add values
            updated_set = copy.deepcopy(UPDATED_SET)
            updated_set["numbers"] = held_numbers + random.sample(remaining_deck, num_elements2update)
            updated_set["name"] = get_set_type(updated_set)
            updated_set["value"] = self.valuetable[updated_set["name"]]

            # update counts
            self.stack_type_hist[updated_set["name"]] += 1

            # update additions
            str_multi1 = ""
            str_multi2 = ""
            updated_set["addition"] = 0

            if self.cost == self.max_cost:
                
                if self.activity == "fhpw":

                    updated_set["addition"] = self.get_value_fhpw(updated_set)

                    if addition_ctr_incr == False and updated_set["addition"] > 0:
                        self.addition_ctr += 1
                        addition_ctr_incr = True

                elif self.activity in ("stp", "dstp", "sstk"):

                    updated_set["addition"] = (self.multi - 1) * updated_set["value"]

                elif self.activity == "ultx":

                    if self.set_multis[i] > 1:

                        str_multi1 = str(self.set_multis[i]) + "x"
                        updated_set["addition"] = (self.set_multis[i] - 1) * updated_set["value"]

                        if addition_ctr_incr == False:

                            self.addition_ctr += 1
                            addition_ctr_incr = True

                    self.set_multis[i] =  self.get_value_ultx(updated_set["name"]) 

                    if self.set_multis[i] > 1:

                        str_multi2 = str(self.set_multis[i]) + "x"

                elif self.activity == "majm":

                    self.set_multis[i] = 1

                    if addition:

                        self.set_multis[i] = self.get_value_majm(addition, updated_set["name"])

                        if self.set_multis[i] > 1:

                            str_multi1 = str(self.set_multis[i]) + "x"
                            updated_set["addition"] = (self.set_multis[i] - 1) * updated_set["value"]

                elif self.activity == "sptrp":

                    multi = self.get_value_sptrp(ADDITION["sptrp"][self.addition_type], updated_set["name"])

                    if multi > 1:

                        str_multi1 = str(multi) + "x"

                        if addition_ctr_incr == False:

                            self.addition_ctr += 1
                            addition_ctr_incr = True

                        updated_set["addition"] = (multi - 1) * updated_set["value"]

                elif self.activity == "cl":

                    if updated_set["value"] >= 125:
                        if addition_ctr_incr == False:
                            self.addition_ctr += 1
                            addition_ctr_incr = True

            # update total value
            updated_set["total_value"] = updated_set["value"] + updated_set["addition"]

            # update win
            self.win += updated_set["total_value"]

            my_print((str_multi1, " ".join(updated_set["elements"]), updated_set["name"], updated_set["value"], updated_set["addition"], str_multi2))

        # post-update additions
        if self.cost == self.max_cost:

            if self.activity == "pstk":

                addition2 = self.get_value_pstk(dealt_set["name"], held_numbers, remaining_deck)

                if addition2 > 0 and addition_ctr_incr == False:

                    self.addition_ctr += 1
                    addition_ctr_incr = True

                self.win += addition2

            elif self.activity == "php":

                addition2 = self.get_value_php(dealt_set["name"], held_numbers, remaining_deck)

                if addition2 > 0 and addition_ctr_incr == False:

                    self.addition_ctr += 1
                    addition_ctr_incr = True

                self.win += addition2

            elif self.activity == "dstp":

                multi2 = self.get_value_stp()
                addition2 = (multi2 - 1) * updated_set["value"]
                updated_set["addition"] += addition2
                updated_set["total_value"] += addition2

                if addition2 > 0 and addition_ctr_incr == False:

                    self.addition_ctr += 1
                    addition_ctr_incr = True 

                self.win += addition2

            elif self.activity == "sstk":

                addition2 = self.get_value_sstk2(held_numbers, remaining_deck)
                self.win += addition2

                
        # update credit, ctr, rtp
        self.win = self.win * self.denom

        if self.win > self.max_win:

            self.max_win = self.win

        self.credit += self.win - self.cost
        rtp = self.win / self.cost
        self.total_rtp += rtp
        my_print((self.ctr, round(-self.cost,3), round(self.win,3), round(self.credit,3), round(rtp,3)))
        
        if self.automate and self.verbose:

            time.sleep(0.3)

        self.ctr += 1

# Tests

def test(vp):

    deck = copy.deepcopy(STACK)
    random.shuffle(deck)
    dealt_set = copy.deepcopy(UPDATED_SET)
    dealt_set_4_elements = input("Enter 4 Elements:").rstrip("\n").split(",")
    dealt_set_4_numbers = [ STACK_ELEMENTS_DICT[x] for x in dealt_set_4_elements]
    remaining_deck1 = [x for x in deck if x not in dealt_set_4_numbers]
    drmcd_number = get_5th_element(dealt_set_4_numbers, remaining_deck1)
    print("DEBUG: 5th-element", STACK_ELEMENTS[drmcd_number-1])

# Main Function
def main(args):
    if args.test == True:

        vp = Vp(args.activity, args.addition_type, args.num_sets, args.credit, args.denom, args.automate, args.verbose)
        test(vp)

    else:

        final_credit_array = [0]*args.iterations
        final_rtp_array = [0]*args.iterations
        addition_ctr_array = [0]*args.iterations
        ctr_array = [0]*args.iterations
        max_win_array = [0]*args.iterations
        succ_cnt = 0
        threshold = args.credit * 0.2
        stack_type_hist = copy.deepcopy(STACK_TYPE_HIST)
        
        for ii in range(args.iterations):

            vp = Vp(args.activity, args.addition_type, args.num_sets, args.credit, args.denom, args.automate, args.verbose, stack_type_hist)
            max_ctr = 120 # Divide by 12 to get ave min
            credit_array = [0]*max_ctr
            net_50_loss = False
            fourth_credit = False
            succ = False
            ctr = 0

            while vp.credit >= vp.cost and ctr < max_ctr :

                vp.run()
                credit_array[ctr] = vp.credit
                ctr += 1

                succ = False

                
                if vp.win >= threshold:

                    succ_cnt += 1
                    succ = True
                    break

            if succ == False and vp.credit >= args.credit:

                succ_cnt += 1

            final_rtp_array[ii] = vp.total_rtp / (ctr)
            final_credit_array[ii] = vp.credit
            addition_ctr_array[ii] = vp.addition_ctr
            max_win_array[ii] = vp.max_win
            ctr_array[ii] = vp.ctr

            if args.iterations == 1:

                print("mean-rtp:", final_rtp_array[ii], "acc", vp.acc_ctr / (vp.ctr - 1), "hist", vp.stack_type_hist)
                #plt.plot(credit_array[0:vp.ctr-1])
                #splt.show()

        if args.iterations > 1:

            succ_ctr_array = [x for ii, x in enumerate(ctr_array) if final_credit_array[ii] > vp.cost ]
            succ_credit_array = [x for ii, x in enumerate(final_credit_array) if final_credit_array[ii] > vp.cost ]
            stack_type_hist = { x: round(vp.stack_type_hist[x] / args.iterations,3) for x in vp.stack_type_hist.keys()}
            stack_type_ret  = { x: round(VALUETABLE[args.addition_type][x] * stack_type_hist[x],3) for x in stack_type_hist.keys() }
            print(
                "succ-pct:", round(succ_cnt/args.iterations,3),
                "mean-succ-ctr:", round(statistics.mean(succ_ctr_array),3),
                "mean-succ-pft:", round(statistics.mean(succ_credit_array)-args.credit,3),
                "mean-max_win", round(statistics.mean(max_win_array),3),
                "mean-pft:", round(statistics.mean(final_credit_array)-args.credit,3),
                "max-prf:", round(max(succ_credit_array)-args.credit,3),
                "mean-add:", round(statistics.mean(addition_ctr_array),3), 
                "mean-rtp", round(statistics.median(final_rtp_array),3),
                "\ntype-hist", stack_type_hist,
            )
            if vp.activity == "cl":
                print( "type-ret", stack_type_ret)



# Command-line Execution
if __name__=="__main__":
    #args
    parser = argparse.ArgumentParser(description="vp")
    parser.add_argument("-c", "--credit", type=float, default=1000, help="credit")
    parser.add_argument("-d", "--denom", type=float, default=1.0, help="denom")
    parser.add_argument("-g", "--activity", default="fhpw", help="activity:cl,sptrp,stp,dstp,sstk,pstk,php,ultx,fhpw,majm,drmcd")
    parser.add_argument("-n", "--num_sets", type=int, default=3, help="num_sets")
    parser.add_argument("-b", "--addition_type", default="ddb", help="addition_type:job,b,bd,db,ddb,tdb")
    parser.add_argument("-i", "--iterations", type=int, default=1, help="iterations")
    parser.add_argument("-a", "--automate", action="store_true", help="automate")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
    parser.add_argument("-t", "--test", action="store_true", help="test")
    
    args = parser.parse_args()
    print(args)

    if args.iterations > 1:

        args.verbose = False
        args.automate = True

        def my_print(statement):

            pass

    main(args)
    



    
