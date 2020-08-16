from datetime import date, time

START_DATE = date(2019, 1, 1)
END_DATE = date(2020, 8, 14)

START_WORK_HOURS = time(9, 0, 0)
END_WORK_HOURS = time(17, 0, 0)

SHIPMENT_DATE_FORMAT = '%d %b, %Y'
PERFORMED_DATE_FORMAT = '%d-%m-%Y %X %z'

STATUS_LIST = ['Open', 'Waiting for Customer', 'Waiting for Third Party', 'Pending', 'Resolved', 'Closed']
CATEGORY_LIST = ['Phone', 'PC', 'Tablet', 'Laptop']
GROUP_LIST = ['exchange', 'refund', 'return', 'RMA', 'repair']
PRODUCT_LIST = ['storage', 'headphone', 'accessory', 'device']
ISSUE_LIST = ['Incident', 'Warranty']

PERFORMER_TYPE_STR = 'user'
CONTACTED_CUSTOMER_BOOL = True

RAND_TIMEDELTA_DAYS = 7
MIN_TIMEDELTA_DAYS = 1

RAND_ID_DIGITS = 6

FAKER_LOCALE = 'en_AU'
DEFAULT_COUNT = 10
DEFAULT_JSON_FILE = 'activities.json'
DEFAULT_SQLITE_FILE = 'db.sqlite3'
