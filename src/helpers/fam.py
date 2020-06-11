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
            print("continued")
            continue
        spouses += [[h, w, f]]
    return spouses