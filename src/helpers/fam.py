# All helper functions related to familys

# Helper function that runs through each family, and for each one finds corresponding husband and wife individual. Returns list of the
# individuals with their corresponding family object.
def families_to_spouses_list(families, individuals):
    spouses = []
    for f in families:
        h = None
        w = None
        husband_id = f[3]
        wife_id = f[5]
        for i in individuals:
            if h == None and i[0] == husband_id:
                h = i
            elif w == None and i[0] == wife_id:
                w = i
            if h and w:
                break
        if h == None or w == None:
            continue
        spouses += [[h, w, f]]
    return spouses


def families_to_child_parent_list(families, individuals):
    extfamily = []
    for f in families:
        h = None
        w = None
        husband_id = f[3]
        wife_id = f[5]
        child_id_list = f[7].split()
        for i in individuals:
            if h == None and i[0] == husband_id:
                h = i
            elif w == None and i[0] == wife_id:
                w = i
            if h and w:
                break
        for c in child_id_list:
            for i in individuals:
                if i[0] == c or '{' + i[0] == c or i[0] + '}' == c:
                    extfamily += [[h, w, i, f]]
    
    return extfamily

# Checks for bigomy, returns true if no bigomy found


def bigomy_checker(list_of_marriages):
    #print(list_of_marriages)
    current_marriages = 0
    for m in list_of_marriages:
        if m[2] == "N/A":
            current_marriages += 1
        if current_marriages > 1:
            return False
    return True

import constants

# US17 - Parents should not marry any of their children
def us17NoMarrriage2Child(familes):
    try:
        children = familes[3][constants.ffnIndex["CHIL"]]
        dad = familes[3][constants.ffnIndex["HUSB"]]
        mom = familes[3][constants.ffnIndex["WIFE"]]
        
        #remove { } and seperate the children in a list
        sepListOfChildren = (children.replace("{", "").replace("}","").split())
        
        for child in sepListOfChildren:
            if(child == dad or child == mom):
                #The child was also the mom or dad
                return False
            
        return True
    except Exception:
        pass
    
