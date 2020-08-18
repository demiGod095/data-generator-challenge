# file to store all the constants used in the project.
# here you can change the parameters to change the behaviour of the scripts.

# datetime needed for storing dates and times
from datetime import date, time

# defines the dates within which the activities need to be generated
START_DATE = date(2019, 1, 1)
END_DATE = date(2020, 8, 14)

# defines the hour of the day withing which the activities are allowed
START_WORK_HOURS = time(9, 0, 0)
END_WORK_HOURS = time(17, 0, 0)

# date format conversions for writing to json
SHIPMENT_DATE_FORMAT = '%d %b, %Y'
PERFORMED_DATE_FORMAT = '%d-%m-%Y %X %z'

# various options for parameters that are present in activities
STATUS_LIST = ['Open', 'Waiting for Customer', 'Waiting for Third Party', 'Pending', 'Resolved', 'Closed']
CATEGORY_LIST = ['Phone', 'PC', 'Tablet', 'Laptop']
GROUP_LIST = ['exchange', 'refund', 'return', 'RMA', 'repair']
PRODUCT_LIST = ['storage', 'headphone', 'accessory', 'device']
ISSUE_LIST = ['Incident', 'Warranty']

# static strings found in the activities
PERFORMER_TYPE_STR = 'user'

# config for how much two activities can be separated from each other
RAND_TIMEDELTA_DAYS = 7
MIN_TIMEDELTA_DAYS = 1

# number of digits in user's and agent's IDs
RAND_ID_DIGITS = 4

# faker locale profile for localised addresses and emails
FAKER_LOCALE = 'en_AU'

# system arguments defaults for the program
DEFAULT_COUNT = 100
DEFAULT_JSON_FILE = 'activities.json'
DEFAULT_SQLITE_FILE = 'db.sqlite3'
