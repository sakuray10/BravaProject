# python file to initialize sqlite database

import sqlite3


def init_db():
    connection = sqlite3.connect('database.db')

    # use this schema for the database
    with open('schema.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()

    connection.commit()
    connection.close()
