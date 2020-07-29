import sqlite3

def create_ind_table():
    indTable = """ CREATE TABLE IF NOT EXISTS individuals (
                        id text,
                        name text,
                        sex text,
                        birt text,
                        age text,
                        alive text,
                        deat text,
                        children text,
                        spouse text
                    ); """
    return indTable

def create_fam_table():
    famTable = """ CREATE TABLE IF NOT EXISTS families (
                        id text,
                        marr text,
                        div text,
                        husbID,
                        husbName,
                        wifeID,
                        wifeName,
                        children text
                    ); """
    return famTable

def populate_ind(individual, cur, conn):
        ind = (individual[0],individual[1],individual[2],individual[3],individual[4],individual[5], individual[6], individual[7], individual[8])
        sql = f''' INSERT INTO individuals(id,name,sex,birt,age,alive,deat,children,spouse)
            VALUES(?,?,?,?,?,?,?,?,?) '''
        cur.execute(sql, ind)
        conn.commit()

def populate_fam(family, cur, conn):
    fam = (family[0],family[1],family[2],family[3],family[4],family[5], family[6], family[7])
    sql = f''' INSERT INTO families(id,marr,div,husbID,husbName,wifeID,wifeName,children)
        VALUES(?,?,?,?,?,?,?,?) '''
    cur.execute(sql, fam)
    conn.commit()