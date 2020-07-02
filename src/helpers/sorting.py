# All helpers used for sorting, whether it be dates individuals families etc

import re
# Resource cited:https://intellipaat.com/community/33368/does-python-have-a-built-in-function-for-string-natural-sort
# This is known as natural sorting, almost like char sorts we did in 392


def sortById(gedcomList):
    def convert(text): return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    # returns a copy of the sorted list by index 0 which is the unique ID field
    return sorted(gedcomList, key=lambda x: alphanum_key(x[0]))


def us28(individuals, families):
    lister = []
    ageList = []
    finalSortedList = []
    finalNames = []
    for f in families:
        item = (f[7].replace("{", "").replace("}","").split())
        if(item == []):
            #if no children iterate over it
            continue
        
        lister.clear()
        finalSortedList.clear()
        for ID in item:
            for person in individuals:
                if(person[0] == ID):
                    lister.append(person)
                    
        ageList.clear()
        for child in lister:
            if(child[4] == "Invalid Date"):
                continue
            ageList.append(child[4])
        

        ageList.sort()
        ageList.reverse()
        
        for age in ageList:
            for child in lister:
                if(child[4] == age):
                    finalSortedList.append(child)

                    
        #we now need to print all the children
        stringOfChildren = ""
        for child in finalSortedList:
            stringOfChildren += "AGE " + str(child[4]) + "--> " + child[0] + " " + child[1] + "; "
        if(len(finalSortedList) == 0):
            #if no children just iterate
            continue
        else:
            print("US28: CHILDREN SORTED: Family ID " + f[0] + " has " + str(len(finalSortedList)) + " children sorted " + stringOfChildren)
                
 
            
            
        
        
                
            