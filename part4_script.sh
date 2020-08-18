
# python -m pip install Faker --user

python part1_ticketGen.py -n 100 -o activities.json

python part2_create_db.py -o db.sqlite3

python part2_load_json2db.py -i activities.json -o db.sqlite3

sqlite3 db.sqlite3 < part3_query.sql