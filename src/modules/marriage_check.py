#Aunts and uncles - make sure aunts and uncles do not marry their neices and nephews
# check whos married
# check if they have siblings
# if so check if those siblings have kids 
# if spouse is a member of siblings children than return anomaly 

def return_children(ind, cur):
    cur.execute("SELECT spouse FROM individuals WHERE id=?", (ind,))
    spouse = cur.fetchall()
    spouse = spouse[0][0].replace("'", "")
    cur.execute("SELECT children FROM families WHERE id=? AND children!=?", (spouse,"N/A",))
    children = cur.fetchall()
    if(children != [] and children != "N/A"):
        children = children[0][0].replace("{","").replace("}", "").split()
    return children

def return_spouse(ind, cur):
    cur.execute("SELECT sex FROM individuals WHERE id=?", (ind,))
    gender = cur.fetchall()
    gender = gender[0][0].replace("'", "")
    cur.execute("SELECT spouse FROM individuals WHERE id=?", (ind,))
    spouse = cur.fetchall()
    spouse = spouse[0][0].replace("'", "")
    if (gender == "F"):
        cur.execute("SELECT husbID FROM families WHERE id=?", (spouse,))
    else:
        cur.execute("SELECT wifeID FROM families WHERE id=?", (spouse,))
    spouse = cur.fetchall()
    if(spouse != []):
        spouse = spouse[0][0].replace("'", "")
    return spouse

def us20(individuals, family, cur):
    cur.execute("SELECT * FROM individuals WHERE spouse!=?", ("N/A",))
    married = cur.fetchall()
    for i in married:
        cur.execute("SELECT children FROM families WHERE id=? AND children!=?", (i[7],"N/A",))
        siblings=cur.fetchall()
        
        if(siblings != []):
            siblings = siblings[0][0].replace("{","").replace("}", "").split()
            for j in siblings:
                j = j.replace("'", "")
                nieces_neph = return_children(j, cur)
                if(nieces_neph == []):
                    continue
                for k in nieces_neph:
                    k=k.replace("'", "")
                    if (return_spouse(k,cur) == i[0]):
                        print(f"US20: ANOMALY: Family {i[8]} -> {i[0]} should NOT marry their niece/nephew {k}.")
