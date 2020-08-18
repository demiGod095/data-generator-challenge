# this script creates the sqlite database file
# it initializes the schema
# and populates the enum tables

# os required for deleting any previous file
import os
# sqlite required for creating file
import sqlite3
# arg parser for command line arguments
from argparse import ArgumentParser

# get the constants and definitions
import configuration as conf
import sqlHelpers as SQL


# create enum type table, all have similar structure
def create_enum_table_with_values(db, name, valList):
    # get the respective sql strings and
    createSql = SQL.create_enum_table.format(name=name)
    insertSql = SQL.insert_enum_table.format(name=name)

    try:
        crs = db.cursor()

        # create table
        crs.execute(createSql)

        # insert all values
        crs.executemany(insertSql, enumerate(valList))

        # commit insert operations
        db.commit()
    except sqlite3.Error as e:
        print(e)


# create a relational tables
def create_relational_table(db, props):
    # name substituted with name,
    # props substituted with comma separated props list
    createSql = SQL.create_rel_table.format(
        table_name=props['name'],
        table_props=', '.join(props['props'])
    )

    try:
        crs = db.cursor()

        # run the query, no need to commit as nothing is inserted
        crs.execute(createSql)
    except sqlite3.Error as e:
        print(e)


# deletes the existing dbFile
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

    db = SQL.create_connection(outFileName)

    if db is None:
        print(f'Problem creating DB.')
        return

    # create the specific enum tables
    create_enum_table_with_values(db, 'status', conf.STATUS_LIST)
    create_enum_table_with_values(db, 'category', conf.CATEGORY_LIST)
    create_enum_table_with_values(db, 'group', conf.GROUP_LIST)
    create_enum_table_with_values(db, 'product', conf.PRODUCT_LIST)
    create_enum_table_with_values(db, 'issue', conf.ISSUE_LIST)

    # create the relational tables
    create_relational_table(db, SQL.user_table_props)
    create_relational_table(db, SQL.agent_table_props)
    create_relational_table(db, SQL.ticket_table_props)
    create_relational_table(db, SQL.activity_table_props)

    print(f'sqlite database generated - {outFileName}')


if __name__ == '__main__':
    main()
