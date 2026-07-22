#!C:\Program Files\Python312\python
import random
import copy
import argparse
import time
import os
import sys
from tkinter import SEL


############### Helper Classes ##############
NONE = "_"
class Sq(object):
    def __init__(self, bonus = NONE):
        self.bonus = bonus
        self.ltr = bonus
        self.coord_name = ""

############## Constants ##############
OUTPUT = open("sample.txt").readlines()
LTTR_CNT_VAL =   {""
        "A" : {"cnt": 9, "val": 1},
        "B" : {"cnt": 2, "val": 3},
        "C" : {"cnt": 2, "val": 3},
        "D" : {"cnt": 4, "val": 2},
        "E" : {"cnt": 12,"val": 1},
        "F" : {"cnt": 2, "val": 4},
        "G" : {"cnt": 3, "val": 2},
        "H" : {"cnt": 2, "val": 4},
        "I" : {"cnt": 9, "val": 1}, 
        "J" : {"cnt": 1, "val": 8},
        "K" : {"cnt": 1, "val": 5},
        "L" : {"cnt": 4, "val": 1}, 
        "M" : {"cnt": 2, "val": 3},
        "N" : {"cnt": 6, "val": 1}, 
        "O" : {"cnt": 8, "val": 1}, 
        "P" : {"cnt": 2, "val": 3}, 
        "Q" : {"cnt": 1, "val": 10},
        "R" : {"cnt": 6, "val": 1},
        "S" : {"cnt": 4, "val": 1},
        "T" : {"cnt": 6, "val": 1}, 
        "U" : {"cnt": 4, "val": 1},
        "V" : {"cnt": 2, "val": 4}, 
        "W" : {"cnt": 2, "val": 4},
        "X" : {"cnt": 1, "val": 8},
        "Y" : {"cnt": 2, "val": 4},
        "Z" : {"cnt": 1, "val": 10},
        "*" : {"cnt": 2, "val": 0},
}

LTTR = LTTR_CNT_VAL.keys()

DISTRO_LTTR = []
for ltr in LTTR:
    DISTRO_LTTR += [ltr] * LTTR_CNT_VAL[ltr]["cnt"]


BOARD = {}
COORD_RANGE = list(range(1,16))
for x in COORD_RANGE:
    for y in COORD_RANGE:
        BOARD[(x,y)] = Sq()



TW = "6"
DW = "4"
TL = "3"
DL = "2"

BONUS = {NONE: 1,  TW: 3, DW: 2, TL: 3, DL: 2}

BONUS_KEYS = BONUS.keys()

BOARD[( 1, 1)].bonus = TW
BOARD[( 1, 8)].bonus = TW
BOARD[( 1,15)].bonus = TW
BOARD[( 8, 1)].bonus = TW
BOARD[( 8,15)].bonus = TW
BOARD[(15, 1)].bonus = TW
BOARD[(15, 8)].bonus = TW
BOARD[(15,15)].bonus = TW

BOARD[(  8, 8)].bonus = DW
BOARD[(  2, 2)].bonus = DW
BOARD[(  3, 3)].bonus = DW
BOARD[(  4, 4)].bonus = DW
BOARD[(  5, 5)].bonus = DW
BOARD[( 14, 2)].bonus = DW
BOARD[( 13, 3)].bonus = DW
BOARD[( 12, 4)].bonus = DW
BOARD[( 11, 5)].bonus = DW
BOARD[(  2,14)].bonus = DW
BOARD[(  3,13)].bonus = DW
BOARD[(  4,12)].bonus = DW
BOARD[(  5,11)].bonus = DW
BOARD[( 11,11)].bonus = DW
BOARD[( 12,12)].bonus = DW
BOARD[( 13,13)].bonus = DW
BOARD[( 14,14)].bonus = DW

BOARD[(  4, 1)].bonus = DL
BOARD[(  7, 3)].bonus = DL
BOARD[(  8, 4)].bonus = DL
BOARD[(  9, 3)].bonus = DL
BOARD[( 12, 1)].bonus = DL

BOARD[( 15, 4)].bonus = DL
BOARD[( 13, 7)].bonus = DL
BOARD[( 12, 8)].bonus = DL
BOARD[( 13, 7)].bonus = DL
BOARD[( 15,12)].bonus = DL

BOARD[(  4,15)].bonus = DL
BOARD[(  7,13)].bonus = DL
BOARD[(  8,12)].bonus = DL
BOARD[(  9,13)].bonus = DL
BOARD[( 12,15)].bonus = DL

BOARD[( 1, 4)].bonus = DL
BOARD[( 3, 7)].bonus = DL
BOARD[( 4, 8)].bonus = DL
BOARD[( 3, 7)].bonus = DL
BOARD[( 1,12)].bonus = DL

BOARD[( 7, 7)].bonus = DL
BOARD[( 9, 7)].bonus = DL
BOARD[( 7, 9)].bonus = DL
BOARD[( 9, 9)].bonus = DL

BOARD[( 6, 2)].bonus = TL
BOARD[(10, 2)].bonus = TL
BOARD[( 2, 6)].bonus = TL
BOARD[( 6, 6)].bonus = TL
BOARD[(10, 6)].bonus = TL
BOARD[(14, 6)].bonus = TL
BOARD[( 2,10)].bonus = TL
BOARD[( 6,10)].bonus = TL
BOARD[(10,10)].bonus = TL
BOARD[(14,10)].bonus = TL
BOARD[( 6,14)].bonus = TL
BOARD[(10,14)].bonus = TL

COORD = BOARD.keys()

for coord in COORD:
    BOARD[coord].ltr = BOARD[coord].bonus

PLAYER = {"score": 0, "letters": []}

HEX = " 123456789abcdef"

COORD_NAMES = {}

for row in COORD_RANGE:
    for col in COORD_RANGE:
        key = HEX[col] + HEX[row]
        COORD_NAMES[key] = (col, row)
        BOARD[(col, row)].coord_name = key

############### Functions ##############
def my_decorator(func):
    def wrapper(statement):
        choice = random.choice(range(len(OUTPUT)))
        line = str(statement).replace("'","").replace(",","")# +" "+ OUTPUT[choice].rstrip("\n")
        func(line)
    return wrapper

@my_decorator
def my_print(statement):
    print(statement)

######################################## Main Class  ########################################
class Scr(object):
    def __init__(self, automate, verbose):
        self.automate = automate
        self.verbose = verbose
        self.letters = copy.deepcopy(DISTRO_LTTR)
        self.board = copy.deepcopy(BOARD)
        self.players = {1: copy.deepcopy(PLAYER), 2: copy.deepcopy(PLAYER)}
        self.turn = 2
        self.first_word_down = False
        self.running = True
        
    def print(self):
        
        label_str = "  1 2 3 4 5 6 7 8 9 a b c d e f  "
        #my_print(label_str)

        for row in COORD_RANGE:
            prow = 16 - row
            row_str = str(prow)
            if row_str == "10":
                row_str = "a"
            elif row_str == "11":
                row_str = "b"
            elif row_str == "12":
                row_str = "c"
            elif row_str == "13":
                row_str = "d"
            elif row_str == "14":
                row_str = "e"
            elif row_str == "15":
                row_str = "f"
            col = row_str + "|" + "".join( [ self.board[xy].ltr + "|"  for xy in COORD if xy[1] == prow] )

            my_print(col)

        my_print(label_str)

    def get_used_letters(self):
        used_letters = [ x.ltr for x in self.board.values()]
        return used_letters

    def get_letters(self):
        num = 7 - len(self.players[self.turn]["letters"])
        random.shuffle(self.letters)
        new_letters = self.letters[:num]
        self.letters = self.letters[num:]
        self.players[self.turn]["letters"] += new_letters
        print("INFO. Updated ltrs:", self.players[self.turn]["letters"])
        if len(self.letters) < 1:
            self.running = False

    def place_word(self):
        
        user_input = input("ACTION. Enter Loc h/v ltrs:").rstrip()

        if user_input == "q":
             print("INFO: Quit")
             self.running = False
             return
        
        if user_input == "d":
             print("INFO: Dump ltrs")
             self.players[self.turn]["letters"] = []
             return

        word_placements = user_input.split(";")
        
        for wp in word_placements:
         
           sel_squares = []
           sel_letters = copy.deepcopy(self.players[self.turn]["letters"])
         
           sq1coordname_dir_word = wp.split(" ")
   
           if len(sq1coordname_dir_word) != 3:
               print("ERROR: Invalid number of inputs", sq1coordname_dir_word)
               #self.running = False
               return 
   
           sq1coordname, _dir, word = sq1coordname_dir_word
   
           if sq1coordname not in COORD_NAMES:
               #print("ERROR: Invalid sq1", sq1coordname)
               self.running = False
               return 
   
           if _dir not in ("h", "v"):
               #print("ERROR: Invalid dir", _dir)
               self.running = False
               return 
   
           cnt_board_letters = 0
           coord = COORD_NAMES[sq1coordname]
   
           for ltr in word:
               
               if ltr not in LTTR:
                   print("ERROR! Invalid Ltr", ltr)
                   self.running = False
                   return
   
               if coord not in COORD:
                   print("ERROR! Invalid Coord", coord)
                   self.running = False
                   return
               
               square = copy.deepcopy(self.board[coord])
               
               if square.ltr not in BONUS_KEYS:
                   if square.ltr == ltr:
                       if self.verbose:
                           print("DEBUG. Using sq and ltr", square.coord_name, square.ltr)
                       cnt_board_letters += 1
                   else:
                       print("ERROR! Ltr Mismatch", square.ltr, ltr)
                       self.running = False
                       return
   
               elif ltr not in self.players[self.turn]["letters"]:
                   if self.first_word_down == False:
                       print("ERROR: Invalid ltr", ltr)
                       self.running = False
                       return 
                   else:
                       cnt_board_letters += 1
               
               else:
                   sel_letters.pop(sel_letters.index(ltr))
                   square.ltr = ltr
                   self.board[coord].ltr = ltr
                   self.board[coord].bonus = NONE
   
               sel_squares.append(square)
               if _dir == "h":
                   coord = (coord[0] + 1, coord[1])
               elif _dir == "v":
                   coord = (coord[0], coord[1] - 1)

           if coord in COORD and BOARD[coord].ltr not in BONUS_KEYS:
               print("ERROR! Adjacent ltr not included. ")
               self.running = False
               return

           if self.first_word_down and cnt_board_letters == 0:
               print("ERROR! No board letters used.")
               self.running = False
               return
        
           if len(sel_letters) == len(self.players[self.turn]["letters"]):
               print("ERROR! No letters chosen.")
               self.running = False
               return
               
   
           self.players[self.turn]["letters"] = copy.deepcopy(sel_letters)
   
           if self.verbose:
               print("DEBUG: sel_squares:", [x.ltr for x in sel_squares])
   
           self.get_word_value(sel_squares)
   
           if self.first_word_down == False:
               self.first_word_down = True

    def get_word_value(self, sel_squares):

        value = 0
        multi = 1

        for sq in sel_squares:

            if sq.bonus == "4":
                multi = multi * 2
                sq.bonus = NONE
                print("INFO. dbl wrd!")
            elif sq.bonus == "6":
                multi = multi * 3
                sq.bonus = NONE
                print("INFO. trp wrd!")
            if sq.bonus == "2":
                value += LTTR_CNT_VAL[sq.ltr]["val"] * 2
                sq.bonus = NONE
                print("INFO. dbl ltr!", sq.ltr)
            elif sq.bonus == "3":
                value += LTTR_CNT_VAL[sq.ltr]["val"] * 3
                sq.bonus = NONE
                print("INFO. trp ltr!", sq.ltr)
            else:
                value += LTTR_CNT_VAL[sq.ltr]["val"]

        value = value * multi

        num_letters = len(sel_squares)
        if (self.first_word_down == 0 and num_letters > 6) or (num_letters > 7):
            value += 50
            print("INFO. All ltrs used", sq.ltr)

        if self.verbose:
            print("DEBUG. Value:", value)

        self.players[self.turn]["score"] += value
        
    def reset(self):
        pass

    def update_turn(self):
        self.turn = 3 - self.turn
        print("turn:", self.turn, "players:", self.players, "num ltrs left:", len(self.letters))

    def run(self):

        while self.running:

            self.update_turn()
            self.print()
            self.get_letters()
            self.place_word()
            

#################### Tests ####################
def test(args):
    self = Scr(args.automate, args.verbose)
    self.run()
    
##################### Main Function ####################
def main(args):
    if args.test == True:
        test(args)
    else:
        ch = Scr(args.automate, args.verbose)
        ch.run()

##################### Command-line Execution ####################
if __name__=="__main__":
    #args
    parser = argparse.ArgumentParser(description="ch")
    parser.add_argument("-a", "--automate", action="store_true", help="automate")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
    parser.add_argument("-t", "--test", action="store_true", help="test")

    args = parser.parse_args()
    print(args)
    main(args)
    



    
