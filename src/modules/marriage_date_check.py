import datetime

# Compares two spouces death dates against their marriage date to ensure both are less than it
def marriage_before_death(death_date1, death_date2, marriage_date):
    try:
        m = datetime.datetime.strptime(marriage_date, "%d %b %Y")
        if datetime.datetime.strptime(death_date1, "%d %b %Y") > m and datetime.datetime.strptime(death_date2, "%d %b %Y") > m:
            return True
        else:
            return False
    except ValueError:
        print("DATE PROVIDED IS INCORRECT FORMAT")

