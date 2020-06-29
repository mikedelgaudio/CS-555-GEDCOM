import datetime
from helpers import dates

def list_recent(individuals):
    for x in individuals:
        if(dates.dateChecker(x[6], -30, False)):
            day = x[6].split()[0]
            month = x[6].split()[1]
            print("US36: RECENT DEATH: " + x[1] + " died on " + month + " " + day + ".")
        if(dates.dateChecker(x[3], -30, False)):
            day = x[3].split()[0]
            month = x[3].split()[1]
            print("US35: RECENT BIRTH: " + x[1] + " was born on " + month + " " + day + "!")