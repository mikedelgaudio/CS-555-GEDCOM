import datetime
from helpers import dates

def birthdays(individuals):
    for x in individuals:
        if(dates.dateChecker(x[3], 30, True) and x[6] == "N/A"):
            day = x[3].split()[0]
            month = x[3].split()[1]
            print("US38: BDAY: " + x[1] + "'s birthday is on " + month + " " + day + "!")

def anniversary(individuals, families):
    error = 0
    for x in families:
        if x[2] == "N/A" and x[1] != "N/A":
            if (dates.dateChecker(x[1], 30, True)):
                husbID= x[3]
                husband=x[4]
                wifeID= x[5]
                wife= x[6]
                count=0
                for i in individuals:
                    if i[0] == husbID or i[0] == wifeID:
                        if i[6] == "N/A":
                            count+=1
                        else:
                            error +=1
                if count==2:
                    day = x[1].split()[0]
                    month = x[1].split()[1]
                    
                    print("US39: ANNIV: " + husband + " and " + wife + "'s anniversary is on " + month + " " + day + "!")
        else:
            error += 1
    if error > 0:
        return False
    else:
        return True
    
                    

     