import json
import pprint

from faker import Faker

from argparse import ArgumentParser
from datetime import datetime, date, time, timedelta

from faker.utils import datetime_safe

startDate = date(2019, 1, 1)
endDate = date(2020, 8, 14)
startTime = time(9, 0, 0)
endTime = time(17, 0, 0)


def genTickets(totalCount):
    startId = fake.random_int()

    returnList = []

    for ticket_id in range(startId, startId + totalCount):
        ticketDateStart = fake.date_between_dates(startDate, endDate)
        performer_type = "user"
        performer_id = fake.random_number(digits=6)

        shipping_address = fake.address()
        shipment_date = ticketDateStart.strftime("%d %b, %Y")
        category = fake.word(ext_word_list=['Phone', 'PC', 'Tablet', 'Laptop'])
        contacted_customer = True
        issue_type = "Incident"
        source = fake.random_digit_not_null()
        priority = fake.random_digit_not_null()
        group = fake.word(ext_word_list=['exchange', 'refund', 'return'])
        # agent_id = performer_id
        requester = fake.random_number(digits=6)
        product = fake.word(ext_word_list=['storage', 'headphone', 'accessory', 'device'])

        thisDate = ticketDateStart

        for status in status_list:
            activity = {
                "shipping_address": shipping_address,
                "shipment_date": shipment_date,
                "category": category,
                "contacted_customer": contacted_customer,
                "issue_type": issue_type,
                "source": source,
                "status": status,
                "priority": priority,
                "group": group,
                "agent_id": performer_id,
                "requester": requester,
                "product": product
            }

            thisDate = (thisDate + fake.time_delta(timedelta(days=5))) + timedelta(days=1)

            performed_at = fake.date_time_between_dates(
                datetime_start=datetime.combine(thisDate, startTime),
                datetime_end=datetime.combine(thisDate, endTime)
            ).astimezone()

            ticket = {
                # "performed_at": performed_at.strftime("%d-%m-%Y %X %z"),
                "performed_at": performed_at,
                "ticket_id": ticket_id,
                "performer_type": performer_type,
                "performer_id": performer_id,
                "activity": activity
            }

            returnList.append(ticket)

    returnList = sorted(returnList, key=lambda e: e['performed_at'])

    return returnList


def encoder(obj):
    if type(obj) is datetime_safe.datetime:
        return obj.strftime("%d-%m-%Y %X %z")


def main():
    argParser = ArgumentParser()
    argParser.add_argument('-n', type=int, default=100)
    argParser.add_argument('-o', type=str, default="activities.json")

    parsed = argParser.parse_args()
    totalCount = parsed.n
    outFileName = parsed.o

    activities_data = genTickets(totalCount)

    outObj = {
        "metadata":
            {
                "start_at": activities_data[0]['performed_at'],
                "end_at": activities_data[-1]['performed_at'],
                "activities_count": totalCount * 6
            },
        "activities_data": activities_data
    }

    with open(outFileName, 'w') as outFile:
        outFile.write(json.dumps(outObj, default=encoder, indent=4))


if __name__ == "__main__":
    status_list = [
        "Open",
        "Waiting for Customer",
        "Waiting for Third Party",
        "Pending",
        "Resolved",
        "Closed"
    ]

    fake = Faker('en_AU')
    # Faker.seed(0)
    # fake.add_provider(date_time)

    # ticketDateStart = fake.date_between_dates(startDate, endDate)
    # thisDate = ticketDateStart
    # print(f"s {thisDate}")
    #
    # for e, status in enumerate(status_list):
    #     thisDate = (thisDate + fake.time_delta(timedelta(days=5))) + timedelta(days=1)
    #
    #     dt = fake.date_time_between_dates(
    #         datetime_start=datetime.combine(thisDate, startTime),
    #         datetime_end=datetime.combine(thisDate, endTime)
    #     )
    #
    #     print(f"{e} {dt}")
    #     pass

    main()
