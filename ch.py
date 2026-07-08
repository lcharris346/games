#!C:\Program Files\Python312\python
import random
import copy
import argparse
import time
import os
import sys

################################ Constants, Supporting Classes  #################################
# Output
OUTPUT = open("sample.txt").readlines()

# Mobility
DIR_COORD = { "e": (1,0),  "n": (0,1),   "w": (-1,0),  "s": (0,-1),
       "me": (1,1), "nw": (1,-1), "se": (-1,1), "sw": (-1,-1),
       "ene": (2,1), "nnw": (1,2),  "nnw": (-1,2), "wnw": ( -2,1),
       "ese": (2,-1), "sse": (1,-2),  "ssw": (-2,-1), "wsw": (-1,-2)}

FWD =   ("n",)
FWD_DIAG = ("ne", "nw")
DIAG =  ("ne","nw","sw","se")
STR  =  ("e","n","w","s")
STR_DIAG = ("e", "ne","n","nw","w","sw","s","se")
EL =  ("ene", "nne", "nnw", "wnw", "ese", "sse","ssw", "wsw")

# State
STATE  = {"my_targets": [], "my_supports": [], "my_paths": [],  "targeting_me": False, "supporting_me": [],  "paths_near_me": []}

# Pieces
PIECE_TYPES = ("king", "queen", "bishop", "knight", "rook", "pawn")

PIECE_NAMES = ("baR", "bbN", "bcB", "bK ", "bQ ", "bfB", "bgN", "bhR",
               "bap", "bbp", "bcp", "bdp", "bep", "bfp", "bgp", "bhp",
               "wap", "wbp", "wcp", "wdp", "wep", "wfp", "wgp", "bhp", 
               "waR", "wbN", "wcB", "wK ", "wQ ", "wfB", "wgN", "whR")

class Piece(object):

    def __init__(self, name, _type, value, target_dir, path_dir, path_range):

        self.name = name
        self.type = _type
        self.value = value
        
        self.target_dir = target_dir
        self.path_dir = path_dir
        self.path_range = path_range
        
        self.pos = ""
        self.color = self.name[0]
        self.state = copy.deepcopy(STATE)
        self.is_king = False
        self.in_check = False

    def update_pos(self, pos):
        self.pos = pos

    # update my squares
    def update_state1(self):    
        pass

    # update squares aimed at me
    def update_state2(self):    
        pass

class King(Piece):
    def __init__(self, name,):
        super().__init__(name, "king",   1e6, STR_DIAG, STR_DIAG, 1)

class Queen(Piece):
    def __init__(self, name):
        super().__init__(name, "queen",    9,  STR_DIAG, STR_DIAG, 7)

class Bishop(Piece):
    def __init__(self, name):
        super().__init__(name, "bishop", 3.3, DIAG,     DIAG, 7)

class Knight(Piece):
    def __init__(self, name):
        super().__init__(name, "knight",   3, EL,       EL, 1)

class Rook(Piece):
    def __init__(self, name):
        super().__init__(name, "rook",     5, STR,      STR, 7)

class Pawn(Piece):
    def __init__(self, name):
        super().__init__(name, "pawn",     1, FWD_DIAG, FWD, 1)

class NoPiece(Piece):
    def __init__(self, name):
        super().__init__(name, "none",     0, (), (), 0)



    

# Squares
POS_IND = {"n0": (0,0)}
LTTR = "abcdefgh"
NMBR = range(1,9)
for ii,ll in enumerate(LTTR):
    for nn in NMBR:
        POS_IND[ll + str(nn)] = (ii+1, nn)

POSITIONS = sorted(POS_IND.keys())
COORDS = [ POS_IND[pos] for pos in POSITIONS ]

class Square(object):
    def __init__(self, pos, piece):
        self.pos = pos
        self.piece = piece
        
        self.coord = POS_IND[pos]
        self.piece.update_pos(self.pos)

# Board
BOARD = { x: Square(x, NoPiece(" + ")) for x in POSITIONS}

BOARD["a1"] = Square("a1", Rook("waR"))
BOARD["b1"] = Square("b1", Knight("wbN"))
BOARD["c1"] = Square("c1", Bishop("wcB"))
BOARD["d1"] = Square("d1", King("wK "))
BOARD["e1"] = Square("e1", Queen("wQ "))
BOARD["f1"] = Square("f1", Bishop("wfB"))
BOARD["g1"] = Square("g1", Knight("wgN"))
BOARD["h1"] = Square("h1", Rook("whR"))

BOARD["a2"] = Square("a2", Pawn("wap"))
BOARD["b2"] = Square("b2", Pawn("wbp"))
BOARD["c2"] = Square("c2", Pawn("wcp"))
BOARD["d2"] = Square("d2", Pawn("wdp"))
BOARD["e2"] = Square("e2", Pawn("wep"))
BOARD["f2"] = Square("f2", Pawn("wfp"))
BOARD["g2"] = Square("g2", Pawn("wgp"))
BOARD["h2"] = Square("h2", Pawn("whp"))


BOARD["a7"] = Square("a7", Pawn("bap"))
BOARD["b7"] = Square("b7", Pawn("bbp"))
BOARD["c7"] = Square("c7", Pawn("bcp"))
BOARD["d7"] = Square("d7", Pawn("bdp"))
BOARD["e7"] = Square("e7", Pawn("bep"))
BOARD["f7"] = Square("f7", Pawn("bfp"))
BOARD["g7"] = Square("g7", Pawn("bgp"))
BOARD["h7"] = Square("h7", Pawn("bhp"))

BOARD["a8"] = Square("a8", Rook("baR"))
BOARD["b8"] = Square("b8", Knight("bbN"))
BOARD["c8"] = Square("c8", Bishop("bcB"))
BOARD["d8"] = Square("d8", King("bK "))
BOARD["e8"] = Square("e8", Queen("bQ "))
BOARD["f8"] = Square("f8", Bishop("bfB"))
BOARD["g8"] = Square("g8", Knight("bgN"))
BOARD["h8"] = Square("h8", Rook("bhR"))

# Prison
PRISON_PIECES = {"w": [], "b": []}

################################ Functions 2 ################################
def my_decorator(func):
    def wrapper(statement):
        choice = random.choice(range(len(OUTPUT)))
        line = str(statement).replace("'","").replace(",","") +" "+ OUTPUT[choice].rstrip("\n")
        func(line)
    return wrapper

@my_decorator
def my_print(statement):
    print(statement)

def print_board(board):
     line = " ".join( (board["a8"].piece.name, board["b8"].piece.name,board["c8"].piece.name,board["d8"].piece.name,
              board["e8"].piece.name, board["f8"].piece.name,board["g8"].piece.name,board["h8"].piece.name) )
     my_print( line)

     line = " ".join( (board["a7"].piece.name, board["b7"].piece.name,board["c7"].piece.name,board["d7"].piece.name,
              board["e7"].piece.name, board["f7"].piece.name,board["g7"].piece.name,board["h7"].piece.name) )
     my_print( line)

     line = " ".join( (board["a6"].piece.name, board["b6"].piece.name,board["c6"].piece.name,board["d6"].piece.name,
              board["e6"].piece.name, board["f6"].piece.name,board["g6"].piece.name,board["h6"].piece.name) )
     my_print( line)

     line = " ".join( (board["a5"].piece.name, board["b5"].piece.name,board["c5"].piece.name,board["d5"].piece.name,
              board["e5"].piece.name, board["f5"].piece.name,board["g5"].piece.name,board["h5"].piece.name) )
     my_print( line)

     line = " ".join( (board["a4"].piece.name, board["b4"].piece.name,board["c4"].piece.name,board["d4"].piece.name,
              board["e4"].piece.name, board["f4"].piece.name,board["g4"].piece.name,board["h4"].piece.name) )
     my_print( line)

     line = " ".join( (board["a3"].piece.name, board["b3"].piece.name,board["c3"].piece.name,board["d3"].piece.name,
              board["e3"].piece.name, board["f3"].piece.name,board["g3"].piece.name,board["h3"].piece.name) )
     my_print( line)

     line = " ".join( (board["a2"].piece.name, board["b2"].piece.name,board["c2"].piece.name,board["d2"].piece.name,
              board["e2"].piece.name, board["f2"].piece.name,board["g2"].piece.name,board["h2"].piece.name) )
     my_print( line)

     line = " ".join( (board["a1"].piece.name, board["b1"].piece.name,board["c1"].piece.name,board["d1"].piece.name,
              board["e1"].piece.name, board["f1"].piece.name,board["g1"].piece.name,board["h1"].piece.name) )
     my_print( line)


################################ TESTS ################################
def test(ch):
    print_board(ch.board)

######################################## Main Class  ########################################

class CH(object):
    def __init__(self, automate, verbose):
        self.automate = automate
        self.verbose = verbose

        
        self.board = copy.deepcopy(BOARD)
        self.turn = "w"

    def reset(self):
        pass

    def update_turn(self):
        self.turn == "b" if self.turn == "w" else "w"

    def update_piece_pos(self):
        pass

    def update_piece_state1(self):
        pass

    def update_piece_state2(self):
        pass


    def run(self):

        pass



    

# Main Function
def main(args):
    ch = CH(args.automate, args.verbose)
    if args.test == True:
        test(ch)
    else:
        ch.run()

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
    



    
