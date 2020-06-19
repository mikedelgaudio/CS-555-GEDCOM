import datetime
from helpers import dates

def us29ListDeceased(individuals):
    for i in individuals:
        if(not dates.us42ValidDate(i[6])):
            pass
        if(not dates.us01DateAfterCurrentDate(i[6])):
            pass
        else:
            if(i[6] != "N/A"):
                print("US29: DEAD: " + i[0] +" " + i[1] + " died on " + i[6]+ ".")