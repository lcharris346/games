#!C:\Program Files\Python312\python
import random
import copy
import argparse
import time
import os
import sys
from datetime import datetime

# Functions


def get_work_time(break_taken, verbose):
    print("work-pay \t    time, gross, net")

    # Get current local date and time
    now = datetime.now()
    net2gross = (4255.28 * 26.0) / 179000.0
    salary_per_day = 179000.0 / 365.23

    # Create a datetime object for 06:30 local time today
    target = now.replace(hour=6, minute=30, second=0, microsecond=0)
    diff = now - target
    hours_since = diff.total_seconds() / 3600 - break_taken
    if hours_since > 8.00:
        hours_since = 8.00
    gross_since = hours_since * 86.06
    print("today        \t%4.2f hrs, $%4.2f, $%4.2f" % (hours_since, gross_since, gross_since * net2gross) )

    if verbose == True:

        target2 = now.replace(year=2026, month=7, day=24)
        diff2 = now - target2
        days_since2 = diff2.days
        salary_since2 = days_since2 * salary_per_day
        print("pay-period   \t %d days, $%4.2f, $%4.2f" % (days_since2, salary_since2, salary_since2 * net2gross) )

        target3 = now.replace(year=2026, month=4, day=24)
        diff3 = now - target3
        days_since3 = diff3.days
        salary_since3 = days_since3 * salary_per_day
        print("year-to-date \t%d days, $%5.2f, $%4.2f" % (days_since3, salary_since3, salary_since3 * net2gross) )

        target4 = now.replace(year=2041, month=8, day=1)
        diff4 = target4 - now
        
        years_since4 = diff4.days / 365.23
        days_since4 = diff4.days % 365.23
        
        print("retirement \t%d years & %d days" % (years_since4, days_since4) )

    return hours_since

######################################## CLASSES  ########################################


# Tests


# Main Function
def main(args):
    hours_since = 0.0
    if args.automate == True:
        while hours_since < 8.0:
            hours_since = get_work_time(args.break_taken, args.verbose)
            time.sleep(60)
    else:
        get_work_time(args.break_taken, args.verbose)

# Command-line Execution
if __name__=="__main__":
    #args
    parser = argparse.ArgumentParser(description="ch")
    parser.add_argument("-a", "--automate", action="store_true", help="automate")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose")
    parser.add_argument("-t", "--test", action="store_true", help="test")
    parser.add_argument("-b", "--break_taken", type=float, default = 0.0, help="break_taken in hrs")

    args = parser.parse_args()
    main(args)
    



    
