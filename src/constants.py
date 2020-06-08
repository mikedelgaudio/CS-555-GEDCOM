
from Table import Table
levels = {"0": ["HEAD", "TRLR", "NOTE"], "1": ["NAME", "SEX", "BIRT", "DEAT",
                                               "FAMC", "FAMS", "MARR", "HUSB", "WIFE", "CHIL", "DIV"], "2": ["DATE"], "SPEC": ["INDI", "FAM"]}
# individual field name index
ifnIndex = {"ID": 0, "NAME": 1, "SEX": 2, "BIRT": 3, "AGE": 4,
            "ALIVE": 5, "DEAT": 6, "CHILDREN": 7, "SPOUCE": [{"MARR": 8, "HUSB": 8, "WIFE": 8}], "DATES": ["BIRT", "MARR", "DEAT"]}
# family field name index
ffnIndex = {"ID": 0, "MARR": 1, "DIV": 2, "HUSB": 3, "HUSBNAME": 4, "WIFE": 5,
            "WIFENAME": 6,  "CHIL": 7, "DATES": ["MARR", "DIV"], "PPL": ["WIFE", "HUSB", "CHIL"]}

indTable = Table()
famTable = Table()

indTable.Set_Field_Names(["ID", "Name", "Gender",
                          'Birthday', "Age", "Alive", "Death", "Child", "Spouse"])

famTable.Set_Field_Names(["ID", "Married", "Divorced", "Husband ID",
                          "Husband Name", "Wife ID", "Wife Name", "Children"])
