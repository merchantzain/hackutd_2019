import sqlite3

# create table if not exists
def create_table():
    # create database and connection if it doesnt exist
    conn = sqlite3.connect("data.db")

    # create table
    sql_query = """CREATE TABLE if not exists "travelers" (
                    "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    "name"	TEXT NOT NULL,
                    "email"	TEXT NOT NULL,
                    "phone"	TEXT NOT NULL,
                    "university"	TEXT NOT NULL DEFAULT 'UT Dallas',
                    "budget"	TEXT NOT NULL,
                    "weekend"	TEXT NOT NULL,
                    "interests"	TEXT NOT NULL DEFAULT ""
                );"""
    cursorObj = conn.cursor()
    cursorObj.execute(sql_query)
    conn.commit()
    conn.close()

# insert a traveller into the table
def insert_traveler(name, email, phone, university, budget, weekend, interests):
    # create database and connection if it doesnt exist
    conn = sqlite3.connect("data.db")

    # insert traveller
    sql_query = f'INSERT INTO travelers (name, email, phone, university, budget, weekend, interests) VALUES("{name}", "{email}", "{phone}", "{university}", "{budget}", "{weekend}", "{interests}")'
    cursorObj = conn.cursor()
    cursorObj.execute(sql_query)
    conn.commit()
    conn.close()

# return a nested list of similar travellers
def get_similar_travellers(current_traveller):
    # get all travellers in db with same date as current traveller
    sql_query = f'SELECT * FROM travelers WHERE weekend = "{current_traveller[4]}";'
    conn = sqlite3.connect("data.db")
    cursorObj = conn.cursor()
    cursorObj.execute(sql_query)
    conn.commit()
    values = cursorObj.fetchall()
    conn.close()

    if len(values) < 4:
        return False, None, None, None

    # parse similar travellers and common interests into a nested list and string respectively
    buddies = []
    common_interests = ""
    for value in values[:4]:
        buddies.append(list(value))
        common_interests = common_interests + " " + buddies[-1][-1]
    common_interests = common_interests[1:]
    common_interests.replace(",", "")
    common_interests = list(set(common_interests.split(" ")))

    # get the smallest budget from the group members
    smallest_budget = 2000
    for buddy in buddies:
        if int(buddy[5]) < smallest_budget:
            smallest_budget = int(buddy[5])

    # return both
    return True, buddies, common_interests, smallest_budget

# drop the table like the mic
def drop_table():
    # create database and connection if it doesnt exist
    conn = sqlite3.connect("data.db")

    # create table
    sql_query = "DROP TABLE travelers;"
    cursorObj = conn.cursor()
    cursorObj.execute(sql_query)
    conn.commit()
    conn.close()

# get number of rows in table
def table_status():
    # get all travellers in db with same date as current traveller
    sql_query = f'SELECT * FROM travelers;'
    conn = sqlite3.connect("data.db")
    cursorObj = conn.cursor()
    cursorObj.execute(sql_query)
    conn.commit()
    values = cursorObj.fetchall()
    conn.close()

    num_rows = len(values)
    return num_rows

# given a traveller id, delete the traveller from the table
def delete_travellers(traveller_id):
    # create database and connection if it doesnt exist
    conn = sqlite3.connect("data.db")

    # insert traveller
    sql_query = f"DELETE FROM travelers WHERE id={traveller_id};"
    cursorObj = conn.cursor()
    cursorObj.execute(sql_query)
    conn.commit()
    conn.close()