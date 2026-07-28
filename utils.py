#!C:\Program Files\Python312\python
import random
import copy
import argparse
import time
import os
import sys
from datetime import datetime

# Functions


def get_work_time():

    # Get current local date and time
    now = datetime.now()

    # Create a datetime object for 07:30 local time today
    target = now.replace(hour=6, minute=30, second=0, microsecond=0)

    # If it's currently before 07:30, you might want the 07:30 from yesterday
    # (Uncomment the block below if you want negative values or previous-day behavior)
    # if now < target:
    #     from datetime import timedelta
    #     target -= timedelta(days=1)

    # Calculate difference and get total hours
    diff = now - target
    hours_since = diff.total_seconds() / 3600

    money_since = hours_since * 86.06

    print("%2.2f($%5.2f)" % (hours_since, money_since) )

    return hours_since, money_since

######################################## CLASSES  ########################################


# Tests


# Main Function
def main(args):
    hours_since = 0.0
    money_since = 0.0
    if args.automate == True:
        while hours_since < 8.0:
            hours_since, money_since = get_work_time()
            time.sleep(60)
    else:
        get_work_time()

# Command-line Execution
if __name__=="__main__":
    #args
    parser = argparse.ArgumentParser(description="ch")
    parser.add_argument("-a", "--automate", action="store_true", help="automate")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
    parser.add_argument("-t", "--test", action="store_true", help="test")

    args = parser.parse_args()
    main(args)
    



    
