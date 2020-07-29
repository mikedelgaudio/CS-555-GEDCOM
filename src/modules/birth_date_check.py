import datetime
from helpers import dates

#Birth should occur before marriage of an individual
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
        return True

#Birth should occur before death of an individual
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
        return True

def less_than_150_years(birth, death):
    try:
        if death == "N/A":
            b_temp = datetime.datetime.strptime(birth, "%d %b %Y")
            b = datetime.datetime(b_temp.year + 150, b_temp.month, b_temp.day)
            return datetime.datetime.now() < b
        else:
            b = datetime.datetime.strptime(birth, "%d %b %Y")
            d = datetime.datetime.strptime(death, "%d %b %Y")
            if b > d:
                return True
            return ((d - b).days < 150*365)
    except ValueError:
        pass

#Children should be born after marriage of parents (and not more than 9 months after their divorce)
def birth_before_marriage_of_parents(birth,mar,div):
    try:
        m = None
        if mar != "N/A":
            m = datetime.datetime.strptime(mar, "%d %b %Y")
        b = datetime.datetime.strptime(birth, "%d %b %Y")
        d = None
        if m is None:
            return False
        if div != "N/A":
            d = datetime.datetime.strptime(div, "%d %b %Y")
        if b >= m and d is None:
            return True
        elif b < m and d is None:
            return False
        elif b >= m and dates.diff90(b,d):
            return True
        else:
            return False
    except ValueError:
        return True

#Child should be born before death of mother and before 9 months after death of father
def birth_before_death_of_parents(birth,mdeath,fdeath):
    try:
        b = datetime.datetime.strptime(birth, "%d %b %Y")
        md = None
        fd = None
        if mdeath != "N/A":
            md = datetime.datetime.strptime(mdeath, "%d %b %Y")
        if fdeath != "N/A":
            fd = datetime.datetime.strptime(fdeath, "%d %b %Y")
        if md is None and fd is None:
            return True
        if fd is None and md >= b:
            return True
        if md is None:
            if dates.diff90(b,fd):
                return True
            else:
                return False
        else:
            if md >= b:
                if dates.diff90(b,fd):
                    return True
                else:
                    return False
            else:
                return False
    except ValueError:
        return True

#Mother should be less than 60 years older than her children and father should be less than 80 years older than his children
def parents_too_old(birth,mbirth,fbirth):
    try:
        b = datetime.datetime.strptime(birth, "%d %b %Y")
        mb = datetime.datetime.strptime(mbirth, "%d %b %Y")
        fb = datetime.datetime.strptime(fbirth, "%d %b %Y")
        if dates.diff60y(b,mb) and dates.diff80y(b,fb):
            return True
        else:
            return False
    except ValueError:
        return True
