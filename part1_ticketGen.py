# script to generate tickets

# json for writing output to file
import json
# argument parser for command line args
from argparse import ArgumentParser
# datetime required for datetime calculations
from datetime import datetime, timedelta

# faker library for generation of random data
from faker import Faker
from faker.utils import datetime_safe

# settings and constants imported for use
import configuration as conf


# function that generates a list of random booleans
# format - False in the beginning, and true for the rest.
def genBoolList(size):
    # number of false values in the start
    # allow at least one true and at least one false
    numFalse = fake.random_int(min=1, max=size - 1)

    # list comprehension for bool with condition
    boolList = [False if e < numFalse else True for e in range(size)]

    return boolList


# function that generates tickets list given count as size
def genTickets(totalCount):
    # chose a random start point for ticket IDs
    startId = fake.random_int()

    # declare an empty list
    returnList = []

    # loop for count times
    for ticket_id in range(startId, startId + totalCount):
        # chose random date between configured dates
        ticketDateStart = fake.date_between_dates(conf.START_DATE, conf.END_DATE)

        # generate a random data, like IDs and addresses
        performer_id = fake.random_number(digits=conf.RAND_ID_DIGITS)
        shipping_address = fake.address()
        shipment_date = ticketDateStart.strftime(conf.SHIPMENT_DATE_FORMAT)
        category = fake.word(ext_word_list=conf.CATEGORY_LIST)
        issue_type = fake.word(ext_word_list=conf.ISSUE_LIST)
        source = fake.random_digit_not_null()
        priority = fake.random_digit_not_null()
        group = fake.word(ext_word_list=conf.GROUP_LIST)
        agent_id = fake.random_number(digits=conf.RAND_ID_DIGITS)
        product = fake.word(ext_word_list=conf.PRODUCT_LIST)

        # generate bool list of size equal to the size of the status_list
        boolList = genBoolList(len(conf.STATUS_LIST))

        # initialize progressive date as shipment date
        thisDate = ticketDateStart

        # loop to generate activities
        for status, contacted in zip(conf.STATUS_LIST, boolList):
            # status is from list,
            # contacted customer is from random generated booleans,

            # define activity
            activity = {
                'shipping_address': shipping_address,
                'shipment_date': shipment_date,
                'category': category,
                'contacted_customer': contacted,
                'issue_type': issue_type,
                'source': source,
                'status': status,
                'priority': priority,
                'group': group,
                'agent_id': agent_id,
                'requester': performer_id,
                'product': product
            }

            # move date forward in time, add 1 + random amount of days
            thisDate += timedelta(days=conf.MIN_TIMEDELTA_DAYS)
            thisDate += fake.time_delta(timedelta(days=conf.RAND_TIMEDELTA_DAYS))

            # performed at is a combination of date and time,
            # chose a time between working hours
            performed_at = fake.date_time_between_dates(
                datetime_start=datetime.combine(thisDate, conf.START_WORK_HOURS),
                datetime_end=datetime.combine(thisDate, conf.END_WORK_HOURS)
            ).astimezone()

            # create the instance according to the structure
            instance = {
                'performed_at': performed_at,
                'ticket_id': ticket_id,
                'performer_type': conf.PERFORMER_TYPE_STR,
                'performer_id': performer_id,
                'activity': activity
            }

            # add to the list
            returnList.append(instance)

    # sort the list according to occurrence
    returnList = sorted(returnList, key=lambda e: e['performed_at'])

    return returnList


# function to convert datetime object to string representation in json serialization
def encoder(obj):
    if type(obj) is datetime_safe.datetime:
        return obj.strftime(conf.PERFORMED_DATE_FORMAT)


def main():
    argParser = ArgumentParser()
    argParser.add_argument('-n', type=int, default=conf.DEFAULT_COUNT)
    argParser.add_argument('-o', type=str, default=conf.DEFAULT_JSON_FILE)

    parsed = argParser.parse_args()
    totalCount = parsed.n
    outFileName = parsed.o

    # get tickets list
    activities_data = genTickets(totalCount)

    print(f'Ticket Generation done.')

    # create the given meta object structure according
    metaObj = {
        'metadata':
            {
                'start_at': activities_data[0]['performed_at'],
                'end_at': activities_data[-1]['performed_at'],
                'activities_count': totalCount * len(conf.STATUS_LIST)
            },
        'activities_data': []
    }

    # write data to json file
    with open(outFileName, 'w') as outFile:
        metaString = json.dumps(metaObj, default=encoder)

        # activities list closing brackets are left out for filling in activities
        outFile.write(f'{metaString[:-2]}\n')

        # write each activity on one line, except the last one
        for activity in activities_data[:-1]:
            # activity ends in ',' as it is a part of a list
            outFile.write(f'{json.dumps(activity, default=encoder)},\n')

        # get the last activity
        activity = activities_data[-1]

        # write the activity
        outFile.write(f'{json.dumps(activity, default=encoder)}')

        # complete the object structure, first ] then }
        # blank new line at the end to satisfy pep8 convention
        outFile.write(f'{metaString[-2:-1]}\n{metaString[-1:]}\n')

    print(f'Data written to {outFileName}')


if __name__ == '__main__':
    # make faker instance with the configured local for global use
    fake = Faker(conf.FAKER_LOCALE)

    # run main
    main()
