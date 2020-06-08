# Used for all helper functions related to dates

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