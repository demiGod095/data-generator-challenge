import json
from argparse import ArgumentParser
from datetime import datetime, timedelta

from faker import Faker
from faker.utils import datetime_safe

# from configuration import START_DATE, END_DATE, START_WORK_HOURS, END_WORK_HOURS, CATEGORY_LIST
import configuration as conf


def main():
    argParser = ArgumentParser()
    argParser.add_argument('-i', type=str, default=conf.DEFAULT_JSON_FILE)
    argParser.add_argument('-o', type=str, default=conf.DEFAULT_SQLITE_FILE)

    parsed = argParser.parse_args()
    inFileName = parsed.i
    outFileName = parsed.o

    print(f"{inFileName} -> {outFileName}")

if __name__ == '__main__':
    fake = Faker(conf.FAKER_LOCALE)
    main()
