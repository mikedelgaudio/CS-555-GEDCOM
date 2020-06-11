import datetime
from helpers import dates

def birthdays(individuals):
    for x in individuals:
        if(dates.next30days(x[3])):
            day = x[3].split()[0]
            month = x[3].split()[1]
            print("BDAY: " + x[1] + "'s birthday is on " + month + " " + day + "!")
           