def us22UniqueIds(individuals, families):
    #do individuals
    seen = set()
    uniq = []
    dup = []
    for i in individuals:
        if i[0] not in seen:
            uniq.append(i)
            seen.add(i[0])
        else:
            dup.append(i)
    
    if(dup):
        dupIndiId = dup[0][0]
        
        for i in individuals:
            if(dupIndiId == i[0]):
                print("US22: ERROR: DUPID: " + i[1] + " has a duplicate individual ID of " + i[0] + "." )
    
    # do family ids
    uniq.clear()
    seen.clear()
    dup.clear()
    
    for f in families:
        if f[0] not in seen:
            uniq.append(f)
            seen.add(f[0])
        else:
            dup.append(f)
            
    if(dup):
        dupFamID = dup[0][0]
        
        for f in families:
            if(dupFamID == f[0]):
                print("US22: ERROR: DUPID: Family ID " + f[0] + "." )
    
    