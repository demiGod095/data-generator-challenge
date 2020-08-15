import json
from argparse import ArgumentParser
from datetime import datetime, timedelta

from faker import Faker
from faker.utils import datetime_safe

# from configuration import START_DATE, END_DATE, START_WORK_HOURS, END_WORK_HOURS, CATEGORY_LIST
import configuration as conf


def genTickets(totalCount):
    startId = fake.random_int()

    returnList = []

    for ticket_id in range(startId, startId + totalCount):
        ticketDateStart = fake.date_between_dates(conf.START_DATE, conf.END_DATE)
        performer_id = fake.random_number(digits=conf.RAND_ID_DIGITS)

        shipping_address = fake.address()
        shipment_date = ticketDateStart.strftime(conf.SHIPMENT_DATE_FORMAT)
        category = fake.word(ext_word_list=conf.CATEGORY_LIST)

        source = fake.random_digit_not_null()
        priority = fake.random_digit_not_null()
        group = fake.word(ext_word_list=conf.GROUP_LIST)
        requester = fake.random_number(digits=conf.RAND_ID_DIGITS)
        product = fake.word(ext_word_list=conf.PRODUCT_LIST)

        thisDate = ticketDateStart

        for status in conf.STATUS_LIST:
            activity = {
                'shipping_address': shipping_address,
                'shipment_date': shipment_date,
                'category': category,
                'contacted_customer': conf.CONTACTED_CUSTOMER_BOOL,
                'issue_type': conf.ISSUE_TYPE_STR,
                'source': source,
                'status': status,
                'priority': priority,
                'group': group,
                'agent_id': performer_id,
                'requester': requester,
                'product': product
            }

            thisDate += timedelta(days=conf.MIN_TIMEDELTA_DAYS)
            thisDate += fake.time_delta(timedelta(days=conf.RAND_TIMEDELTA_DAYS))

            performed_at = fake.date_time_between_dates(
                datetime_start=datetime.combine(thisDate, conf.START_WORK_HOURS),
                datetime_end=datetime.combine(thisDate, conf.END_WORK_HOURS)
            ).astimezone()

            ticket = {
                'performed_at': performed_at,
                'ticket_id': ticket_id,
                'performer_type': conf.PERFORMER_TYPE_STR,
                'performer_id': performer_id,
                'activity': activity
            }

            returnList.append(ticket)

    returnList = sorted(returnList, key=lambda e: e['performed_at'])

    return returnList


def encoder(obj):
    if type(obj) is datetime_safe.datetime:
        return obj.strftime(conf.PERFORMED_DATE_FORMAT)


def main():
    argParser = ArgumentParser()
    argParser.add_argument('-n', type=int, default=conf.DEFAULT_COUNT)
    argParser.add_argument('-o', type=str, default=conf.DEFAULT_ACTIVITIES_FILE)

    parsed = argParser.parse_args()
    totalCount = parsed.n
    outFileName = parsed.o

    activities_data = genTickets(totalCount)

    outObj = {
        'metadata':
            {
                'start_at': activities_data[0]['performed_at'],
                'end_at': activities_data[-1]['performed_at'],
                'activities_count': totalCount * len(conf.STATUS_LIST)
            },
        'activities_data': activities_data
    }

    with open(outFileName, 'w') as outFile:
        outFile.write(json.dumps(outObj, default=encoder, indent=conf.JSON_INDENT))


if __name__ == '__main__':
    fake = Faker(conf.FAKER_LOCALE)
    main()
