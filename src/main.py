# Shannon Hobby, Paul Gurman, Michael DelGaudio, Brandon Seidman
# https://github.com/mikedelgaudio/CS-555-GEDCOM
# I pledge my honor that I have abided by the Stevens Honor System

import sqlite3 
from Table import Table
from helpers import ind as Ind, dates, fam, sorting, database as db
import constants
from modules import list_upcoming_dates, marriage_date_check, birth_date_check, list_deceased, unique_id, list_recent, list_living, multiple_births


# Wrapped this in a run() function so that our pytest knows what to do


def run():
    f = open("../test.ged", "r")
    conn = sqlite3.connect("../familytable.db")
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
                        family[constants.ffnIndex[nameTag]] = Ind.findIndividual(
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
                            individual[constants.ifnIndex["AGE"]] = Ind.ageCalculator(individual[constants.ifnIndex["BIRT"]], individual[constants.ifnIndex["DEAT"]])
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

    individual[constants.ifnIndex["AGE"]] = Ind.ageCalculator(individual[constants.ifnIndex["BIRT"]], individual[constants.ifnIndex["DEAT"]])
                            
    individuals += [individual]
    families += [family]

    individuals = sorting.sortById(individuals)
    families = sorting.sortById(families)

    individuals = Ind.fam_info_to_individual(individuals, families)

    # Adds Both Lists to pretty table to be dispalyed
    for x in individuals:
        constants.indTable.Add_Row(x)

    for x in families:
        constants.famTable.Add_Row(x)



    if conn is not None:
        cur = conn.cursor()
        cur.execute(db.create_ind_table())
        cur.execute(db.create_fam_table())
        for i in individuals:
            db.populate_ind(i, cur, conn)
        for f in families:
            db.populate_fam(f,cur, conn)
  
    #############################################
    #                PRINT HERE                 #
    #############################################
    print("Individuals")
    print(constants.indTable)
    print("Families")
    print(constants.famTable)

    # Create spouses list, the structure of each element in the list is: [Husband Object, Wife Object, Family Object]
    spouses = fam.families_to_spouses_list(families, individuals)

    # Creates list of parents with children
    extfamily = fam.families_to_child_parent_list(families,individuals)

    # US02: Chck if birthday is before date of marriage
    for s in filter(lambda s: s[2][constants.ffnIndex["MARR"]] != "N/A", spouses):
        if not birth_date_check.birth_before_marriage(s[0][constants.ifnIndex["BIRT"]], s[1][constants.ifnIndex["BIRT"]], s[2][1]):
            print("US02: ANOMALY: Marraige cannot be before either spouse's birth date. Marriage ID: {0}".format(s[2][0]))

    # US03: Check if death is before birth
    for s in individuals:
        if not birth_date_check.birth_before_death(s[constants.ifnIndex["BIRT"]],s[constants.ifnIndex["DEAT"]]):
            print("US03: ANOMALY: Death cannot come before birth. Individual ID: {0}".format(s[0]))
            
    # US04: For each divorced couple, make sure they are divorced AFTER they are married
    for s in filter(lambda couple: couple[2][constants.ffnIndex["DIV"]] != "N/A", spouses):
        if not marriage_date_check.marriage_divorce_date_comparison(s[2][constants.ffnIndex["MARR"]], s[2][constants.ffnIndex["DIV"]]):
            print("US04: ANOMALY: Divorce must come after a marriage. Marriage ID: {0}".format(s[2][0]))

    # US08: Children should be born after marriage of parents (and not more than 9 months after their divorce)
    for s in extfamily:
        if not birth_date_check.birth_before_marriage_of_parents(s[2][constants.ifnIndex["BIRT"]],s[3][constants.ffnIndex["MARR"]],s[3][constants.ffnIndex["DIV"]]):
            print("US08: ANOMALY: Children should be born after parents marriage. Individual ID: {0}".format(s[2][0]))

    # US09: Child should be born before death of mother and before 9 months after death of father
    for s in extfamily:
        if not birth_date_check.birth_before_death_of_parents(s[2][constants.ifnIndex["BIRT"]],s[1][constants.ifnIndex["DEAT"]],s[0][constants.ifnIndex["DEAT"]]):
            print("US09: ANOMALY: Children should be born before parents death. Individual ID: {0}".format(s[2][0]))

    # For each spouse, make sure their death dates are before their marriage dates. If not, print anamoly message.
    for s in filter(lambda s: s[2][constants.ffnIndex["MARR"]] != "N/A", spouses):
        if not marriage_date_check.marriage_before_death(s[0][constants.ifnIndex["DEAT"]], s[1][constants.ifnIndex["DEAT"]], s[2][1]):
            print("US05: ANOMALY: Marriage date cannot be after either spouse's death date. Marriage ID: {0}".format(s[2][0]))

    # For each divorced couple, make sure they are divorced AFTER they are married
    for s in filter(lambda s: s[2][constants.ffnIndex["DIV"]] != "N/A", spouses):
        if not marriage_date_check.marriage_divorce_date_comparison(s[2][constants.ffnIndex["MARR"]], s[2][constants.ffnIndex["DIV"]]):
            print("US04: ANOMALY: Divorce must come after a marriage. Marriage ID: {0}".format(s[2][0]))

    # US05: For each spouse, make sure their death dates are before their marriage dates. If not, print anamoly message.
    for s in filter(lambda couple: couple[2][constants.ffnIndex["MARR"]] != "N/A", spouses):
        if not marriage_date_check.marriage_before_death(s[0][constants.ifnIndex["DEAT"]], s[1][constants.ifnIndex["DEAT"]], s[2][1]):
            print("US05: ANOMALY: Marriage date cannot be after either spouse's death date. Marriage ID: {0}".format(s[2][0]))

    # US06: For each divorced couple, make sure they are divorced BEFORE they have died
    for s in filter(lambda couple: couple[2][constants.ffnIndex["DIV"]] != "N/A", spouses):
        if not marriage_date_check.divorce_date_before_death(s[2][constants.ffnIndex["DIV"]],
        s[0][constants.ifnIndex["DEAT"]], s[1][constants.ifnIndex["DEAT"]]):
            print("US06: ANAMOLY: Divorce date cannot be before either or both spouse's death date. Marriage ID: {0}".format(s[2][0]))
          
    # US10: For each couple, make sure  marriage is at least 14 years for both spouses
    for s in spouses:
        if not marriage_date_check.older_than_14(s[0][constants.ifnIndex["BIRT"]], s[1][constants.ifnIndex["BIRT"]], s[2][1]):
            print("US10: ANAMOLY: Marriage date should be at least 14 years after both spouse's births. Marriage ID: {0}".format(s[2][0]))
    
    # US11: No bigamy allowed, make sure for each married individual they have all but one marriage they're in that has divorce dates
    for i in list(filter(lambda ind: ind[8] != "N/A", individuals)):
        if not fam.bigomy_checker(list(filter(lambda f: f[3] == i[0] or f[5] == i[0], families))):
            print("US11: ANAMOLY: Bigomy is not allowed. Individual ID: {0}".format(i[0]))

    # US07: For each individual, make sure they are less than 150 years old
    for ind in individuals:
        if not birth_date_check.less_than_150_years(ind[constants.ifnIndex["BIRT"]], ind[constants.ifnIndex["DEAT"]]):
            print("US07: ANOMALY: Individual must be less than 150 years old. Individual ID: {0}".format(ind[0]))

    #runs us01 and us42 on individuals and familes
    dates.dateHelper(individuals, families)

    list_deceased.us29ListDeceased(individuals)
    unique_id.us22UniqueIds(individuals, families)

    list_upcoming_dates.birthdays(individuals)
    list_upcoming_dates.anniversary(individuals, families)
    list_recent.list_recent(individuals)
    
    # US30: List living married
    list_living.us30(individuals, families)
    # US31: List Living Single
    list_living.us31(individuals,families)
    
    # US28: Order siblings by age
    sorting.us28(individuals, families)

    multiple_births.us32_us14(individuals,families)
    

    # clear db at the end! 
    sql = 'DELETE FROM individuals'
    cur.execute(sql)
    conn.commit()
       
    sql = 'DELETE FROM families'
    cur.execute(sql)
    conn.commit()

# Uncomment me for debugging!!\
run()
