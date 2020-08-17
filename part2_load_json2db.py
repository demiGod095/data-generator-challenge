import json
import sqlite3
from argparse import ArgumentParser
from datetime import datetime

from faker import Faker

import configuration as conf
import sqlHelpers as SQL


def extractCount(firstLine):
    findStr1 = '_count":'
    findStr2 = '}'

    pos1 = firstLine.find(findStr1)
    pos1 += len(findStr1)

    pos2 = firstLine.find(findStr2, pos1)

    return int(firstLine[pos1:pos2])


def genInsertSql(props):
    sqlStr = SQL.insert_rel_table.format(
        table_name=props['name'],
        insert_props=', '.join(props['insert']),
        param_styles=', '.join(['?' for _ in props['insert']])
    )

    return sqlStr


def genEmailFromName(name):
    email = name.lower()
    email = email.replace(' ', fake.random_choices(elements=('_', '.', ''), length=1)[0])
    email = f'{email}@{fake.domain_name()}'

    return email


def insertUser(db, user_id):
    insertSql = genInsertSql(SQL.user_table_props)

    name = fake.name()
    email = genEmailFromName(name)

    insertTuple = (user_id, name, email)

    db.execute(insertSql, insertTuple)
    db.commit()


def insertAgent(db, agent_id):
    insertSql = genInsertSql(SQL.agent_table_props)

    name = fake.name()
    tfn = fake.bothify(text='###-###-###')

    insertTuple = (agent_id, name, tfn)

    db.execute(insertSql, insertTuple)
    db.commit()


def insertTicket(db, instance):
    insertSql = genInsertSql(SQL.ticket_table_props)

    activity = instance['activity']

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

    db.execute(insertSql, insertTuple)
    db.commit()


def insertActivity(db, activity_id, instance):
    insertSql = genInsertSql(SQL.activity_table_props)

    activity = instance['activity']

    date_string = instance['performed_at']

    dt = datetime.strptime(date_string, conf.PERFORMED_DATE_FORMAT)

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

    db.execute(insertSql, insertTuple)
    db.commit()


def convert(inFileName, db):
    with open(inFileName, 'r') as inFile:
        firstLine = inFile.readline()
        count = extractCount(firstLine)

        userIdSet = set()
        agentIdSet = set()
        ticketIdSet = set()

        for ctr in range(count):
            line = inFile.readline()

            instance = json.loads(line[:-2])
            activity = instance['activity']

            if instance['performer_id'] not in userIdSet:
                insertUser(db, instance['performer_id'])
                userIdSet.add(instance['performer_id'])

            if activity['agent_id'] not in agentIdSet:
                insertAgent(db, activity['agent_id'])
                agentIdSet.add(activity['agent_id'])

            if instance['ticket_id'] not in ticketIdSet:
                insertTicket(db, instance)
                ticketIdSet.add(instance['ticket_id'])

            insertActivity(db, ctr, instance)


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
        print(f'DB error occurred, Did you run create script?')


if __name__ == '__main__':
    fake = Faker(conf.FAKER_LOCALE)
    main()
