# Shannon Hobby, Paul Gurman, Michael DelGaudio, Brandon Seidman
# https://github.com/mikedelgaudio/CS-555-GEDCOM
# I pledge my honor that I have abided by the Stevens Honor System

from prettytable import PrettyTable
import datetime


months = {"JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
          "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12}


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


levels = {"0": ["HEAD", "TRLR", "NOTE"], "1": ["NAME", "SEX", "BIRT", "DEAT",
                                               "FAMC", "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"], "2": ["DATE"], "SPEC": ["INDI", "FAM"]}
# individual field name index
ifnIndex = {"ID": 0, "NAME": 1, "SEX": 2, "BIRT": 3, "AGE": 4,
            "ALIVE": 5, "DEAT": 6, "CHIL": 7, "MARR": 8, "HUSB": 8, "WIFE": 8, "DATES": ["BIRT", "MARR", "DEAT"]}
# family field name index
ffnindex = {"ID": 0, "MARR": 1, "DIV": 2, "HUSBID": 3, "HUSBNAME": 4, "WIFEID": 5,
            "WIFENAME": 6,  "CHIL": 7}
valid = "N"

individual = ["N/A", "N/A", "N/A", "N/A",
              "N/A", "TRUE", "N/A", "N/A", "N/A"]

indTable = PrettyTable()
famTable = PrettyTable()

indTable.field_names = ["ID", "Name", "Gender",
                        'Birthday', "Age", "Alive", "Death", "Child", "Spouse"]

famTable.field_names = ["ID", "Married", "Divorced", "Husband ID",
                        "Husband Name", "Wife ID", "Wife Name", "Children"]


f = open("Project01- Targaryon Family.ged", "r")

first = False
date = False
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
    elif tag == "DATE" and date == True:
        individual[ifnIndex[dateType]] = arg
        date = False
    elif tag in levels[level]:
        valid = "Y"
        if tag in ifnIndex:
            if tag in ifnIndex["DATES"]:
                if tag == "DEAT" and arg != "N":
                    individual[ifnIndex["ALIVE"]] = "FALSE"
                dateType = tag
                date = True
            else:
                individual[ifnIndex[tag]] = arg
                first = True
   elif tag == "TRLR":
        indTable.add_row(individual)
    else:
        if tag not in levels[level]:
            if arg in levels["SPEC"]:
                if arg == "INDI":
                    if first:
                        individual[ifnIndex["AGE"]] = ageCalculator(
                            individual[ifnIndex["BIRT"]], individual[ifnIndex["DEAT"]])
                        indTable.add_row(individual)
                    individual[0] = tag
                output[1] = arg
                output[2] = tag
                valid = "Y"
            else:
                valid = "N"

print(indTable)
print(famTable)
