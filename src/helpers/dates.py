# Used for all helper functions related to dates
import datetime

#Takes in a date string and returns True if date is before present day or False if not
def us01DateAfterCurrentDate(date):            
    try:
        if(date == "N/A"):
            return True
        else: 
            #could implement check on us42 if the date is in correct format first
            strippedDate = datetime.datetime.strptime(date, "%d %b %Y")
            if(strippedDate < datetime.datetime.today()):
                return True
            else:
                return False
    except ValueError:
        print("DATE PROVIDED IS INCORRECT FORMAT")
        
#Takes in a date string and returns true or false if valid date
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
            print("ERROR: " + individuals[i][0] +" "+ individuals[i][1] + " cannot have birthday " + individuals[i][3] + " after current date.")
        if( us01DateAfterCurrentDate(individuals[i][6]) == False ):
            print("ERROR: " + individuals[i][0] +" "+ individuals[i][1] + " cannot have death date " + individuals[i][6] + " after current date.")
            
        if ( us42ValidDate(individuals[i][3]) == False):
            print("ERROR: " + individuals[i][0] +" "+ individuals[i][1] + " has an invalid birthday of " + individuals[i][3] +".")
        if ( us42ValidDate(individuals[i][6]) == False):
            print("ERROR: " + individuals[i][0] +" "+ individuals[i][1] + " has an invalid death date of " + individuals[i][6] +".")
            
    for j in range(len(families)):
        
        if (us01DateAfterCurrentDate(families[j][1]) == False):
            print("ERROR: Family ID " + families[j][0] +" cannot have a marriage date " + families[j][1] + " after current date.")
        if (us42ValidDate(families[j][2]) == False):
            print("ERROR: Family ID " + families[j][0] +" cannot have a divorce date " + families[j][2] + " after current date.")
            
        if (us42ValidDate(families[j][1]) == False):
            print("ERROR: Family ID " + families[j][0] +" has an invalid marriage date of " + families[j][1])
        if (us42ValidDate(families[j][2]) == False):
            print("ERROR: Family ID " + families[j][0] +" has an invalid divorce date of " + families[j][2])
            
        
        
