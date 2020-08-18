# Aginic data generation

The project generates data similar to the format present in [example.json](example.json) file.
Then converts the json to relational model, by first creating the database and its schema, and then loading the records one by one. 

## Build Instructions

#### Requirements
1. Ensure python3 is installed on the command line by running `python3` in terminal and seeing the shell change to python interpreter.
1. Install the python dependencies using the following command, this installs Faker library used in the project for getting random data.
    ```
        python -m pip install -r requirements.txt --user
    ```
1. Install sqlite command line tool by using package manager like so, for Debian based distributions:-
    ```
        sudo apt-get install sqlite3
    ```
   or you can go [here](https://www.sqlite.org/download.html) and download the appropriate binary directly. 

#### Execution
CD to the project directory and run the script part4_script.sh using bash. The script has preconfigured file name arguments and you can choose to change them if you wish.
```
    bash part4_script.sh
```
All the parameters of the program are defined in the [configuration.py](configuration.py) file.
For example:-
1. Edit the START_DATE and END_DATE values (lines 8 and 9) to change the scope of the generated ticket's dates.
1. Similarly, you can change the working hours defined on lines 12 and 13.

## Design Decisions
#### Assumptions
1. Only activities with a status field are relevant to the project. The first activity with just a note field is not important as it doesn't provide much information about the status, and hence not generated.
1. Status of any ticket takes the following order:-
    1. Open
    1. Waiting for Customer
    1. Waiting for Third Party
    1. Pending
    1. Resolved
    1. Closed
1. Output of the query in part 3 is expected as hours, for easy understanding of how much time does a particular ticket needs. 
1. The individual columns of part 3 are defined as following difference in timestamps: -
    1. Time spent open: for how long was the ticket open
        * "Waiting for Customer" - "Open"
    1. Time spent Waiting on Customer: how long did it take for the customer to respond to the ticket
        * "Waiting for Third Party" - "Waiting for Customer"
    1. Time spent waiting for response (Pending Status): how long was the ticket in pending state
        * "Resolved" - "Pending"
    1. Time till resolution: how long did it take for a ticket to go from resolved to closed
        * "Closed" - "Resolved"
    1. Time to first response: When was the customer first contacted after generation of the ticket
        * Timestamp of first occurrence of "contacted_customer = True" for a ticket - "Open"
        * Initially, It seemed like this last time was equal to the first time, i.e. "Waiting for Customer" - "Open", but after carefully reading the example, I saw that I can use the boolean 'contacted_customer field' for this purpose.
        * The code was hence modified to have a random number of 'False' values for the earlier activities, and 'True' for the rest.

#### Python
1. Python is the language of choice for writing data generation and handling scripts.
1. It was a requirement specified for part 1 of this challenge, and hence was the logical successor for solving the rest.
1. All the necessary constants were defined in a file for easy access throughout the project.
    * Lists like Group, Category, etc. definitions can be changed according to need, and all the scripts will just work without having to, accommodate for the changes.
    * This applies to the database part as well. The SQL string definitions were stored separate from the code and are hence easier to view and change as needed.
    * It provides modularity of code, even SQL Queries and keeps the main script clean.
    
#### SQLite
1. The database engine is flexible in terms of use, and has loose type definitions.
1. It doesn't support Date and Time data types, hence the datetime fields are of type Integer so that it can be stored as Unix Epoch Time stamps.
1. This conversion is done in python while inserting into the DB for the "performed_at" field.
1. This conversion is skipped for the "shipment_date" attribute, and is stored as the original string instead, as it is not needed for the future parts.
1. The schema for tickets was chosen to have the fields that may remain constant over the entire ticket. (This may not necessarily be true for all fields and the tables can be modified according to need)
1. The schema for activities has fields that can change during the ticket's journey, for example, the "priority" could change over time.
1. Users and Agents (employees) are created with random details when inserting tickets to the database, their tables are tokens, and can be changed according to actual needs.
1. The part3 [script](part3_query.sql) self joins the activity table for all getting all the necessary values in a single row.
    * The first 6 joins are done for getting the various statuses of a particular ticket together.
    * The last join collects the times when customer has been contacted and the `MIN()` along with `GROUP BY` determines the first activity of contact. According to assumption `4.v`.
