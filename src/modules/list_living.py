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

def us31(individuals,families):
    divorced = False
    for i in individuals:
        #individual has no spouse, is above 30, and is alive
        if(i[4] != "Invalid Date"):
            if(i[8] == "N/A" and int(i[4]) > 30 and i[5] == "TRUE"):
                for f in families:
                    #check to ensure that the ind is not just divorced, 
                    # if so break and check the next ind
                    if(i[1] == f[4] or i[1] == f[6]):
                        if(f[2] != "N/A"):
                            divorced = True
                            break;
                # for f in families:
                #     #
                #     for child in f[7]:
                #         if(child == i[0]):
                if(not divorced):
                    print("US31: ALIVE & SINGLE: " + i[1] + " is over 30 and has never been married.")