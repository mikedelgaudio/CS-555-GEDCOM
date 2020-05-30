# Shannon Hobby, Paul Gurman, Michael DelGaudio, Brandon Seidman
# https://github.com/mikedelgaudio/CS-555-GEDCOM
# I pledge my honor that I have abided by the Stevens Honor System

levels = {"0": ["HEAD", "TRLR", "NOTE"], "1": ["NAME", "SEX", "BIRT", "DEAT",
                                                              "FAMC", "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"], "2": ["DATE"], "SPEC": ["INDI", "FAM"]}


valid = "N"

individuals = []
families = []

f = open("Project01- Targaryon Family.ged", "r")
for x in f:
    txt = x.split()
    level = txt[0]
    tag = txt[1]
    arg = " ".join(txt[2:])
    output = [txt[0], txt[1], " ".join(txt[2:])]
    if int(level) > 2:
        valid = "N"
        pass
    elif tag in levels[level]:
        valid = "Y"
    else:
        if tag not in levels[level]:
            if arg in levels["SPEC"]:
                output[1] = arg
                output[2] = tag
                valid = "Y"
            else:
                valid = "N"
    print("--> " + x.strip('\n'))
    print("<-- " + output[0] + "|" + output[1] +
          "|" + valid + "|" + output[2])
