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

    # get common interests between travellers

    # return both

    pass

# given a traveller id, delete the traveller from the table
def delete_travellers(traveller_id):
    pass