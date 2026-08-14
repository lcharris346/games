#!C:\Program Files\Python312\python
import random
import copy
import argparse
import time
import os
import sys
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image

os.system('cls' if os.name == 'nt' else 'clear')
################## Constants ################################

OUTPUT = open("sample.txt").readlines()


NUM_VAL = {
    3: 1, 4:1, 
    5:2, 
    6:3, 
    7:5, 
    8:11, 9:11, 10:11, 11:11, 12:11
}

CUBE_LTTR = {
    0: {"ltrs":"EGNWEH","coord":(0,0), "conn": []},
    1: {"ltrs":"BAONOJ","coord":(1,0), "conn": []},
    2: {"ltrs":"NEAAEG","coord":(2,0), "conn": []},
    3: {"ltrs":"STYDUT","coord":(3,0), "conn": []},
    4: {"ltrs":"REVWTH","coord":(0,1), "conn": []},
    5: {"ltrs":"XILERD","coord":(1,1), "conn": []},
    6: {"ltrs":"CMTIOU","coord":(2,1), "conn": []},
    7: {"ltrs":"FAKFSP","coord":(3,1), "conn": []},
    8: {"ltrs":"LYROVE","coord":(0,2), "conn": []},
    9: {"ltrs":"QHIMNU","coord":(1,2), "conn": []},
   10: {"ltrs":"PCSHOA","coord":(2,2), "conn": []},
   11: {"ltrs":"NUESIE","coord":(3,2), "conn": []},
   12: {"ltrs":"LNRHNZ","coord":(0,3), "conn": []},
   13: {"ltrs":"LRETTY","coord":(1,3), "conn": []},
   14: {"ltrs":"EOISST","coord":(2,3), "conn": []},
   15: {"ltrs":"TOOTAM","coord":(3,3), "conn": []},
}

CUBES = list(range(0,16))
random.shuffle(CUBES)

COORD = [CUBE_LTTR[x]["coord"] for x in CUBES]
LTTR =  [CUBE_LTTR[x]["ltrs"] for x in CUBES]

VOWELS = "AEIOUY"

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

IMAGES = {x:Image.open("ltrs/" + x + ".png") for x in ALPHABET}

#print("DEBUG:", IMAGES.keys())


# Functions

def get_conn_cubes(cube, conn_cubes):
    if cube not in conn_cubes:
        conn_cubes.append(cube)
    test_cubes = [x for x in CUBES if x not in conn_cubes]
    c = COORD[cube]
    for test_cube in test_cubes:
        tc = COORD[test_cube]
        dist = ((c[0] - tc[0])**2 + (c[1] - tc[1])**2)**0.5
        if dist < 2:
            conn_cubes2 = copy.copy(conn_cubes)
            #print("DEBUG:", cube, test_cube, conn_cubes2)
            get_conn_cubes(test_cube, conn_cubes2)
            
            CUBE_LTTR[test_cube]["conn"].append(conn_cubes2)


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

def graph_ltrs(ltrs):
    

    # 1. Create a 4x4 grid of subplots
    fig, axs = plt.subplots(4, 4, figsize=(1,1))
    

    # 2. Flatten the 2D array of axes for easy 1D iteration
    axs = axs.ravel()

    # 3. Loop through your 16 images and plot them
    for ii in range(16):
        # Replace 'images[i]' with your actual image array/data
        ltr = ltrs[ii]
        lower_ltr = ltr.lower()
        angle = random.choice([0,90,180,-90])
        rotated_img = IMAGES[lower_ltr].rotate(angle)
        axs[ii].imshow(rotated_img)
    
        # Optional: Turn off axis lines and labels for cleaner look
        axs[ii].axis('off')

    # 4. Automatically adjust padding between subplots
    plt.tight_layout()
    fig.canvas.manager.window.geometry("160x160+-1850+800")

    # 6. show figure  non-blocking
    fig.set_facecolor('white')
    plt.subplots_adjust(wspace=0.1, hspace=0.1)
    plt.show(block = False)
    plt.pause(0.1)

######################################## Classes  ########################################
class BG(object):
    def __init__(self, args):
        self.automate = args.automate
        self.verbose = args.verbose
        self.cubes = copy.deepcopy(CUBE_LTTR)
        self.possible_words = None
        self.sc = 0
        self.ltrs = []
        self.words = []
        self.running = True
        self.start_time= time.perf_counter()
        self.timer = 0
        self.ctr = 0

    def print_ltrs(self):
        print("INFO: Ltrs:")
        print([x for x in self.ltrs[  : 4]])
        print([x for x in self.ltrs[ 4: 8]])
        print([x for x in self.ltrs[ 8:12]])
        print([x for x in self.ltrs[12:16]])

    

    def algorithm1(self):
        pass
        
    def choose_words(self):

        user_input = ""

        if self.automate == True:

            user_input = self.algorithm1()

        else:

            user_input = input("INPUT. Enter next word: ")

        if user_input == "q":
            print("INFO. quit")
            self.running = False
            return

        wd = user_input.upper()

        if self.validate_word(wd):

            self.words.append(wd)
            self.sc += NUM_VAL[len(wd)]
            print("INFO. wd: ", wd, " sc: ", self.sc)

        self.timer = (time.perf_counter() - self.start_time)

        print("INFO. Duration:", self.timer)

        self.ctr += 1

    def validate_word(self, wd):

        valid = True

        if not is_sublist(wd, self.ltrs):

            print("ERROR. wd ltrs are not on cube ltrs", wd)
            valid = False

        elif len(wd) < 3:

            print("ERROR. wd is too short", wd)
            valid = False

        elif wd in self.words :

            print("ERROR. wd already used", wd)
            valid = False

        return valid

    def shuffle_cubes(self):
        self.ltrs = [random.choice(LTTR[x]) for x in CUBES]
        self.words = []
        graph_ltrs(self.ltrs)

        if "q" in self.ltrs:
            ind_q  = self.ltrs.index("q")
            self.ltrs.insert(ind_q, "u")
            print("INFO. Added u for q in ltrs")

    def run(self):
        # shuffle 

        self.shuffle_cubes()
        
        while self.running == True and self.timer < 120:

            self.choose_words()

            self.ctr += 1

        print("INFO. sc: ", self.sc)

# Tests
def test(args):
    graph_ltrs(ALPHABET[:16])
    graph_ltrs(ALPHABET[10:26])
    input("end...")
    
# Main Function
def main(args):
    if args.test == True:
        test(args)
    else:
        bg = BG(args)
        bg.run()

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
    



    
