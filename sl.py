#!C:\Program Files\Python312\python
import random
import copy
import argparse
from symtable import Symbol
import time
import os
import sys
import matplotlib.pyplot as plt
import statistics

# Constants
OUTPUT = open("sample.txt").readlines()
COLUMNS = [0] *5
ROWS =  [[0] * 5] *3
PAYLINES = (

    # straight. 9
    #                       0 0 0 0 0
    #                       . . . . .
    #                       . . . . .
    (1,1,1),    (1,1,1,1),  (1,1,1,1,1),
    #                       . . . . .
    #                       0 0 0 0 0
    #                       . . . . .
    (2,2,2),    (2,2,2,2),  (2,2,2,2,2),
    #                       . . . . .
    #                       . . . . .
    #                       0 0 0 0 0
    (3,3,3),    (3,3,3,3),  (3,3,3,3,3),

    # Y-axis (bilateral) symmetry. 21
    # Valleys
    #                       0 0 . 0 0
    #                       . . 0 . .
    #                       . . . . .
    (1,1,2),    (1,1,2,1),  (1,1,2,1,1),    
    
    #                       0 0 . 0 0
    #                       . . . . .  
    #                       . . 0 . .
    (1,1,3),    (1,1,3,1),  (1,1,3,1,1),
    #                       0 . . . 0
    #                       . 0 0 0 .  
    #                       . . . . .
    (1,2,2),    (1,2,2,2),  (1,2,2,2,1),                  
    #                       0 . . . 0
    #                       . 0 . 0 .  
    #                       . . 0 . .
    (1,2,3),    (1,2,3,2),  (1,2,3,2,1),
    #                       0 . . . 0
    #                       . . . . .  
    #                       . 0 0 0 .
    (1,3,3),    (1,3,3,3),  (1,3,3,3,1),    
    #                       . . . . .
    #                       0 0 . 0 0  
    #                       . . 0 . .
    (2,2,3),    (2,2,3,2),  (2,2,3,2,2),
    #                       . . . . .
    #                       0 . . . 0  
    #                       . 0 0 0 .
    (2,3,3),    (2,3,3,3),  (2,3,3,3,2),    
                            

    # Hills. 21
    #                       . 0 0 0 .
    #                       0 . . . 0  
    #                       . . . . .
    (2,1,1),    (2,1,1,1),  (2,1,1,1,2),
    #                       . . 0 . .
    #                       0 0 . 0 0  
    #                       . . . . .
    (2,2,1),    (2,2,1,2),  (2,2,1,2,2),
    #                       . 0 0 0 .
    #                       . . . . .  
    #                       0 . . . 0
    (3,1,1),    (3,1,1,1),  (3,1,1,1,3),    
    #                       . . 0 . .
    #                       . 0 . 0 .  
    #                       0 . . . 0
    (3,2,1),    (3,2,1,2),  (3,2,1,2,3),
    #                       . . . . .
    #                       . 0 0 0 .  
    #                       0 . . . 0
    (3,2,2),    (3,2,2,2),  (3,2,2,2,3),
    #                       . . 0 . .
    #                       . . . . .  
    #                       0 0 . 0 0
    (3,3,1),    (3,3,1,3),  (3,3,1,3,3),
    #                       . . . . .
    #                       . . 0 . .  
    #                       0 0 . 0 0
    (3,3,2),    (3,3,2,3),  (3,3,2,3,3),
          
    # Ws. 15
    #                       0 . 0 . 0
    #                       . 0 . 0 .  
    #                       . . . . .
    (1,2,1),    (1,2,1,2),  (1,2,1,2,1),
    #                       0 . 0 . 0
    #                       . . . . .  
    #                       . 0 . 0 .
    (1,3,1),    (1,3,1,3),  (1,3,1,3,1),
    #                       0 . . . 0
    #                       . . 0 . .  
    #                       . 0 . 0 .
    (1,3,2),    (1,3,2,3),  (1,3,2,3,1),
    #                       . . 0 . .
    #                       0 . . . 0  
    #                       . 0 . 0 .
    (2,3,1),    (2,3,1,3),  (2,3,1,3,2),
    #                       . . . . .
    #                       0 . 0 . 0  
    #                       . 0 . 0 .
    (2,3,2),    (2,3,2,3),  (2,3,2,3,2),

    # Ms. 15
    #                       . 0 . 0 .
    #                       0 . 0 . 0  
    #                       . . . . .
    (2,1,2),    (2,1,2,1),  (2,1,2,1,2),    
    #                       . 0 . 0 .
    #                       0 . . . 0  
    #                       . . 0 . .
    (2,1,3),    (2,1,3,1),  (2,1,3,1,2),
    #                       . 0 . 0 .
    #                       . . 0 . .  
    #                       0 . . . 0
    (3,1,2),    (3,1,2,1),  (3,1,2,1,3),    
    #                       . 0 . 0 .
    #                       . . . . .  
    #                       0 . 0 . 0            
    (3,1,3),    (3,1,3,1),  (3,1,3,1,3),
    #                       . . . . .
    #                       . 0 . 0 .  
    #                       0 . 0 . 0
    (3,2,3),    (3,2,3,2),  (3,2,3,2,3),

    # Z-axis (rotational) symmetry
    # Ns. 8
    #                       0 . . 0 .
    #                       . . 0 . .  
    #                       . 0 . . 0
                (1,3,2,1),  (1,3,2,1,3),
    #                       . 0 . . .
    #                       0 . 0 . 0  
    #                       . . . 0 .
                (2,1,2,3),  (2,1,2,3,2),
    #                       . . . 0 .
    #                       0 . 0 . 0  
    #                       . 0 . . .
                (2,3,2,1),  (2,3,2,1,2),
    #                       . 0 . . 0
    #                       . . 0 . .  
    #                       0 . . 0 .
                (3,1,2,3),  (3,1,2,3,1),

    # Ss. 6
    #                       . . . . 0
    #                       . 0 0 0 .  
    #                       0 . . . .
                            (3,2,2,2,1),
    #                       0 0 . . .
    #                       . . 0 . .  
    #                       . . . 0 0   
                (1,1,2,3),  (1,1,2,3,3),
    #                       0 . . . .
    #                       . 0 0 0 .  
    #                       . . . . 0
                            (1,2,2,2,3),
    #                       . . . 0 0
    #                       . . 0 . .  
    #                       0 0 . . .
                (3,3,2,1),  (3,3,2,1,1),

    # Non-symmetric. 5
    #           . 0 0 . .
    #           0 . . 0 .  
    #           . . . . .
                (2,1,1,2),

    #           . . . . .
    #           0 . . 0 .  
    #           . 0 0 . .
                (2,3,3,2),

    #           . . . . .
    #           . 0 0 . .  
    #           0 . . 0 .
                (3,2,2,3),

    #           0 . . 0 .
    #           . 0 0 . .  
    #           . . . . .
                (1,2,2,1),

    #           . 0 0 . .
    #           . . . . .  
    #           0 . . 0.
                (3,1,1,3),
)
PAYLINES2 = []
for line in PAYLINES:
    line2 = list(line)
    line2[1] += 3
    line2[2] += 6
    if (len(line2)) > 3:
        line2[3] += 9
        if (len(line2)) > 4:
            line2[4] += 12
    PAYLINES2.append(line2)

MIN_VAL = 5

WLD = "WD "
FS  = "FS "
SYMBOLS = {
    "B  ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0},
    "C  ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0},
    "D  ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0},
    "E  ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0},
    "G  ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0},
    "H  ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0},
    "I  ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0},
    "10 ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0}, 
    "J  ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0}, 
    "Q  ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0}, 
    "K  ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0}, 
    "A  ": {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0},
       FS: {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0},
      WLD: {"worth":    MIN_VAL, "lines": [], "pay_lines": [],  "value": 0},
}

KEYS_SYMBOLS = list(SYMBOLS.keys())
LEN_SYMBOLS = len(KEYS_SYMBOLS)
DISTRO_SYMBOLS = []
for key in KEYS_SYMBOLS:
    cnt = int(1000 / SYMBOLS[key]["worth"])
    DISTRO_SYMBOLS += [key,]*cnt

MNY = {
    "10x": {"worth":   10, "lines": [], "pay_lines": [],  "value": 0},
    "20x": {"worth":   20, "lines": [], "pay_lines": [],  "value": 0},
    "30x": {"worth":   30, "lines": [], "pay_lines": [],  "value": 0},
    "40x": {"worth":   40, "lines": [], "pay_lines": [],  "value": 0},
    "50x": {"worth":   50 , "lines": [], "pay_lines": [],  "value": 0},
    "MNI": {"worth":  100, "lines": [], "pay_lines": [],  "value": 0},
    "MNR": {"worth":  200, "lines": [], "pay_lines": [],  "value": 0},
    "MXI": {"worth":  500, "lines": [], "pay_lines": [],  "value": 0},
    "MJR": {"worth": 1000, "lines": [], "pay_lines": [],  "value": 0},
    #"GRD": {"worth":10000, "lines": [], "pay_lines": [],  "value": 0},
}
GRAND_WORTH = MNY["MJR"]["worth"]*10
KEYS_MNY = list(MNY.keys())
LEN_MNY = len(KEYS_MNY)
DISTRO_MNY = []
for key in KEYS_MNY:
    cnt = int(1000 / MNY[key]["worth"])
    DISTRO_MNY += [key]*cnt

SYMBOLS_MNY = {}
SYMBOLS_MNY.update(SYMBOLS)
SYMBOLS_MNY.update(MNY)
LEN_SYMBOLS_MNY = LEN_SYMBOLS + LEN_MNY
KEYS_SYMBOLS_MNY = KEYS_SYMBOLS + KEYS_MNY
DISTRO_SYMBOLS_MNY = DISTRO_SYMBOLS + DISTRO_MNY

#print(DISTRO_SYMBOLS_MNY)
#sys.exit()

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
class SL(object):
    def __init__(self, threshold, denomination, credits, bankroll, automate, verbose):
        # credits = multiplier * num_lines
        # bet = credits * denomination = multiplier * num_lines * denomination
        # multiplier = credits / num_lines
        
        self.paylines = copy.deepcopy(PAYLINES2)
        self.num_lines = len(PAYLINES2)
        args.threshold = threshold
        self.denomination = denomination
        self.credits = credits
        self.bet = credits * denomination
        self.multiplier = self.bet / self.denomination / self.num_lines
        self.bankroll = bankroll
        self.automate = automate
        self.verbose = verbose
        self.mean_rtp = 0

        self.line_symbol_worth = 1.4 * self.bet / self.num_lines
        
        self.columns = copy.deepcopy(COLUMNS)
        self.rows = copy.deepcopy(ROWS)
        self.session_symbols = []
        self.num_fs = 0
        self.orbs = []
        self.symbols = copy.deepcopy(SYMBOLS_MNY)
        self.symbols_w_value = {}
        self.addition_ctr = 0
        self.ctr = 0
        self.max_ctr = 0
        self.win = 0

    def reset(self):
        self.columns = copy.deepcopy(COLUMNS)
        self.rows = copy.deepcopy(ROWS)
        self.session_symbols = []
        self.num_fs = 0
        self.num_orbs = []
        self.symbols = copy.deepcopy(SYMBOLS_MNY)
        self.symbols_w_value = {}
        self.addition_ctr = 0
        self.ctr = 0
        self.max_ctr = 0
        self.win = 0

    def free_spin(self):
        total_addition = 0
        for ii in range(3):
            #os.system("cls")
            my_print(("FS", ii+1))
            total_addition += self.spin()
            if self.verbose:
                time.sleep(0.2)
                user_input = input("FS >")
                if user_input in ("q", "e"):
                    sys.exit()

        my_print(("FS Complete.", total_addition))

        return total_addition
    
    def hold_and_spin(self):
        total_addition = 0
        rows = copy.deepcopy(self.rows)
        spins = 3
        orb_falls = False
        
        while spins > 0:
            #os.system("cls")
            num_orbs = 0
            my_print(("H&S", spins, "left"))
            orb_falls = False
            orbs = 0
            for row in range(3):
                for col in range(5):
                    if num_orbs < 14 or random.randint(1,200000) == 1: # Set GRAND odds
                        if rows[row][col] not in KEYS_MNY:
                            hs_symbols = DISTRO_MNY + [0] * (num_orbs + 1) ** 4
                            symbol = random.choice(hs_symbols)
                            if symbol in KEYS_MNY:
                                rows[row][col] = symbol
                                orb_falls = True
                                num_orbs += 1
                                orbs += MNY[symbol]["worth"]
                            else:
                                rows[row][col] = "   "
                        else:
                            orbs += MNY[rows[row][col]]["worth"]
                            num_orbs += 1
                            
                row_str = str(rows[row]).replace("'","")
                my_print(row_str)
            if num_orbs > 14:
                #if self.verbose:
                print(self.ctr, "GRAND!")
                total_addition += GRAND_WORTH
                return total_addition

            if orb_falls == False:
                spins -= 1
            my_print("")
            if self.verbose:
                time.sleep(0.2)
                user_input = input("H&S >")
                if user_input in ("q", "e"):
                    sys.exit()

        addition = self.denomination * self.multiplier *orbs
        total_addition += addition

        my_print(("H&S Complete.", total_addition))

        return total_addition
        
    def get_additions(self):
        total_addition = 0
        self.num_fs = 0
        self.orbs = []

        # free spins
        self.num_fs = len([x for x in self.session_symbols if x == FS])
        if self.num_fs > 2:
            my_print("FS!")
            total_addition += self.free_spin()
            if self.verbose:
                time.sleep(0.2)
            #self.addition_ctr += 1

        # hold and spin
        self.orbs = [MNY[x]["worth"] for x in self.session_symbols if x in KEYS_MNY]
        if len(self.orbs) > 4:
            my_print(("H&S!"))
            total_addition += self.hold_and_spin()
            if self.verbose:
                time.sleep(0.2)
            self.addition_ctr += 1
            

        return total_addition

    def get_paylines(self):
        paylines = 0
        self.symbols_w_value = {}
        for key in KEYS_SYMBOLS_MNY:
            total_value = 0
            for line in self.symbols[key]["lines"]:
                if line in self.paylines:
                    self.symbols[key]["pay_lines"].append(line)
                    value = self.line_symbol_worth * self.symbols[key]["worth"]*len(line)
                    total_value += value
            self.symbols[key]["value"] = total_value
            if total_value > 0:
                self.symbols_w_value[key] = (self.symbols[key])
                if self.verbose:
                    my_print(("LINES!", key, self.symbols_w_value[key]["pay_lines"], round(self.symbols_w_value[key]["value"],2)))
                    time.sleep(0.2)

            paylines += total_value

        return paylines
        
    def get_lines(self, indeces):

        indeces.sort()
        lines = []
        col1 = [ x for x in indeces if x >= 1  and x <= 3]
        col2 = [ x for x in indeces if x >= 4  and x <= 6]
        col3 = [ x for x in indeces if x >= 7  and x <= 9]
        col4 = [ x for x in indeces if x >= 10 and x <= 12]
        col5 = [ x for x in indeces if x >= 13 and x <= 15]
        for ii in col1:
            for jj in col2:
                for kk in col3:
                    line = [ii, jj, kk]
                    #if len(col4) == 0 and line not in lines:
                    lines.append(line)
                    #else:
                    for ll in col4:
                        line2 = line + [ll]
                        #if len(col5) == 0 and line not in lines:
                        lines.append(line2)                             
                        #else:
                        for mm in col5:
                            line3 = line2 + [mm]
                            lines.append(line3)

        return lines

    def get_session_lines(self):
        self.symbols = copy.deepcopy(SYMBOLS_MNY)
        symbols_keys = self.symbols.keys()
        for key in symbols_keys:
            indeces = list(set([ii+1 for ii,x in enumerate(self.session_symbols) if x in (key, WLD)]))
            self.symbols[key]["lines"] = self.get_lines(indeces)

    def get_session_symbols(self):
        self.session_symbols = []
        self.columns = copy.deepcopy(COLUMNS)
        for ii in range(5):

            self.columns[ii] = random.sample(DISTRO_SYMBOLS_MNY, 3)
            self.session_symbols += self.columns[ii]

        for jj in range(3):
            self.rows =  copy.deepcopy(ROWS)
            self.rows[jj] = [self.columns[0][jj], self.columns[1][jj], self.columns[2][jj], self.columns[3][jj], self.columns[4][jj]]
            row_str = str(self.rows[jj])
            my_print(row_str)

        my_print("")

    def spin(self):
        # init
        ret = 0
        if self.verbose:
            
            #os.system("clear")
            #os.system("cls")
            pass
        
        self.get_session_symbols()
        self.get_session_lines()
        paylines  = self.get_paylines()
        additions = self.get_additions()
        ret += paylines + additions

        return ret

    def run(self):

        # init
        self.reset()
        self.ctr = 0
        self.max_ctr = 180
        total_rtp = 0
        init_bankroll = self.bankroll 

        while self.bankroll > self.bet and self.ctr < self.max_ctr:

            # user input
            if not self.automate:
                user_input = input(">")
                if user_input in ("q", "e"):
                    break

            # spin
            ret = self.spin()
            self.ctr += 1
            if ret > GRAND_WORTH:
                break
            
            
            # update ret, bankroll, rtp
            self.win = ret - self.bet
            rtp = ret / self.bet
            total_rtp += rtp
            self.bankroll += self.win

            #results
            
            my_print(("ctr", self.ctr, "bet", -self.bet, "ret", round(ret,2), "br", round(self.bankroll,2), "\n"))
            
            if self.verbose:
                time.sleep(0.1)

            #else:
            #    if any((self.bankroll >= init_bankroll + args.threshold, self.win > args.threshold)):
            #        break
            

        self.mean_rtp = total_rtp / self.ctr
        #os.system("cls")
        my_print(("ctr", self.ctr, "br", round(self.bankroll,2), "mean-rtp", round(self.mean_rtp,4)))

# Tests
def test(args):
    self = SL(args.threshold, args.denomination, args.credits, args.bankroll, args.automate, args.verbose)

    self.session_symbols = []
    self.columns = copy.deepcopy(COLUMNS)
    for ii in range(5):

        self.columns[ii] = [WLD, WLD, WLD] #random.sample(DISTRO_SYMBOLS_MNY, 3)

        self.session_symbols += self.columns[ii]

    for jj in range(3):
        self.rows =  copy.deepcopy(ROWS)
        self.rows[jj] = [self.columns[0][jj], self.columns[1][jj], self.columns[2][jj], self.columns[3][jj], self.columns[4][jj]]
        row_str = str(self.rows[jj])
        my_print(row_str)

    my_print("")

    self.get_session_lines()
    self.get_paylines()

    for key in self.symbols.keys():
        value = self.symbols[key]
        print(key, value["value"])

    
    #sl.reset()
    #sl.run()
    #sl.spin()
    #sl.get_session_symbols()
    #sl.get_session_lines()
    #indeces = []
    #sl.get_lines(indeces)
    #sl.get_paylines()
    #sl.get_additions()
    #sl.free_spin()
    #sl.hold_and_spin()

# Main Function
def main(args):
    if args.test == True:
        test(args)
    else:
        final_bankroll_array = [0]*args.iterations
        final_rtp_array = [0]*args.iterations
        addition_ctr_array = [0]*args.iterations
        ctr_array = [0]*args.iterations
        succ_cnt = 0
        success = False
        
        for ii in range(args.iterations):

            if args.iterations > 1:

                args.automate = True
                args.verbose = False

            sl = SL(args.threshold, args.denomination, args.credits, args.bankroll, args.automate, args.verbose)
            sl.run()

            if any((sl.bankroll > args.bankroll, sl.win > args.threshold)):
                succ_cnt += 1

            final_rtp_array[ii] = sl.mean_rtp
            final_bankroll_array[ii] = sl.bankroll
            addition_ctr_array[ii] = sl.addition_ctr
            ctr_array[ii] = sl.ctr

        if args.iterations > 1:
            succ_ctr_array = [x for ii, x in enumerate(ctr_array) if final_bankroll_array[ii] > sl.bet ]
            succ_bankroll_array = [x for ii, x in enumerate(final_bankroll_array) if final_bankroll_array[ii] > sl.bet ]
            print("succ-pct:", succ_cnt/args.iterations,
                  "mean-succ-cnt:", statistics.mean(succ_ctr_array),
                  "max-succ-prf:", max(succ_bankroll_array)-args.bankroll, 
                  "mean-succ-pft:", statistics.mean(succ_bankroll_array)-args.bankroll,
                  "mean-pft:", statistics.mean(final_bankroll_array)-args.bankroll,
                  "mean-addition-cnt:", statistics.mean(addition_ctr_array), 
                  "mean-rtp", statistics.median(final_rtp_array))

# Command-line Execution
if __name__=="__main__":
    #args
    parser = argparse.ArgumentParser(description="vp")
    parser.add_argument("-b", "--bankroll", type=float, default=100, help="bankroll")
    parser.add_argument("-d", "--denomination", type=float, default=0.01, help="denomination")
    parser.add_argument("-c", "--credits", type=int, default=100, help="credits:100,200,300,...,1000")
    parser.add_argument("-i", "--iterations", type=int, default=1, help="iterations")
    parser.add_argument("-a", "--automate", action="store_true", help="automate")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
    parser.add_argument("-t", "--test", action="store_true", help="test")
    parser.add_argument("-e", "--threshold", type=float, default = 20, help="threshold")

    args = parser.parse_args()
    print(args)
    if args.iterations > 1:
        args.verbose = False
        args.automate = True
        def my_print(statement):
            pass
    main(args)
    



    
