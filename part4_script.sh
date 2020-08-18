# this script calls the other scripts one by one

# Ensure python requirements are installed prior to use
# commented out as redundant in readme for project setup
# python -m pip install -r requirements.txt --user

# run ticket generator
python part1_ticketGen.py -n 1000 -o activities.json

# run database creation
python part2_create_db.py -o db.sqlite3

# run for json to relational conversion
python part2_load_json2db.py -i activities.json -o db.sqlite3

# query the database, by loading the db and running the query from file
# need to have sqlite3 installed as specified in readme file
sqlite3 db.sqlite3 < part3_query.sql