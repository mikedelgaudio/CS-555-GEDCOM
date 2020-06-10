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

