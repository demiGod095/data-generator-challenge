# this script loads json to relational model
import json
import sqlite3
from argparse import ArgumentParser
from datetime import datetime

# faker required for generating user names etc.
from faker import Faker

# load the constants and configurations
import configuration as conf
import sqlHelpers as SQL


# function to check how many records are present by inspecting the first line
def extractCount(firstLine):

    # starting of string
    findStr1 = '_count":'
    findStr2 = '}'

    # get position1, then add length of str to get end pos
    pos1 = firstLine.find(findStr1)
    pos1 += len(findStr1)

    # find closing bracket from end position
    pos2 = firstLine.find(findStr2, pos1)

    # convert the string to integer
    return int(firstLine[pos1:pos2])


# get formatted sql for inserting into tables
def genInsertSql(props):
    # name: from prop name
    # insert props: from prop insert list
    # param styles: list of ? size of the insert props
    sqlStr = SQL.insert_rel_table.format(
        table_name=props['name'],
        insert_props=', '.join(props['insert']),
        param_styles=', '.join(['?' for _ in range(props['insert'])])
    )

    return sqlStr

# prepare and email address from a name
def genEmailFromName(name):
    email = name.lower()
    
    # spaces replaced by underscores, dots or just removed.
    email = email.replace(' ', fake.random_choices(elements=('_', '.', ''), length=1)[0])

    # concatinate with a random email domain
    email = f'{email}@{fake.domain_name()}'

    return email


# create new user and insert into db with provided id
def insertUser(db, user_id):
    insertSql = genInsertSql(SQL.user_table_props)

    # get random name and generate email
    name = fake.name()
    email = genEmailFromName(name)

    insertTuple = (user_id, name, email)

    # execute insert and comit
    db.execute(insertSql, insertTuple)
    db.commit()

# create new agent and insert into db with provided id
def insertAgent(db, agent_id):
    insertSql = genInsertSql(SQL.agent_table_props)

    # get random name and TFN
    name = fake.name()
    tfn = fake.bothify(text='###-###-###')

    insertTuple = (agent_id, name, tfn)

    # execute insert and comit
    db.execute(insertSql, insertTuple)
    db.commit()


# insert ticket according to provided instance
def insertTicket(db, instance):
    insertSql = genInsertSql(SQL.ticket_table_props)

    activity = instance['activity']

    # insert values
    insertTuple = (
        instance['ticket_id'],
        instance['performer_type'],
        instance['performer_id'],
        activity['shipping_address'],
        activity['shipment_date'],
        conf.CATEGORY_LIST.index(activity['category']),
        conf.ISSUE_LIST.index(activity['issue_type']),
        conf.GROUP_LIST.index(activity['group']),
        conf.PRODUCT_LIST.index(activity['product'])
    )

    # execute insert and comit
    db.execute(insertSql, insertTuple)
    db.commit()


def insertActivity(db, activity_id, instance):
    insertSql = genInsertSql(SQL.activity_table_props)

    activity = instance['activity']

    date_string = instance['performed_at']

    # convert string to datetime, later converted to Unix Timestamp
    dt = datetime.strptime(date_string, conf.PERFORMED_DATE_FORMAT)


    # insert values
    insertTuple = (
        activity_id,
        instance['ticket_id'],
        dt.timestamp(),
        activity['contacted_customer'],
        activity['source'],
        conf.STATUS_LIST.index(activity['status']),
        activity['priority'],
        activity['agent_id'],
        activity['requester']
    )

    # execute insert and comit
    db.execute(insertSql, insertTuple)
    db.commit()


# driver function for reading and writing
def convert(inFileName, db):
    with open(inFileName, 'r') as inFile:
        # read first line and get number of values
        firstLine = inFile.readline()
        count = extractCount(firstLine)

        # declare empty sets for tracking new IDs
        userIdSet = set()
        agentIdSet = set()
        ticketIdSet = set()


        for activity_id in range(count):
            # read one line and convert to string
            line = inFile.readline()

            instance = json.loads(line[:-2])
            activity = instance['activity']

            # check if user is new, insert to db
            if instance['performer_id'] not in userIdSet:
                insertUser(db, instance['performer_id'])
                userIdSet.add(instance['performer_id'])

            # check if agent is new, insert to db
            if activity['agent_id'] not in agentIdSet:
                insertAgent(db, activity['agent_id'])
                agentIdSet.add(activity['agent_id'])

            # check if ticket_id is new, insert to db
            if instance['ticket_id'] not in ticketIdSet:
                insertTicket(db, instance)
                ticketIdSet.add(instance['ticket_id'])

            # insert the activity to db, with loop counter as id
            insertActivity(db, activity_id, instance)


def main():
    argParser = ArgumentParser()
    argParser.add_argument('-i', type=str, default=conf.DEFAULT_JSON_FILE)
    argParser.add_argument('-o', type=str, default=conf.DEFAULT_SQLITE_FILE)

    parsed = argParser.parse_args()
    inFileName = parsed.i
    outFileName = parsed.o

    print(f"{inFileName} -> {outFileName}")

    db = SQL.create_connection(outFileName)

    if db is None:
        print(f'Error establishing connection with DB.')
        return

    try:
        convert(inFileName, db)
        print(f'Database conversion done!')

    except sqlite3.Error as e:
        print(e)
        print(f'DB error occurred, Did you run create script first?')


if __name__ == '__main__':
    fake = Faker(conf.FAKER_LOCALE)
    main()
