
# python -m pip install Faker --user

time python part1_ticketGen.py -n 100 -o activities.json

time python part2_create_db.py -o db.sqlite3

time python part2_load_json2db.py -i activities.json -o db.sqlite3

time ./sqlite3 db.sqlite3 < query.sql
# sqlite3 db.sqlite3 -column -headers "select * from user;"