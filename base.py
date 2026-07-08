#!C:\Program Files\Python312\python
import random
import copy
import argparse
import time
import os
import sys

# Constants
OUTPUT = open("sample.txt").readlines()

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
class Base(object):
    def __init__(self):
        pass

    def reset(self):
        pass


    def run(self):

        pass

# Tests
def test(args):
    self = Base()

# Main Function
def main(args):
    if args.test == True:
        test(args.automate, args.verbose)
    else:
        ch = Base(args.automate, args.verbose)
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
    



    
