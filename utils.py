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

    print("work-pay:\n time-frame \ttime\t\tgross\t\tnet")

    # Get current local date and time
    now = datetime.now()
    net2gross = (4255.28 * 26.0) / 179000.0
    salary_per_day = 179000.0 / 365.23

    # Create a datetime object for 06:30 local time today
    target = now.replace(hour=7, minute=0, second=0, microsecond=0)
    diff = now - target
    hours_since = diff.total_seconds() / 3600 - break_taken/60
    gross_since = hours_since * 86.06
    print(" today\t\t%4.2f hrs\t$%4.2f\t\t$%4.2f" % (hours_since, gross_since, gross_since * net2gross) )

    if verbose == True:

        target2 = now.replace(year=2026, month=8, day=7)
        diff2 = now - target2
        days_since2 = diff2.days
        while days_since2 >= 14:
            days_since2 = days_since2 - 14
        salary_since2 = days_since2 * salary_per_day
        print(" pay-period\t%d days\t\t$%4.2f\t$%4.2f" % (days_since2, salary_since2, salary_since2 * net2gross) )

        target3 = now.replace(year=2026, month=4, day=24)
        diff3 = now - target3
        days_since3 = diff3.days
        salary_since3 = days_since3 * salary_per_day
        print(" year-to-date\t%d days\t$%5.2f\t$%4.2f" % (days_since3, salary_since3, salary_since3 * net2gross) )

        print("countdowns:")

        target5 = now.replace(year=2027, month=4, day=24)
        diff5 = target5 - now
        years_since5 = diff5.days / 365.23
        days_since5 = diff5.days % 365.23
        months_since5 = days_since5 / 30
        days_since5b = days_since5 % 30
        print(" 1-yr at work\t %d months, %d days\tkeep $20k bonus" % (months_since5, days_since5b) )

        target6 = now.replace(year=2030, month=6, day=1)
        diff6 = target6 - now
        years_since6 = diff6.days / 365.23
        days_since6 = diff6.days % 365.23
        months_since6 = days_since6 / 30.44
        print(" child-support \t %d years,  %d months\tsave $966/mo" % (years_since6, months_since6) )

        target7 = now.replace(year=2031, month=1, day=1)
        diff7 = target7 - now
        years_since7 = diff7.days / 365.23
        days_since7 = diff7.days % 365.23
        months_since7 = days_since7 / 30.44
        print(" TRS  ret\t %d years,  %d months\tincome $3666/mo" % (years_since7, months_since7) )

        target4 = now.replace(year=2041, month=8, day=1)
        diff4 = target4 - now
        years_since4 = diff4.days / 365.23
        days_since4 = diff4.days % 365.23
        months_since4 = days_since4 / 30.44
        print(" 401k ret\t%d years, %d months" % (years_since4, months_since4) )

        target8 = now.replace(year=2046, month=8, day=1)
        diff8 = target8 - now
        years_since8 = diff8.days / 365.23
        days_since8 = diff8.days % 365.23
        months_since8 = days_since8 / 30.44
        print(" SS   ret\t%d years, %d months" % (years_since8, months_since8) )

        

        

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
    parser.add_argument("-b", "--break_taken", type=float, default = 0.0, help="break_taken in min")

    args = parser.parse_args()
    main(args)
    



    
