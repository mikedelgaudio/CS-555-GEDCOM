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