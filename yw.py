#!C:\Program Files\Python312\python
import random
import copy
import argparse
import time
import os
import sys
from collections import Counter
os.system('cls' if os.name == 'nt' else 'clear')
################## Notes ################################

"""
    priority
    -target y1-4
    -target av
    -target 6l
    -target 5l
    -target 4l
    -target 3l
    -target 2l
    -target ac
    -target 3w
    -target 2w
    -target 1w
    -target ch
"""

################## Constants ################################

OUTPUT = open("sample.txt").readlines()
yahtzee_words_list = open("yahtzee_words_list.txt").readlines()
WORDS = []
for row in yahtzee_words_list:
    for x in row.replace(",","").split():
        if ":" not in x and x not in WORDS:
            WORDS.insert(0, x)

STAR = "*"
LTTR_VAL = {
        STAR: 0,

        "A": 1, "E": 1, "O": 1, 

        "I": 2, "L": 2, "N": 2, "R": 2, "S": 2, "T": 2,

        "D": 3, "H": 3, "M": 3, "U": 3, 

        "B": 4, "C": 4, "F": 4, "G": 4, "P": 4, "V": 4, "W": 4, "Y": 4,
         
        "K": 5, 

        "J": 6, 
         
        "Q": 8, "X": 8,

        "Z": 10
}
LTTR = list(LTTR_VAL.keys())
CUBE_LTTR = {
    0: "CKONUV",
    1: "ABESXY",
    2: "ADJNQR",
    3: "EIGMP" + STAR,
    4: "MOPUWY",
    5: "ACEFIZ",
    6: "AEHLST",
}

CARD = {
    "y1":    {"tp": "lower", "val":  50, "sc": 0},
    "y2":    {"tp": "lower", "val": 100, "sc": 0},
    "y3":    {"tp": "lower", "val": 100, "sc": 0},
    "y4":    {"tp": "lower", "val": 100, "sc": 0},

    "av":    {"tp": "lower", "val":  35, "sc": 0},

    "6l":    {"tp": "upper", "val":   0, "sc": 0},
    "5l":    {"tp": "upper", "val":   0, "sc": 0},
    "4l":    {"tp": "upper", "val":   0, "sc": 0},
    "3l":    {"tp": "upper", "val":   0, "sc": 0}, 
    "2l":    {"tp": "upper", "val":   0, "sc": 0},

    "bn":    {"tp": "lower", "val":   0, "sc": 0},

    "ac":    {"tp": "lower", "val":  25, "sc": 0},

    "3w":    {"tp": "lower", "val":   0, "sc": 0},
    "2w":    {"tp": "lower", "val":   0, "sc": 0}, 
    "1w":    {"tp": "lower", "val":   0, "sc": 0}, 
    
    "ch":    {"tp": "lower", "val":   0, "sc": 0},
     
}
CARD_KEYS = list(CARD.keys())

VOWELS = "AEIOUY*"
CONSONANTS = "BCDFGHJKLMNPQRSTVWXYZ*"

# Functions
def my_decorator(func):
    def wrapper(statement):
        choice = random.choice(range(len(OUTPUT)))
        line = str(statement).replace("'","").replace(",","") +" "+ OUTPUT[choice].rstrip("\n")
        func(line)
    return wrapper

@my_decorator
def my_print(statement):
    print(statement)

######################################## Functions  ########################################
def is_sublist(small_list, big_list):
    # Subtracting Counters removes elements found in both
    # A remaining positive count means big_list lacks that item
    return not (Counter(small_list) - Counter(big_list))

def check_for_words(ltrs_list):
    wrds = []
    wrds2 = []
    all_ltrs = sorted([x for x in LTTR if x != STAR])
    for wd in WORDS:
        wd_list = [x for x in wd]
        if STAR in ltrs_list:
            ltrs_list2 = copy.deepcopy(ltrs_list)
            ind = ltrs_list2.index(STAR)
            for ltr in all_ltrs:
                ltrs_list2[ind] = ltr
                if is_sublist(wd_list, ltrs_list2)  == True and ltr in wd_list:
                    wd_list2 = copy.deepcopy(wd_list)
                    #print("DEBUG:", wd_list2, ltrs_list2)
                    ind = wd_list2.index(ltr)
                    
                    wd_list2[ind] = STAR
                    wd2 = "".join(wd_list2)
                        
                    if wd not in wrds:
                        wrds.append(wd)
                    if wd2 not in wrds2:
                        wrds2.append(wd2)
        else:
            if is_sublist(wd_list, ltrs_list) and wd not in wrds:
                #print("INFO. wrd found", wd)
                wrds.append(wd)
                wrds2.append(wd)
    print("TIP: wds found:", wrds)
    return wrds2

######################################## Classes  ########################################
class Yw(object):
    def __init__(self, args):
        self.automate = args.automate
        self.verbose = args.verbose
        self.rnd = 1
        self.cubes = copy.deepcopy(CUBE_LTTR)
        self.card = copy.deepcopy(CARD)
        self.rows_left = copy.deepcopy(CARD_KEYS)
        self.rows_left.pop(self.rows_left.index("bn"))
        self.sc = 0
        self.ltrs = []
        self.running = True
        self.upper_bonus = 0

    def print_ltrs(self):
        ltrs_vals = [ x + str(LTTR_VAL[x]) for x in self.ltrs]
        print(ltrs_vals)

    def algorithm1(self, step):

        user_input = ""
        ltrs_str = "".join(self.ltrs)
        test_wd = ""
        
        wds = check_for_words(self.ltrs)

        if len(wds) > 0:
        
            test_wd = wds[0]
            for wd in wds:
                if "yl" in self.rows_left or "y2" in self.rows_left or "y3" in self.rows_left or "y4" in self.rows_left and len(wd) == 7:
                    test_wd = wd
                    break
                if "6l" in self.rows_left and len(wd) == 6:
                    test_wd = wd
                    break
                if "5l" in self.rows_left and len(wd) == 5:
                    test_wd = wd
                    break
                if "4l" in self.rows_left and len(wd) == 4:
                    test_wd = wd
                    break
                if "3l" in self.rows_left and len(wd) == 3:
                    test_wd = wd
                    break
                if "2l" in self.rows_left and len(wd) == 2:
                    test_wd = wd
                    break
                test_wd = wds[0]

        len_test_wd = len(test_wd)

        consonants = [x for x in self.ltrs if x in CONSONANTS]
        len_consonants = len(consonants)
        vowels = [x for x in self.ltrs if x in VOWELS]
        len_vowels = len(vowels)

        if step == "choose_ltrs":

            if "ac" in self.rows_left and  len_consonants == 7:

                user_input = "".join(consonants)

            elif "av" in self.rows_left and  len_vowels > 4:
            
                user_input = "".join(vowels)

            elif len_test_wd > 0:

                user_input = test_wd

            else:

                user_input = ltrs_str

            print("ALG1. Enter ltrs: ", user_input)

        elif step == "choose_row_ltrs":

            if   len_test_wd == 7:

                if "y1" in self.rows_left: 

                    user_input = "y1 " + test_wd

                if "y2" in self.rows_left: 
                
                    user_input = "y2 " + test_wd

                if "y3" in self.rows_left: 
                                
                    user_input = "y3 " + test_wd

                if "y4" in self.rows_left: 
                                
                    user_input = "y4 " + test_wd

                if "ch" in self.rows_left:

                    user_input = "ch " + test_wd

            elif "av" in self.rows_left and len_vowels == 7:
            
                user_input = "av " + ltrs_str

            elif "6l" in self.rows_left and len_test_wd == 6:

                user_input = "6l " + test_wd

            elif "5l" in self.rows_left and len_test_wd == 5:
            
                user_input = "5l " + test_wd

            elif "4l" in self.rows_left and len_test_wd == 4:
            
                user_input = "4l " + test_wd

            elif "3l" in self.rows_left and len_test_wd == 3:
            
                user_input = "3l " + test_wd

            elif "2l" in self.rows_left and len_test_wd == 2:
            
                user_input = "2l " + test_wd

            elif "ac" in self.rows_left and len_consonants == 7:
            
                user_input = "ac " + ltrs_str

            elif "3w" in self.rows_left and len_test_wd > 0:
                        
                user_input = "3w " + test_wd + ";;"

            elif "2w" in self.rows_left and len_test_wd > 0:
            
                user_input = "2w " + test_wd + ";"

            elif "1w" in self.rows_left and len_test_wd > 0:

                user_input = "1w " + test_wd

            elif "ch" in self.rows_left:

                user_input = "ch " + ltrs_str

            else:

                user_input = "z"

            print("ALG1. Enter row & ltrs: ", user_input)

        if self.verbose == True:
            #user_input2 = input("    continue...")
            #if user_input2 == "q":
            #    user_input = user_input2
            time.sleep(0.5)

        return user_input
        
    def choose_ltrs(self):

        print("\nINFO: rows_left", self.rows_left)

        # shuffle 1
        self.ltrs = [random.choice(CUBE_LTTR[x]) for x in range(7)]
        print("   shuffle1 ltrs: ", self.ltrs)

        if self.automate == True:
            user_input = self.algorithm1("choose_ltrs")
        else:
            if self.verbose:
                check_for_words(self.ltrs)
            user_input = input("INPUT. Enter ltrs: ")

            if user_input == "q":
                print("INFO. quit")
                self.running = False
                return

            if user_input == "a":
                user_input = "".join(self.ltrs)
        
        cnt_ltrs = {}
        choices = []
        for ltr in user_input:
            indices = [i for i,x in enumerate(self.ltrs) if x == ltr]
            if len(indices) == 0:
                print("ERROR. ltr not in ltrs: ", ltr)
                self.running = False
                return
            else:
                if ltr not in cnt_ltrs.keys():
                    cnt_ltrs[ltr] = 0
                else:
                    cnt_ltrs[ltr] += 1
                    if len(indices) - cnt_ltrs[ltr] == 0:
                        print("ERROR. ltr not in ltrs: ", ltr)
                        self.running = False
                        return

                ind = indices[cnt_ltrs[ltr]]
                choices.append(ind)

        # shuffle 2
        for x in range(7):
            if x not in choices:
                self.ltrs[x] = random.choice(CUBE_LTTR[x])

        print("   shuffle2 ltrs_left: ", self.ltrs)

        if self.automate == True:
            user_input = self.algorithm1("choose_ltrs")
        else:
            if self.verbose:
                check_for_words(self.ltrs)
            user_input = input("INPUT. Enter ltrs: ")

            if user_input == "q":
                print("INFO. quit")
                self.running = False
                return

            if user_input == "a":
                user_input = "".join(self.ltrs)
        
        cnt_ltrs = {}
        choices = []
        for ltr in user_input:
            indices = [i for i, x in enumerate(self.ltrs) if x == ltr]
            if len(indices) == 0:
                print("ERROR. ltr not in ltrs: ", ltr)
                self.running = False
                return
            else:
                if ltr not in cnt_ltrs.keys():
                    cnt_ltrs[ltr] = 0
                else:
                    cnt_ltrs[ltr] += 1
                    if len(indices) - cnt_ltrs[ltr] == 0:
                        print("ERROR. ltr not in ltrs: ", ltr)
                        self.running = False
                        return

                ind = indices[cnt_ltrs[ltr]]
                choices.append(ind)

        # shuffle 3
        for x in range(7):
            if x not in choices:
                self.ltrs[x] = random.choice(CUBE_LTTR[x])

        print("     shuffle3 ltrs: ", self.ltrs)
        
    def choose_row_ltrs(self):
        if self.running == False:
            return
        
        print("\nINFO. rows_lft: ", self.rows_left)
        print("        ltrs_left:", self.ltrs)

        if self.automate == True:
            user_input = self.algorithm1("choose_row_ltrs")
        else:
            if self.verbose:
                check_for_words(self.ltrs)
            user_input = input("INPUT. Enter row & ltrs:")

            if user_input == "q":
                print("INFO. quit")
                self.running = False
                return

        if user_input == "z":
            print("INFO. accept 0")
            return

        row_ltrs_list = user_input.split()

        if len(row_ltrs_list) != 2:
            print("ERROR. Invalid row ltrs", row_ltrs_list)
            self.running = False
            return

        row_to_sc, chosen_ltrs = row_ltrs_list

        if chosen_ltrs == "a":
            chosen_ltrs = "".join(self.ltrs)

        if not self.validate_row_ltrs(row_to_sc, chosen_ltrs):
            self.running = False
            return

        kept_ltrs = []

        for ltr in chosen_ltrs:
            if ltr in self.ltrs:
                add_ltr = self.ltrs.pop(self.ltrs.index(ltr))
                kept_ltrs.append(add_ltr)
        
        self.rows_left.pop(self.rows_left.index(row_to_sc))

        if self.card[row_to_sc]["val"] > 0:
            self.card[row_to_sc]["sc"] = self.card[row_to_sc]["val"]
        else:
            self.card[row_to_sc]["sc"] = sum([ LTTR_VAL[x] for x in kept_ltrs])

        # check upper rows bonus
        upper_sc = 0
        if self.card["bn"]["sc"] == 0:
            for row in CARD_KEYS:
                if self.card[row]["tp"] == "upper":
                    upper_sc += self.card[row]["sc"]
            if upper_sc >= 45:
                print("INFO. Upper row bonus 35!")
                self.card["bn"]["sc"] = 35
                self.sc += self.card["bn"]["sc"]

        self.sc += self.card[row_to_sc]["sc"]

        print("INFO. row sc", self.card[row_to_sc]["sc"])

    def validate_row_ltrs(self, row_to_sc, chosen_ltrs):
        valid = True
        len_ltrs = len([x for x in chosen_ltrs if x != ";"])
        len_consonants = len([x for x in chosen_ltrs if x in CONSONANTS])
        len_vowels = len([x for x in chosen_ltrs if x in VOWELS])
        len_words = len(chosen_ltrs.rstrip().split(";"))
        if row_to_sc not in self.rows_left:
            print("ERROR. invalid row", row_to_sc)
            valid = False
        elif row_to_sc in ("y1", "y2", "y3", "y4", "ch", "av", "ac") and len_ltrs != 7:
            print("ERROR. 7 ltrs were not selected", chosen_ltrs)
            valid = False
        elif row_to_sc == "av" and len_vowels != 7:
            print("ERROR. ltrs are not all vowels", chosen_ltrs)
            valid = False
        elif row_to_sc == "ac" and len_consonants != 7:
            print("ERROR. ltrs are not all consonants", chosen_ltrs)
            valid = False
        elif row_to_sc == "6l" and len_ltrs != 6:
            print("ERROR. 6 ltrs were not chosen", chosen_ltrs)
            valid = False
        elif row_to_sc == "5l" and len_ltrs != 5:
            print("ERROR. 5 ltrs were not chosen", chosen_ltrs)
            valid = False
        elif row_to_sc == "4l" and len_ltrs != 4:
            print("ERROR. 4 ltrs were not chosen", chosen_ltrs)
            valid = False
        elif row_to_sc == "3l" and len_ltrs != 3:
            print("ERROR. 3 ltrs were not chosen", chosen_ltrs)
            valid = False
        elif row_to_sc == "2l" and len_ltrs != 2:
            print("ERROR. 2 ltrs were not chosen", chosen_ltrs)
            valid = False
        elif row_to_sc == "3w" and len_words != 3:
            print("ERROR. 3 wrds were not chosen", chosen_ltrs)
            valid = False
        elif row_to_sc == "2w" and len_words != 2:
            print("ERROR. 2 wrds were not chosen", chosen_ltrs)
            valid = False
        elif row_to_sc == "1w" and len_words != 1:
            print("ERROR. 1 wrd were not chosen", chosen_ltrs)
            valid = False

        return valid

    def update_rnd(self):
        self.print_card()
        self.rnd += 1
        print("INFO. rnd:", self.rnd)
        if self.rnd > 12:
            self.running = False
            
    def print_card(self):
        card_score = [ key + ":" + str(self.card[key]["sc"]) for key in CARD_KEYS]
        print("INFO. total sc:", self.sc, card_score)

    def run(self):
        while self.running == True:
            self.choose_ltrs()
            self.choose_row_ltrs()
            self.update_rnd()

# Tests
def test(args):
    self = Yw(args)
    self.ltrs = input("TEST: enter ltrs: ")
    self.algorithm1("choose_ltrs")
    self.algorithm1("choose_row_ltrs")

# Main Function
def main(args):
    if args.test == True:
        test(args)
    else:
        yw = Yw(args)
        yw.run()

# Command-line Execution
if __name__=="__main__":
    #args
    parser = argparse.ArgumentParser(description="ch")
    parser.add_argument("-a", "--automate", action="store_true", help="automate")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
    parser.add_argument("-t", "--test", action="store_true", help="test")

    args = parser.parse_args()
    print(args)
    main(args)
    



    
