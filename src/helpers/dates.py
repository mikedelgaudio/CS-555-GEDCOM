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

def us02BirthBeforeMarriage(birth,marriage):
    try:
        if(marriage == "N/A"):
            return True
        else:
            bsplit = birth.split()
            msplit = marriage.split()
            if(int(msplit[2]) > int(bsplit[2])):
                return True
            elif(datetime.datetime.strptime(msplit[1], '%b').month > datetime.datetime.strptime(bsplit[1], '%b').month and int(msplit[2]) == int(bsplit[2])):
                return True
            elif (int(msplit[0]) > int(bsplit[0]) and datetime.datetime.strptime(msplit[1], '%b').month == datetime.datetime.strptime(bsplit[1], '%b').month and int(msplit[2]) == int(bsplit[2])):
                return True
            else:
                return False
    except ValueError: #Need us42 to check format
        print("DATE PROVIDED IS INCORRECT FORMAT")
