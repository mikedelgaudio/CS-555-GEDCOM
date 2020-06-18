# Used for all helper functions related to dates
import datetime

months = {"JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
          "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12}

# Takes in a date string and returns True if date is before present day or False if not


def us01DateAfterCurrentDate(date):
    try:
        if(date == "N/A"):
            return True
        else:
            # could implement check on us42 if the date is in correct format first
            strippedDate = datetime.datetime.strptime(date, "%d %b %Y")
            if(strippedDate < datetime.datetime.today()):
                return True
            else:
                return False
    except ValueError:
        pass

# Takes in a date string and returns true or false if valid date


def us42ValidDate(date):
    try:
        if(date == "N/A"):
            return True
        datetime.datetime.strptime(date, "%d %b %Y")
        return True
    except ValueError:
        return False

        
def dateHelper(individuals, families):
    for i in range(len(individuals)):
        if(us01DateAfterCurrentDate(individuals[i][3]) == False):
            print("US01: ERROR: " + individuals[i][0] +" "+ individuals[i][1] + " cannot have birthday " + individuals[i][3] + " after current date.")
        if( us01DateAfterCurrentDate(individuals[i][6]) == False ):
            print("US01: ERROR: " + individuals[i][0] +" "+ individuals[i][1] + " cannot have death date " + individuals[i][6] + " after current date.")
            
        if ( us42ValidDate(individuals[i][3]) == False):
            print("US42: ERROR: " + individuals[i][0] +" "+ individuals[i][1] + " has an invalid birthday of " + individuals[i][3] +".")
        if ( us42ValidDate(individuals[i][6]) == False):
            print("US42: ERROR: " + individuals[i][0] +" "+ individuals[i][1] + " has an invalid death date of " + individuals[i][6] +".")
            
    for j in range(len(families)):
        
        if (us01DateAfterCurrentDate(families[j][1]) == False):
            print("US01: ERROR: Family ID " + families[j][0] +" cannot have a marriage date " + families[j][1] + " after current date.")
        if (us42ValidDate(families[j][2]) == False):
            print("US01: ERROR: Family ID " + families[j][0] +" cannot have a divorce date " + families[j][2] + " after current date.")
            
        if (us42ValidDate(families[j][1]) == False):
            print("US42: ERROR: Family ID " + families[j][0] +" has an invalid marriage date of " + families[j][1])
        if (us42ValidDate(families[j][2]) == False):
            print("US42: ERROR: Family ID " + families[j][0] +" has an invalid divorce date of " + families[j][2])
            
        
        



def next30days(date):
    if(not us42ValidDate(date)):
        return False
    try:
        if(date == "N/A"):
            return False
        today = datetime.datetime.now()
        compare = today + datetime.timedelta(30)
        day = date.split()[0]
        month = date.split()[1]
        date = datetime.datetime(int(today.year), months[month], int(day))
        
        if(compare >= date and today <= date):
            return True

        else:
            return False
    except ValueError:
        return False

