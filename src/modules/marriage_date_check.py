import datetime

# Compares two spouces death dates against their marriage date to ensure both are less than it
def marriage_before_death(death_date1, death_date2, marriage_date):
    try:
        m = datetime.datetime.strptime(marriage_date, "%d %b %Y")
        d_1 = None
        d_2 = None
        if death_date1 != "N/A":
            d_1 = datetime.datetime.strptime(death_date1, "%d %b %Y")
            
        if death_date2 != "N/A":
            d_2 = datetime.datetime.strptime(death_date2, "%d %b %Y")

        if d_1 is None and d_2 is None:
            return True
        if d_1 is None and d_2 is not None:
            if d_2 > m:
                return True
        elif d_2 is None and d_1 is not None:
            if d_1 > m:
                return True
        else:
            if d_1 > m and d_2 > m:
                return True
            else:
                return False
                 
    except ValueError:
        print("marriage_before_death: DATE PROVIDED IS INCORRECT FORMAT")

# Checks if marriage date is before divorce date
def marriage_divorce_date_comparison(marriage_date, divorce_date):
    try:
        if marriage_date == "N/A" or divorce_date == "N/A":
            return False
        
        m = datetime.datetime.strptime(marriage_date, "%d %b %Y")
        d = datetime.datetime.strptime(divorce_date, "%d %b %Y")

        if m >= d:
            return False
        else:
            return True

    except ValueError:
        print("marriage_divorce_date_comparison: DATE PROVIDED IS INCORRECT FORMAT")

# Function to check if divorce date occurred before each spouse's death
def divorce_date_before_death(divorce, death_1, death_2):
    try:
        if divorce == "N/A":
            return False
        elif death_1 == "N/A" and death_2 == "N/A":
            return True
        
        res = True

        div = datetime.datetime.strptime(divorce, "%d %b %Y")
        if death_1 != "N/A":
            d_1 = datetime.datetime.strptime(death_1, "%d %b %Y")
            res = res and (div < d_1)
        if death_2 != "N/A":
            d_2 = datetime.datetime.strptime(death_2, "%d %b %Y")
            res = res and (div < d_2)

        return res
    except ValueError:
        print("divorce_date_before_death: DATE PROVIDED IS INCORRECT FORMAT")
# Checks if marriage is at least 14 years of both birth dates
def older_than_14(birth_date_1, birth_date_2, marriage_date):
    try:
        bd_1 = datetime.datetime.strptime(birth_date_1, "%d %b %Y")
        bd_2 = datetime.datetime.strptime(birth_date_2, "%d %b %Y")
        md = datetime.datetime.strptime(marriage_date, "%d %b %Y")
        return (int((md - bd_1).days/365) >= 14 and int((md - bd_2).days/365) >= 14)
    except ValueError:
        print("older_than_14: DATE PROVIDED IS INCORRECT FORMAT")
        
import constants
# US34 - List large age differences 
#List all couples who were married when the older spouse was more than twice as old as the younger spouse
def us34ListLargeAge(families):
    try:
        husbandID = families[3][constants.ffnIndex["HUSB"]] 
        wifeID = families[3][constants.ffnIndex["WIFE"]] 
        husbandAge = families[0][constants.ifnIndex["AGE"]] 
        husbandName = families[0][constants.ifnIndex["NAME"]] 
        wifeAge = families[1][constants.ifnIndex["AGE"]] 
        wifeName = families[1][constants.ifnIndex["NAME"]] 
        familyID = families[3][0] 
        
        finalOutput = "US34: ANOMALY: Large age difference on family {0}! ".format(familyID)
        if(husbandAge > wifeAge * 2):
            finalOutput += "{0} {1} is more than twice as old as spouse {2} {3}.".format(husbandID, husbandName, wifeID, wifeName)
            print(finalOutput)
        elif(wifeAge > husbandAge * 2):
            finalOutput += "{0} {1} is more than twice as old as spouse {2} {3}.".format(wifeID, wifeName, husbandID, husbandName)
            print(finalOutput)
        else:
            pass
    
    except Exception:
        pass
    