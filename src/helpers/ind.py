# Used for all helper functions related to individuals
import datetime
from helpers import dates

# Finds an individual from list l using passed in id. Returns the name of that individual
# does NOT work for family list
def findIndividual(id, l):
    for x in l:
        if id in x:
            return x[1]

    return "N/A"


months = {"JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
          "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12}

# calculates age either using todays date or death date if applicable


def ageCalculator(birthday, deathDate):
    if(not dates.us42ValidDate(birthday) or not dates.us42ValidDate(deathDate)):
        return "Invalid Date"
    if birthday != "N/A" :
        day = birthday.split()[0]
        month = birthday.split()[1]
        year = birthday.split()[2]
    else:
        return "N/A"
    if deathDate != "N/A":
        deathday = deathDate.split()[0]
        deathmonth = deathDate.split()[1]
        deathyear = deathDate.split()[2]
        
    if deathDate == "N/A":
        today = datetime.datetime.now()
        birth = datetime.datetime(int(year), months[month], int(day))
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        
    else:
        death = datetime.datetime(int(deathyear), months[deathmonth], int(deathday))
        birth = datetime.datetime(int(year), months[month], int(day))
        return death.year - birth.year - ((death.month, death.day) < (birth.month, birth.day))
        


# Adds required family info to individuals table such as spouse or child id
def fam_info_to_individual(individuals, families):
    count = 0
    for x in individuals:
        for i in families:
            if x[0] in i:
                x[8] = i[0]
            elif x[0] in i[7]:
                x[7] = i[0]
        count += 1
    return individuals
