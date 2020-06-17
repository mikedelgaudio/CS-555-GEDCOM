import datetime

def birth_before_marriage(birth1,birth2,marriage):
    try:
        if(marriage == "N/A"):
            return True
        else:
            bsplit1 = birth1.split()
            bsplit2 = birth2.split()
            msplit = marriage.split()
            if(int(msplit[2]) > int(bsplit1[2]) and int(msplit[2]) > int(bsplit2[2])):
                return True
            elif(datetime.datetime.strptime(msplit[1], '%b').month > datetime.datetime.strptime(bsplit1[1], '%b').month and int(msplit[2]) == int(bsplit1[2]) and datetime.datetime.strptime(msplit[1], '%b').month > datetime.datetime.strptime(bsplit2[1], '%b').month and int(msplit[2]) == int(bsplit2[2])):
                return True
            elif (int(msplit[0]) > int(bsplit1[0]) and datetime.datetime.strptime(msplit[1], '%b').month == datetime.datetime.strptime(bsplit1[1], '%b').month and int(msplit[2]) == int(bsplit1[2]) and int(msplit[0]) > int(bsplit2[0]) and datetime.datetime.strptime(msplit[1], '%b').month == datetime.datetime.strptime(bsplit2[1], '%b').month and int(msplit[2]) == int(bsplit2[2])):
                return True
            else:
                return False
    except ValueError:
        print("DATE PROVIDED IS INCORRECT FORMAT")

def birth_before_death(birth,death):
    try:
        if(death == "N/A"):
            return True
        else:
            bsplit = birth.split()
            dsplit = death.split()
            if(int(dsplit[2]) > int(bsplit[2])):
                return True
            elif(datetime.datetime.strptime(dsplit[1], '%b').month > datetime.datetime.strptime(bsplit[1], '%b').month and int(dsplit[2]) == int(bsplit[2])):
                return True
            elif (int(dsplit[0]) > int(bsplit[0]) and datetime.datetime.strptime(dsplit[1], '%b').month == datetime.datetime.strptime(bsplit[1], '%b').month and int(dsplit[2]) == int(bsplit[2])):
                return True
            elif (int(dsplit[0]) == int(bsplit[0]) and datetime.datetime.strptime(dsplit[1], '%b').month == datetime.datetime.strptime(bsplit[1], '%b').month and int(dsplit[2]) == int(bsplit[2])):
                return True
            else:
                return False
    except ValueError:
        print("DATE PROVIDED IS INCORRECT FORMAT")
