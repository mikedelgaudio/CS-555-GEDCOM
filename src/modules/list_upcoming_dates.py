import datetime
from helpers import dates

def birthdays(individuals):
    for x in individuals:
        if(dates.next30days(x[3]) and x[6] == "N/A"):
            day = x[3].split()[0]
            month = x[3].split()[1]
            print("BDAY: " + x[1] + "'s birthday is on " + month + " " + day + "!")

def anniversary(individuals, families):
    for x in families:
        if x[2] == "N/A":
            if (dates.next30days(x[1])):
                husbID= x[3]
                husband=x[4]
                wifeID= x[5]
                wife= x[6]
                count=0
                for i in individuals:
                    if i[0] == husbID or i[0] == wifeID:
                        if i[6] != "N/A":
                            count+=1
                if count==2:
                    day = x[1].split()[0]
                    month = x[1].split()[1]
                    
                    print("ANNIV: " + husband + " and " + wife + "'s anniversary is on " + month + " " + day + "!")
                    
    
                    

     