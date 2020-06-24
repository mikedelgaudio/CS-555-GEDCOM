import datetime
from helpers import dates

def deaths(individuals):
    for x in individuals:
        if(dates.dateChecker(x[6], -30, False)):
            day = x[6].split()[0]
            month = x[6].split()[1]
            print("US36: DEATH: " + x[1] + " died on " + month + " " + day + ".")
