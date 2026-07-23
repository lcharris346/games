#!C:\Program Files\Python312\python
import random
import copy
import argparse
import time
import os
import sys
from collections import Counter

# Constants

CMN_WDS_7 = (
    "ADONISE", "ELASTIN", "NAILSET", "SALIENT", "AILERON",
    "ELATION", "NASTIER", "SALTINE", "ALERION", "ENAMELS",
    "NEUTERS", "ERASION", "ANESTRI", "SESTINA", "PAINTER",
    "SANTERO", "ALIENER", "ENTAILS", "NIDATES", "SARDINE",
    "ALIENOR", "ENTRAIL", "NORITES", "SATINES", "ANEROID",
    "NOTAIRE", "SAUNTER", "ANISOLE", "ETAERIO", "OARIEST",
    "SEALION", "ANODISE", "ETESIAN", "OESTRIN", "SEDATER",
    "GARTENS", "ORIENTS", "SENATOR", "ANTIRED", "GOATIER",
    "ORIGANE", "SERIATE", "ANTSIER", "GRANITE", "OTARIEN",
    "ARENITE", "GRATINE", "OTARINE", "SETLINE", "ARIDEST",
    "INERTIA", "OUTEARN", "SLAINTE", "ARTISTE", "INGRATE",
    "SODAINE", "ASTRIDE", "IODATES", "PANTIES", "SOREDIA",
    "ATELIER", "ISOLATE", "PIRATES", "STAINER", "ATONERS",
    "RADIOES", "STARNIE", "ATONIES", "LESTERS", "RATINES",
    "STEARIN", "DARIOLE", "LINEATE", "RATLINE", "STONIER",
    "LINTERS", "REALTIE", "STRANGE", "DESTAIN", "REALISE",
    "RELIANT", "STRIATE", "DETAINS", "RENAILS", "RESIANT",
    "DETRAIN", "RENTALS", "RETAINS", "TOADIES", "DIASTER",
    "RETAILS", "RETINAE", "TOENAIL", "DISRATE", "RETINOL",
    "DEARNES", "TAURINE", "LATRINE", "ROASTIE", "TRAINEE",
)
CMN_WDS_6 = (
    "ALTERS", "ARISEN", "ARTIST", "ASPIRE", "ASTERN",
    "CASTER", "CASTLE", "CRATER", "DIREST", "EARNER",
    "EARTHS", "EASTER", "ENTERS", "ESTERS", "GRATER",
    "HATERS", "HEARTS", "LASERS", "LATEST", "LEANER",
    "LISTEN", "LITERS", "LOOSER", "MASTER", "MINERS",
    "MISERS", "NEATER", "NESTLE", "PASTES", "PASTIE",
    "PASTOR", "RAISED", "REASON", "RESENT", "RESETS",
    "RESIST", "RESTED", "RETAIL", "RETAIN", "RETEST",
    "RETIRE", "ROASTS", "ROSTER", "SAILER", "SAINTS",
    "SALINE", "SALTER", "SATIRE", "SCARED", "SCARES",
    "SCORES", "SCREES", "SECTOR", "SENDER", "SENIOR",
    "SENSES", "SERENE", "SERIAL", "SERIES", "SERMON",
    "SHARES", "SHIRTS", "SHORES", "SISTER", "SMARTS",
    "SNARES", "SOREST", "STALER", "STANCE", "STARER",
    "STARES", "STARTS", "STATES", "STORES", "STRAIN",
    "STREAK", "STREAM", "STREET", "STRIKE", "STRIPE",
    "STRIPS", "STRIVE", "TAILER", "TENORS", "TENSOR",
    "TESTER", "TIGERS", "TIMERS", "TINDER", "TINSEL",
    "TOASTS", "TONERS", "TRACER", "TRAILS", "TRAINS",
    "TRAITS", "TREADS", "VOTERS", "WASTES", "WRITES"
)
OUTPUT = open("sample.txt").readlines()
LTTR_VAL = {
        "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4,
        "G": 2, "H": 4, "I": 1, "J": 6, "K": 5, "L": 2,
        "M": 2, "N": 2, "O": 1, "P": 3, "Q": 8, "R": 1,
        "S": 1, "T": 1, "U": 1, "V": 5, "W": 4, "X": 6,
        "Y": 3, "Z": 8, "*": 0
}
LTTR = LTTR_VAL.keys()
CUBE_LTTR = {
    0: "CKONUV",
    1: "ABESXY",
    2: "ADJNQR",
    3: "EIGMP*",
    4: "MOPUWY",
    5: "ACEFIZ",
    6: "AEHLST",
}

CARD = {
     "2l":    {"tp": "upper", "val":   0, "sc": 0},
     "3l":    {"tp": "upper", "val":   0, "sc": 0}, 
     "4l":    {"tp": "upper", "val":   0, "sc": 0}, 
     "5l":    {"tp": "upper", "val":   0, "sc": 0},
     "6l":    {"tp": "upper", "val":   0, "sc": 0},

     "1w":    {"tp": "lower", "val":   0, "sc": 0}, 
     "2w":    {"tp": "lower", "val":   0, "sc": 0}, 
     "3w":    {"tp": "lower", "val":   0, "sc": 0}, 
     "ac":    {"tp": "lower", "val":  25, "sc": 0},
     "av":    {"tp": "lower", "val":  35, "sc": 0},

     "y1":    {"tp": "lower", "val":  50, "sc": 0},
     "ch":    {"tp": "lower", "val":  35, "sc": 0},

     "y2":    {"tp": "lower", "val": 100, "sc": 0},
     "y3":    {"tp": "lower", "val": 100, "sc": 0},
     "y4":    {"tp": "lower", "val": 100, "sc": 0},
}
CARD_KEYS = list(CARD.keys())

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

######################################## CLASSES  ########################################
class Yw(object):
    def __init__(self, args):
        self.automate = args.automate
        self.verbose = args.verbose
        self.rnd = 1
        self.cubes = copy.deepcopy(CUBE_LTTR)
        self.card = copy.deepcopy(CARD)
        self.rows_left = copy.deepcopy(CARD_KEYS)
        self.sc = 0
        self.ltrs = []
        self.running = True
        self.upper_bonus = 0

    def choose_ltrs(self):

        # shuffle 1
        cubes_left = [0,1,2,3,4,5,6]
        ltrs_left = [ random.choice(CUBE_LTTR[x]) for x in cubes_left]
        self.ltrs = []

        self.check_for_7ltr_wrd(self.ltrs + ltrs_left)
        self.check_for_6ltr_wrd(self.ltrs + ltrs_left)

        print("\nINFO: rows_left", self.rows_left)
        print("        shuffle1 ltrs_left: ", ltrs_left)
        user_input = input("INPUT. sel ltrs: ")

        if user_input == "q":
            print("INFO. quit")
            self.running = False
            return
        

        for ltr in user_input:
            if ltr not in ltrs_left:
                print("ERROR. ltr not in ltrs_left: ", ltr)
                self.running = False
                return

            ind_ltr = ltrs_left.index(ltr)
            if ind_ltr == -1:
                print("ERROR. ltr not on cubes", ltr)
                self.running = False
                return
            else:
                choice = ltrs_left.pop(ind_ltr)
                cubes_left.pop(ind_ltr)
                self.ltrs.append(choice)

        print("INFO. kept_ltrs: ", self.ltrs, ". cubes left: ", cubes_left, ". ltrs left: ", ltrs_left)

        

        # shuffle 3
        ltrs_left = [ random.choice(CUBE_LTTR[x]) for x in cubes_left]

        self.check_for_7ltr_wrd(self.ltrs + ltrs_left)
        self.check_for_6ltr_wrd(self.ltrs + ltrs_left)

        if len(ltrs_left) == 0:
            print("INFO. all ltrs selected")
            return

        print("INFO: shuffle2 ltrs_left: ", ltrs_left)
        user_input = input("INPUT. sel ltrs: ")

        if user_input == "q":
            print("INFO. quit")
            self.running = False
            return

        for ltr in user_input:
            if ltr not in ltrs_left:
                print("ERROR. ltr not in ltrs_left: ", ltr)
                self.running = False
                return
            ind_ltr = ltrs_left.index(ltr)
            if ind_ltr == -1:
                print("ERROR. ltr not on cubes", ltr)
                self.running = False
                return
            else:
                choice = ltrs_left.pop(ind_ltr)
                cubes_left.pop(ind_ltr)
                self.ltrs.append(choice)

        print("INFO. kept_ltrs: ", self.ltrs, ". cubes left: ", cubes_left, ". ltrs left: ", ltrs_left)

        

        # shuffle 3
        ltrs_left = [ random.choice(CUBE_LTTR[x]) for x in cubes_left]

        if len(ltrs_left) == 0:
            print("INFO. all ltrs selected")
            return
        
        self.ltrs += ltrs_left

        print("INFO. kept_ltrs: ", self.ltrs, ". cubes left: ", cubes_left, ". ltrs left: ", ltrs_left)
        
    

    def calc_row_sc(self):
        if self.running == False:
            return
        
        print("\nINFO. rows_lft: ", self.rows_left)
        print("        ltrs_left:", self.ltrs)

        self.check_for_7ltr_wrd(self.ltrs)
        self.check_for_6ltr_wrd(self.ltrs)

        user_input = input("INPUT. Enter row & ltrs:")

        if user_input == "q":
            print("INFO. quit")
            self.running = False
            return

        if user_input == "z":
            print("INFO. accept 0")
            return

        row_ltrs_list = user_input.split()

        while len(row_ltrs_list) != 2:
            print("ERROR. Invalid row ltrs", row_ltrs_list)
            user_input = input("INPUT. Enter row & ltrs:")
            row_ltrs_list = user_input.split()

        row_to_sc, chosen_ltrs = row_ltrs_list

        
        if row_to_sc not in self.rows_left:
            print("ERROR. invalid row-to-sc ", row_to_sc)
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
        if self.upper_bonus == 0:
            for row in CARD_KEYS:
                if self.card[row]["tp"] == "upper":
                    upper_sc += self.card[row]["sc"]
            if upper_sc >= 45:
                print("INFO. Upper row bonus 35!")
                self.upper_bonus = 35
                self.sc += self.upper_bonus

        self.sc += self.card[row_to_sc]["sc"]

        print("INFO. row sc", self.card[row_to_sc]["sc"])

    def update_rnd(self):
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
            self.calc_row_sc()
            self.print_card()
            self.update_rnd()

    def check_for_7ltr_wrd(self, ltrs_list):
        wrds = []
        for wrd in CMN_WDS_7:
            ltrs_str = "".join(ltrs_list)
            if Counter(wrd) == Counter(ltrs_str):
                wrds.append(wrd)
                print("INFO. 7 ltrs form wrd: ", wrd)

        return wrds
    
    def check_for_6ltr_wrd(self, ltrs_list):
        wrds = []
        for ii in range(7):
            ltrs_list2 = copy.deepcopy(ltrs_list)
            ltrs_list2.pop(ii)
            for wrd in CMN_WDS_6:
                ltrs_str = "".join(ltrs_list2)
                if Counter(wrd) == Counter(ltrs_str):
                    wrds.append(wrd)
                    print("INFO. 6 ltrs form wrd: ", wrd)

        return wrds

        

# Tests
def test(args):
    self = Yw(args)
    wrds = []
    while len(wrds) < 4:
        cubes_left = [0,1,2,3,4,5,6]
        ltrs_left = [ random.choice(CUBE_LTTR[x]) for x in cubes_left]
        wrds += self.check_for_7ltr_wrd(ltrs_left)
        wrds += self.check_for_6ltr_wrd(ltrs_left)

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
    



    
