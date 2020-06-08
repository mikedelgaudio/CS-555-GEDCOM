# Shannon Hobby, Paul Gurman, Michael DelGaudio, Brandon Seidman
# https://github.com/mikedelgaudio/CS-555-GEDCOM
# I pledge my honor that I have abided by the Stevens Honor System

from Table import Table
from helpers import ind, dates, fam, sorting
import constants

# Wrapped this in a run() function so that our pytest knows what to do


def run():
    f = open("./gameOfThrones.ged", "r")
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
            family[constants.ffnIndex[dateType]] = arg
            datef = False
        elif tag == "DATE" and date == True:
            individual[constants.ifnIndex[dateType]] = arg
            date = False
        elif tag in constants.levels[level]:
            valid = "Y"
            # if the tag falls under the individual fields names
            if tag in constants.ifnIndex and not firstf:
                if tag in constants.ifnIndex["DATES"]:
                    if tag == "DEAT" and arg != "N":
                        individual[constants.ifnIndex["ALIVE"]] = "FALSE"
                    dateType = tag
                    date = True
                else:
                    individual[constants.ifnIndex[tag]] = arg
                    first = True
            # if that tag falls under the family field names
            elif tag in constants.ffnIndex:
                if tag in constants.ffnIndex["DATES"]:
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
                        family[constants.ffnIndex[tag]] = arg
                        family[constants.ffnIndex[nameTag]] = ind.findIndividual(
                            arg, individuals)

                        firstf = True

        elif tag == "TRLR":
            # If we've reach the end of the file we should add the last individual
            # Still doesn't seem to work as the last individual bug is still present
            if not firstf:
                individuals += [individual]

            else:
                family[constants.ffnIndex["CHIL"]] = '{' + \
                    ''.join(children).strip() + '}'
                families += [family]

        else:
            # If tag is either invalid or is a special case like INDI or FAM
            if tag not in constants.levels[level]:
                if arg in constants.levels["SPEC"]:
                    # Stores the individual's list into individuals array
                    # Resets individual to default values
                    if arg == "INDI":
                        if first:

                            individual[constants.ifnIndex["AGE"]] = ind.ageCalculator(
                                individual[constants.ifnIndex["BIRT"]], individual[constants.ifnIndex["DEAT"]])
                            individuals += [individual]
                            individual = ["N/A", "N/A", "N/A", "N/A",
                                          "N/A", "TRUE", "N/A", "N/A", "N/A"]

                        individual[0] = tag
                    # Stores family into families array
                    # resets family to default value
                    # transforms the children array into a string with the format {a b c d ...}
                    if arg == "FAM":
                        if firstf:
                            family[constants.ffnIndex["CHIL"]
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
    family[constants.ffnIndex["CHIL"]] = '{' + \
        ''.join(children).strip() + '}'

    individuals += [individual]
    families += [family]

    individuals = sorting.sortById(individuals)
    families = sorting.sortById(families)

    individuals = ind.fam_info_to_individual(individuals, families)

    # Adds Both Lists to pretty table to be dispalyed
    for x in individuals:
        constants.indTable.Add_Row(x)

    for x in families:
        constants.famTable.Add_Row(x)

    #############################################
    #                PRINT HERE                 #
    #############################################
    print("Individuals")
    print(constants.indTable)
    print("Families")
    print(constants.famTable)


# Uncomment me for debugging!!
run()
