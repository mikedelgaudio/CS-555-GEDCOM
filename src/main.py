# Shannon Hobby, Paul Gurman, Michael DelGaudio, Brandon Seidman
# https://github.com/mikedelgaudio/CS-555-GEDCOM
# I pledge my honor that I have abided by the Stevens Honor System

from prettytable import PrettyTable
import datetime

months = {"JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
          "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12}


# Finds an individual from list l using passed in id. Returns the name of that individual
# does NOT work for family list
def findIndividual(id, l):
    for x in l:
        if id in x:
            return x[1]

    return "N/A"


# calculates age either using todays date or death date if applicable
def ageCalculator(birthday, deathDate):
    if birthday != "N/A":
        day = birthday.split()[0]
        month = birthday.split()[1]
        year = birthday.split()[2]
    else:
        return "N/A"
    if deathDate != "N/A":
        deathday = deathDate.split()[0]
        deathmonth = deathDate.split()[1]
        deathyear = deathDate.split()[2]

    if deathDate == "N/A":
        today = datetime.datetime.now()
        birth = datetime.datetime(int(year), months[month], int(day))
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

    else:
        death = datetime.datetime(
            int(deathyear), months[deathmonth], int(deathday))
        birth = datetime.datetime(int(year), months[month], int(day))

        return death.year - birth.year - ((death.month, death.day) < (birth.month, birth.day))


# Leaving these as globals for now - to be cleaned.

levels = {"0": ["HEAD", "TRLR", "NOTE"], "1": ["NAME", "SEX", "BIRT", "DEAT",
                                               "FAMC", "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"], "2": ["DATE"], "SPEC": ["INDI", "FAM"]}
# individual field name index
ifnIndex = {"ID": 0, "NAME": 1, "SEX": 2, "BIRT": 3, "AGE": 4,
            "ALIVE": 5, "DEAT": 6, "CHILDREN": 7, "SPOUCE": [{"MARR": 8, "HUSB": 8, "WIFE": 8}], "DATES": ["BIRT", "MARR", "DEAT"]}
# family field name index
ffnIndex = {"ID": 0, "MARR": 1, "DIV": 2, "HUSB": 3, "HUSBNAME": 4, "WIFE": 5,
            "WIFENAME": 6,  "CHIL": 7, "DATES": ["MARR", "DIV"], "PPL": ["WIFE", "HUSB", "CHIL"]}
valid = "N"


indTable = PrettyTable()
famTable = PrettyTable()

indTable.field_names = ["ID", "Name", "Gender",
                        'Birthday', "Age", "Alive", "Death", "Child", "Spouse"]

famTable.field_names = ["ID", "Married", "Divorced", "Husband ID",
                        "Husband Name", "Wife ID", "Wife Name", "Children"]

# Wrapped this in a run() function so that our pytest knows what to do


def run():
    f = open("gameOfThrones.ged", "r")
    individuals = []
    families = []
    individual = ["N/A", "N/A", "N/A", "N/A",
                  "N/A", "TRUE", "N/A", "N/A", "N/A"]
    children = [[]]
    firstf = False
    first = False
    date = False
    datef = False
    family = ["N/A", "N/A", "N/A", "N/A",
              "N/A", "N/A", "N/A", ["N/A"]]
    dateType = ''
    for x in f:
        txt = x.split()
        level = txt[0]
        tag = txt[1]
        arg = " ".join(txt[2:])
        output = [txt[0], txt[1], " ".join(txt[2:])]
        if int(level) > 2:
            valid = "N"
            pass
        elif tag == "DATE" and datef == True:
            # if datef is true we know it's a family date like marr or div
            family[ffnIndex[dateType]] = arg
            datef = False
        elif tag == "DATE" and date == True:
            individual[ifnIndex[dateType]] = arg
            date = False
        elif tag in levels[level]:
            valid = "Y"
            # if the tag falls under the individual fields names
            if tag in ifnIndex and not firstf:
                if tag in ifnIndex["DATES"]:
                    if tag == "DEAT" and arg != "N":
                        individual[ifnIndex["ALIVE"]] = "FALSE"
                    dateType = tag
                    date = True
                else:
                    individual[ifnIndex[tag]] = arg
                    first = True
            # if that tag falls under the family field names
            elif tag in ffnIndex:
                if tag in ffnIndex["DATES"]:
                    # If the tag is MAR or DIV we should save which tag and flag datef as true
                    dateType = tag
                    datef = True
                    firstf = True
                else:
                    if tag == "CHIL":
                        # if tag is CHIL add the argument to the children array
                        children += arg + " "
                        firstf = True
                    else:
                        # anything else under fam is going to be husb or wife
                        # First set Husband Id or Wife ID to the argument
                        # Then find the full name of the individual using findIndividual
                        nameTag = tag + "NAME"
                        family[ffnIndex[tag]] = arg
                        family[ffnIndex[nameTag]] = findIndividual(
                            arg, individuals)

                        firstf = True

        elif tag == "TRLR":
            # If we've reach the end of the file we should add the last individual
            # Still doesn't seem to work as the last individual bug is still present
            if not firstf:
                individuals += [individual]
                individual = ["N/A", "N/A", "N/A", "N/A",
                              "N/A", "TRUE", "N/A", "N/A", "N/A"]

            else:
                family[ffnIndex["CHIL"]] = '{' + \
                    ''.join(children).strip() + '}'
                families += [family]
                family = ["N/A", "N/A", "N/A", "N/A",
                          "N/A", "N/A", "N/A", ["N/A"]]
        else:
            # If tag is either invalid or is a special case like INDI or FAM
            if tag not in levels[level]:
                if arg in levels["SPEC"]:
                    # Stores the individual's list into individuals array
                    # Resets individual to default values
                    if arg == "INDI":
                        if first:
                            individual[ifnIndex["AGE"]] = ageCalculator(
                                individual[ifnIndex["BIRT"]], individual[ifnIndex["DEAT"]])
                            individuals += [individual]
                            individual = ["N/A", "N/A", "N/A", "N/A",
                                          "N/A", "TRUE", "N/A", "N/A", "N/A"]
                        individual[0] = tag
                    # Stores family into families array
                    # resets family to default value
                    # transforms the children array into a string with the format {a b c d ...}
                    if arg == "FAM":
                        if firstf:
                            family[ffnIndex["CHIL"]
                                   ] = '{' + ''.join(children).strip() + '}'
                            families += [family]
                            family = ["N/A", "N/A", "N/A", "N/A",
                                      "N/A", "N/A", "N/A", ["N/A"]]
                        family[0] = tag
                        children = []

                    output[1] = arg
                    output[2] = tag
                    valid = "Y"
                else:
                    valid = "N"

    # This is for the spouse and child column of the Individual Table.
    # Checks to see if invididual's id appears in any of the family lists
    # if so -> have that family id populate either the child or spouse column
    count = 0
    for x in individuals:
        for i in families:
            if x[0] in i:
                x[8] = i[0]
            elif x[0] in i[7]:
                x[7] = i[0]
        count += 1

    # Adds Both Lists to pretty table to be dispalyed
    for x in individuals:
        indTable.add_row(x)

    for x in families:
        famTable.add_row(x)

    # TODO SORT: pretty table has a built in sort function but I think it's a little weird we may have to build our own
    # example: this code will print the ids as : i9 i8 i7 i6 i5 i4 i3 i2 i1 i17 i16 i15 i14 i13 etc
    # indTable.sortby = "ID"
    # indTable.reversesort = True

    print("Individuals")
    print(indTable)
    print("Families")
    print(famTable)


# Uncomment me for debugging!!
# run()
