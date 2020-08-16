import os
import sqlite3
from argparse import ArgumentParser

# from configuration import START_DATE, END_DATE, START_WORK_HOURS, END_WORK_HOURS, CATEGORY_LIST
import configuration as conf


def create_enum_table(db, name, valList):
    createSql = f'CREATE TABLE enum_{name}(' \
                f'id INTEGER NOT NULL,' \
                f'{name}_type TEXT NOT NULL, ' \
                f'PRIMARY KEY (id));'

    insertSql = f'INSERT INTO enum_{name} VALUES(?,?);'

    # print(f'createSql: {createSql}')
    # print(f'isql: {insertSql}')

    try:
        crs = db.cursor()
        crs.execute(createSql)

        crs.executemany(insertSql, enumerate(valList))

        db.commit()
    except sqlite3.Error as e:
        print(e)


def create_relational_table(db, createSql):
    try:
        crs = db.cursor()
        crs.execute(createSql)
    except sqlite3.Error as e:
        print(e)


def create_connection(dbFileName):
    db = None
    try:
        db = sqlite3.connect(dbFileName)
    except sqlite3.Error as e:
        print(e)
    return db


def delete_db_if_exists(dbFileName):
    try:
        os.remove(dbFileName)
    except FileNotFoundError:
        # nothing to do if file doesn't exits
        pass


def main():
    argParser = ArgumentParser()
    argParser.add_argument('-o', type=str, default=conf.DEFAULT_SQLITE_FILE)

    parsed = argParser.parse_args()
    outFileName = parsed.o

    delete_db_if_exists(outFileName)

    db = create_connection(outFileName)

    if db is None:
        print(f'Problem creating DB.')
        return

    create_enum_table(db, "status", conf.STATUS_LIST)
    create_enum_table(db, "category", conf.CATEGORY_LIST)
    create_enum_table(db, "group", conf.GROUP_LIST)
    create_enum_table(db, "product", conf.PRODUCT_LIST)

    print(f'sqlite database generated - {outFileName}')


if __name__ == '__main__':
    main()
