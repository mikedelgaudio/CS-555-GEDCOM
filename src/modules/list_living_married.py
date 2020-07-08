# List all living and alive married
def us30(individuals, familes):
    for f in familes:
        if(f[2] == "N/A"):
            # they are not divorced so
            #print("US30: NOT DIVORCED & MARRIED: Husband " + f[4] + " alive and married to wife " + f[6])
            for i in individuals:
                if ( (f[4] == i[1] and i[5] == "TRUE") ): #go into indi table to find husband is alive
                    for i in individuals:
                        if (f[6] == i[1] and i[5] == "TRUE"):   #go into indi table to find wife is alive
                            print("US30: ALIVE & MARRIED: "+ f[4] + " and " + f[6] + " are alive and married.")
