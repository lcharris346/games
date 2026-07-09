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
DIR_COORD = { "e": (1, 0),    "n": ( 0, 1),     "w": (-1, 0),    "s": ( 0,-1),
             "ne": (1, 1),   "nw": (-1, 1),    "se": ( 1,-1),   "sw": (-1,-1),
            "ene": (2, 1),  "nne": ( 1, 2),   "nnw": (-1, 2),  "wnw": (-2, 1),
            "ese": (2,-1),  "sse": ( 1,-2),   "ssw": (-1,-2),  "wsw": (-2,-1) }

FWD =   ("n",)
BACK =   ("s",)
FWD_DIAG = ("ne", "nw")
BACK_DIAG = ("se", "sw")
DIAG =  ("ne","nw","sw","se")
STR  =  ("e","n","w","s")
STR_DIAG = ("e", "ne","n","nw","w","sw","s","se")
EL =  ("ene", "nne", "nnw", "wnw", "ese", "sse","ssw", "wsw")

# State
STATE  = {"my_targets": set(), "my_supports": set(), "my_paths": set(),  "targeting_me": set(), "supporting_me": set(),  "paths_near_me": set()}

# Pieces
PIECE_TYPES = ("king", "queen", "bishop", "knight", "rook", "pawn")

PIECE_NAMES = ("bR", "bN", "bB", "bK", "bQ", "bB", "bN", "bR",
               "bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp",
               "wp", "wp", "wp", "wp", "wp", "wp", "wp", "bp", 
               "wR", "wN", "wB", "wK", "wQ", "wB", "wN", "wR")

# Squares, Positions, Coordinates
POS_COORD = {}
LTTR = "abcdefgh"
NMBR = range(1,9)
for ii,ll in enumerate(LTTR):
    for nn in NMBR:
        POS_COORD[ll + str(nn)] = (ii+1, nn)

POSITIONS = sorted(POS_COORD.keys())
COORD_POS = { POS_COORD[pos]:pos for pos in POSITIONS }

def get_pos(pos1, _dir, path_range):
    coord1 = POS_COORD[pos1]
    dir_coord = DIR_COORD[_dir]
    coord2 = (coord1[0] + dir_coord[0] * path_range, coord1[1]+ dir_coord[1] * path_range)
    pos2 = COORD_POS[coord2] if coord2 in COORD_POS.keys() else ""
    return pos2

def print_labels():
    print("   a8 b8 c8 d8 e8 f8 g8 h8 ")
    print("   a7 b7 c7 d7 e7 f7 g7 h7 ")
    print("   a6 b6 c6 d6 e6 f6 g6 h6 ")
    print("   a5 b5 c5 d5 e5 f5 g5 h5 ")
    print("   a4 b4 c4 d4 e4 f4 g4 h4 ")
    print("   a3 b3 c3 d3 e3 f3 g3 h3 ")
    print("   a2 b2 c2 d2 e2 f2 g2 h2 ")
    print("   a1 b1 c1 d1 e1 f1 g1 h1 ")

#Pieces

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
        self.prev_state = None
        self.is_king = False
        self.in_check = False
        self.check_mate = False
        self.moved = False

    def update_pos(self, pos):
        if pos != self.pos:
            self.pos = pos
            if self.moved == False: 
                self.moved = True
                if self.type == "pawn":
                    self.path_range = 1
        

    def reset_state(self):
        self.prev_state = copy.deepcopy(self.state)
        for key in self.state:
            self.state[key] = set()

    def update_state(self, w_pos, b_pos, e_pos, board):
        self.reset_state()
        friendly_pos = w_pos if self.color == "w" else b_pos
        enemy_pos    = b_pos if self.color == "w" else w_pos
        
        for _dir in self.path_dir:
            for rng in range(self.path_range):
                 test_pos =  get_pos(self.pos, _dir, rng + 1)
                 if test_pos in friendly_pos:
                     if self.type != "pawn":
                        self.state["my_supports"].add(test_pos)
                        board[test_pos].piece.state["supporting_me"].add(self.pos)
                     break
                 elif test_pos in enemy_pos:
                     if self.type != "pawn":                   
                        self.state["my_targets"].add(test_pos)
                        board[test_pos].piece.state["targeting_me"].add(self.pos)
                     break
                 elif test_pos in e_pos:
                     self.state["my_paths"].add(test_pos)

        if self.type == "pawn":
            for _dir in self.target_dir:
                test_pos =  get_pos(self.pos, _dir, 1)
                if test_pos in friendly_pos:
                    self.state["my_supports"].add(test_pos)
                    board[test_pos].piece.state["supporting_me"].add(self.pos)
                elif test_pos in enemy_pos:
                    self.state["my_targets"].add(test_pos)
                    board[test_pos].piece.state["targeting_me"].add(self.pos)
                    
        #if self.type != "none":
		  #     print("State", self.pos, self.name, self.state)
			

   
class King(Piece):
    def __init__(self, name,):
        super().__init__(name, "king",   1e6, STR_DIAG, STR_DIAG, 1)

class Queen(Piece):
    def __init__(self, name):
        super().__init__(name, "queen",    9, STR_DIAG, STR_DIAG, 7)

class Bishop(Piece):
    def __init__(self, name):
        super().__init__(name, "bishop", 3.3, DIAG,     DIAG, 7)

class Knight(Piece):
    def __init__(self, name):
        super().__init__(name, "knight",   3, EL,       EL, 1)

class Rook(Piece):
    def __init__(self, name):
        super().__init__(name, "rook",     5, STR,      STR, 7)

class WhitePawn(Piece):
    def __init__(self, name):
        super().__init__(name, "pawn",     1, FWD_DIAG, FWD, 2)

class BlackPawn(Piece):
    def __init__(self, name):
        super().__init__(name, "pawn",     1, BACK_DIAG, BACK, 2)

class NoPiece(Piece):
    def __init__(self, name):
        super().__init__(name, "none",     0, (), (), 0)


# Positions
class Square(object):
    def __init__(self, pos, piece):
        self.pos = pos
        self.piece = piece
        self.coord = POS_COORD[pos]
        self.piece.pos = self.pos

    def update_piece(self, piece):
        old_piece = copy.deepcopy(self.piece)
        self.piece = piece
        self.piece.update_pos(self.pos)
        return old_piece



# Board
BOARD = { x: Square(x, NoPiece("n ")) for x in POSITIONS}

BOARD["a1"] = Square("a1", Rook("wR"))
BOARD["b1"] = Square("b1", Knight("wN"))
BOARD["c1"] = Square("c1", Bishop("wB"))
BOARD["d1"] = Square("d1", King("wK"))
BOARD["e1"] = Square("e1", Queen("wQ"))
BOARD["f1"] = Square("f1", Bishop("wB"))
BOARD["g1"] = Square("g1", Knight("wN"))
BOARD["h1"] = Square("h1", Rook("wR"))

BOARD["a2"] = Square("a2", WhitePawn("wp"))
BOARD["b2"] = Square("b2", WhitePawn("wp"))
BOARD["c2"] = Square("c2", WhitePawn("wp"))
BOARD["d2"] = Square("d2", WhitePawn("wp"))
BOARD["e2"] = Square("e2", WhitePawn("wp"))
BOARD["f2"] = Square("f2", WhitePawn("wp"))
BOARD["g2"] = Square("g2", WhitePawn("wp"))
BOARD["h2"] = Square("h2", WhitePawn("wp"))


BOARD["a7"] = Square("a7", BlackPawn("bp"))
BOARD["b7"] = Square("b7", BlackPawn("bp"))
BOARD["c7"] = Square("c7", BlackPawn("bp"))
BOARD["d7"] = Square("d7", BlackPawn("bp"))
BOARD["e7"] = Square("e7", BlackPawn("bp"))
BOARD["f7"] = Square("f7", BlackPawn("bp"))
BOARD["g7"] = Square("g7", BlackPawn("bp"))
BOARD["h7"] = Square("h7", BlackPawn("bp"))

BOARD["a8"] = Square("a8", Rook("bR"))
BOARD["b8"] = Square("b8", Knight("bN"))
BOARD["c8"] = Square("c8", Bishop("bB"))
BOARD["d8"] = Square("d8", King("bK"))
BOARD["e8"] = Square("e8", Queen("bQ"))
BOARD["f8"] = Square("f8", Bishop("bB"))
BOARD["g8"] = Square("g8", Knight("bN"))
BOARD["h8"] = Square("h8", Rook("bR"))

BOARD_KEYS = BOARD.keys()

# Pieces
PIECES = { BOARD[x].piece: x for x in BOARD_KEYS }
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
     line = "  A  B  C  D  E  F  G  H   "
     my_print( line)
     line = " ".join(("8", board["a8"].piece.name, board["b8"].piece.name,board["c8"].piece.name,board["d8"].piece.name,
              board["e8"].piece.name, board["f8"].piece.name,board["g8"].piece.name,board["h8"].piece.name, "8") )
     my_print( line)

     line = " ".join( ("7", board["a7"].piece.name, board["b7"].piece.name,board["c7"].piece.name,board["d7"].piece.name,
              board["e7"].piece.name, board["f7"].piece.name,board["g7"].piece.name,board["h7"].piece.name, "7") )
     my_print( line)

     line = " ".join( ("6", board["a6"].piece.name, board["b6"].piece.name,board["c6"].piece.name,board["d6"].piece.name,
              board["e6"].piece.name, board["f6"].piece.name,board["g6"].piece.name,board["h6"].piece.name, "6") )
     my_print( line)

     line = " ".join( ("5", board["a5"].piece.name, board["b5"].piece.name,board["c5"].piece.name,board["d5"].piece.name,
              board["e5"].piece.name, board["f5"].piece.name,board["g5"].piece.name,board["h5"].piece.name, "5") )
     my_print( line)

     line = " ".join( ("4", board["a4"].piece.name, board["b4"].piece.name,board["c4"].piece.name,board["d4"].piece.name,
              board["e4"].piece.name, board["f4"].piece.name,board["g4"].piece.name,board["h4"].piece.name, "4") )
     my_print( line)

     line = " ".join( ("3", board["a3"].piece.name, board["b3"].piece.name,board["c3"].piece.name,board["d3"].piece.name,
              board["e3"].piece.name, board["f3"].piece.name,board["g3"].piece.name,board["h3"].piece.name, "3") )
     my_print( line)

     line = " ".join( ("2", board["a2"].piece.name, board["b2"].piece.name,board["c2"].piece.name,board["d2"].piece.name,
              board["e2"].piece.name, board["f2"].piece.name,board["g2"].piece.name,board["h2"].piece.name, "2") )
     my_print( line)

     line = " ".join( ("1", board["a1"].piece.name, board["b1"].piece.name,board["c1"].piece.name,board["d1"].piece.name,
              board["e1"].piece.name, board["f1"].piece.name,board["g1"].piece.name,board["h1"].piece.name, "1") )
     my_print( line)

     line = "  A  B  C  D  E  F  G  H   "
     my_print( line)


######################################## Main Class  ########################################

class CH(object):
    def __init__(self, automate, verbose):
        self.automate = automate
        self.verbose = verbose

        self.board = copy.deepcopy(BOARD)
        self.prison = copy.deepcopy(PRISON_PIECES)
        self.pieces = copy.deepcopy(PIECES)
        self.turn  = "b"
        self.w_pos = []
        self.b_pos = []
        self.e_pos = []
        self.w_b_pos = []
        self.running = True
        self.ctr = 0

    def update_turn(self):
        self.turn = "b" if self.turn == "w" else "w"
        print("Ctr", self.ctr, "Turn:", self.turn)

    def update_teams(self):
        self.w_pos = [x for x in BOARD_KEYS if self.board[x].piece.color == "w" ]
        self.b_pos = [x for x in BOARD_KEYS if self.board[x].piece.color == "b" ]
        self.e_pos = [x for x in BOARD_KEYS if self.board[x].piece.color == "n" ]

    def update_pieces(self):
        self.pieces = { self.board[x].piece: x for x in BOARD_KEYS }

    def update_piece_states(self):
        for pos in BOARD_KEYS:
            piece = self.board[pos].piece
            piece.update_state(self.w_pos, self.b_pos, self.e_pos, self.board)

    def evaluate_check(self):
        ctr = 0
        for pos in BOARD_KEYS:
            piece = self.board[pos].piece
            if piece.is_king:
                if len(piece.state["targeting_me"]) > 0:
                    piece.is_check = True
                    if len(piece.state["my_paths"]) == 0:
                        piece.check_mate = True
                        self.running = False
                        print("CheckMate!")
                        return
                else:
                    piece.is_check = False

                ctr += 1
                if ctr >= 2:
                    return
        
    def algorithm1(self):
		  
        mobile_piece_pos = {}
        
        pos_of_enemy_targets = []
        pos_of_enemy_paths = []
        for x in BOARD_KEYS:
           if self.board[x].piece.color != self.turn:
              pos_of_enemy_targets.append(self.board[x].piece.state["my_targets"])
              pos_of_enemy_paths.append(self.board[x].piece.state["my_paths"])

        
		  
        for x in BOARD_KEYS:
           if self.board[x].piece.color == self.turn:
              if   len(self.board[x].piece.state["my_targets"]) > 0:
                   mobile_piece_pos[x] = self.board[x].piece.state["my_targets"]
             
                   
              elif len(self.board[x].piece.state["my_paths"])   > 0:
                 paths = []
                 for pos in self.board[x].piece.state["my_paths"]:
                    if pos not in pos_of_enemy_paths:
                       paths.append(pos)
                       break
                 if len(paths) == 0:
                    paths = self.board[x].piece.state["my_paths"][0]
                 mobile_piece_pos[x] = paths

           if x in mobile_piece_pos.keys() and x in pos_of_enemy_targets:
               break
              
		  
        if len(mobile_piece_pos) == 0:
            self.running = False
            return "q,q"
		      
        curr_pos = random.choice(list(mobile_piece_pos.keys()))
        new_pos =  random.choice(list(mobile_piece_pos[curr_pos]))
		  
        return curr_pos +","+ new_pos
		  

    def move_piece(self):

        #selet piece pos
        print("prison:", self.prison)
        print_board(self.board)
        
        if self.automate == False and self.turn == "w":
            user_input = input("Enter curr_pos,new_pos:")
        else:
            user_input = self.algorithm1()
            input("algorith choice: " + user_input)
            if user_input.find("q") > -1:
                return

        if user_input.find("q") > -1:
            self.running = False
            return

        curr_pos, new_pos = user_input.split(",")

        if curr_pos not in BOARD_KEYS:
            print("ERROR! invalid board position")
            return

        piece = self.board[curr_pos].piece

        if piece.color != self.turn:
            print("ERROR! Wrong Color:", piece.color)
            return

        my_targets_paths = set(list(piece.state["my_targets"]) + list(piece.state["my_paths"]))

        if len(my_targets_paths) < 1:
            print("ERROR! Piece has no targets/paths")
            return
            
        #print(curr_pos, piece.name, my_targets_paths)

        if new_pos not in my_targets_paths:
            print("ERROR! invalid board position:", )
            return

        old_piece = self.board[new_pos].update_piece(piece)
        if old_piece.color != "n":
            self.prison[old_piece.color].append(old_piece.name)
        moved_piece = self.board[curr_pos].update_piece(NoPiece("n "))
        
        #print("INFO. ", 	self.board[new_pos].piece.name, curr_pos, new_pos)

    def select_dest_pos(self):
        pass

    def advance(self):
        
        self.update_turn()
        self.update_teams()
        self.update_pieces()
        self.update_piece_states()
        self.evaluate_check()
        self.move_piece()
        

    def run(self):
        while self.running:
            self.advance()
            self.ctr += 1
        print("INFO. Program ended")

        

################################ TESTS ################################
def test(self):
    self.run()
    


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
    



    
