import os
import sqlite3
from argparse import ArgumentParser

# from configuration import START_DATE, END_DATE, START_WORK_HOURS, END_WORK_HOURS, CATEGORY_LIST
import configuration as conf
import sqlStrings as SQL


def create_enum_table_with_values(db, name, valList):
    createSql = SQL.create_enum_table.format(name=name)
    insertSql = SQL.insert_enum_table.format(name=name)

    # print(f'cSql: {createSql}')
    # print(f'iSql: {insertSql}')

    try:
        crs = db.cursor()
        crs.execute(createSql)

        crs.executemany(insertSql, enumerate(valList))

        db.commit()
    except sqlite3.Error as e:
        print(e)


def create_relational_table(db, props):
    createSql = SQL.create_rel_table.format(
        table_name=props['name'],
        table_props=', '.join(props['props'])
    )

    # print(f'cSql: {createSql}')

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

    create_enum_table_with_values(db, "status", conf.STATUS_LIST)
    create_enum_table_with_values(db, "category", conf.CATEGORY_LIST)
    create_enum_table_with_values(db, "group", conf.GROUP_LIST)
    create_enum_table_with_values(db, "product", conf.PRODUCT_LIST)
    create_enum_table_with_values(db, "issue", conf.ISSUE_LIST)

    create_relational_table(db, SQL.user_table_props)
    create_relational_table(db, SQL.agent_table_props)
    create_relational_table(db, SQL.ticket_table_props)
    create_relational_table(db, SQL.activity_table_props)

    print(f'sqlite database generated - {outFileName}')


if __name__ == '__main__':
    main()
