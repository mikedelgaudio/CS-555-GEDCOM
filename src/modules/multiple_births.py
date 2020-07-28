from collections import Counter
multBirths = {2: "twins!", 3:"triplets!", 4: "quadruplets!", 5: "quintuplets!" }

def us32_us14(individuals, families):

    for f in families:
        ages = []
        str = f[7].replace('{','')
        str = str.replace('}','')
        children = str.split()
        if (len(children) > 1):
            for child in children:
                # childId = child
                # cur.execute("SELECT age FROM individuals WHERE id=?", (childId,))
                # child = cur.fetchall()
                for ind in individuals:
                    if (child == ind[0]):
                        ages.append(ind[3])
            ages = Counter(ages)
            for age in ages:
                if ages[age] > 1 and ages[age] <= 5:
                    print(f"US32: Family {f[0]} has {multBirths[ages[age]]}")
                elif (ages[age]> 5):
                    print("US14: ANOMALY: No more than 5 siblings should be born at the same time.")

# There should be fewer than 15 siblings in a family
def fewer_than_15_siblings(sibling_list):
    i = 0
    for s in sibling_list:
        i = i+1
    if (i > 15):
        return False
    else:
        return True
