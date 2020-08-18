# file to store all the sql configurations and database connection function
# here the database schema and relational model is defined,
# this is done in order to separate it from the code.

# sqlite imported for connection
import sqlite3


# function connects to db file and returns object or None if failed
def create_connection(dbFileName):
    db = None
    try:
        db = sqlite3.connect(dbFileName)
    except sqlite3.Error as e:
        print(e)
    return db


# enum tables creation template,
# name is replaced in code with status, category, group etc.
create_enum_table = (
    'CREATE TABLE enum_{name}( '
    'id INTEGER NOT NULL, '
    '{name}_type TEXT NOT NULL, '
    'PRIMARY KEY (id));'
)

# enum tables insert template,
# name is replaced by code, and (?, ?) are param_styles of SQLITE
insert_enum_table = 'INSERT INTO enum_{name}(id, {name}_type) VALUES(?, ?);'

# relational table creation template, populated at runtime according to the table_props
create_rel_table = 'CREATE TABLE {table_name}({table_props} );'

# relational table insertion template
insert_rel_table = 'INSERT INTO {table_name}({insert_props}) VALUES({param_styles});'

# table types with their respective properties.
# in the format - name: a name given to the table
#   props: the list of properties along with their data types
#           Also includes Primary key and Foreign Key constraints.
#   insert: the list of properties that are required while inserting

# table_props start
user_table_props = {
    'name': 'user',
    'props': (
        'id INTEGER NOT NULL',
        'name TEXT NOT NULL',
        'email TEXT NOT NULL',
        'PRIMARY KEY (id)'),
    'insert': ('id', 'name', 'email')}

agent_table_props = {
    'name': 'agent',
    'props': (
        'id INTEGER NOT NULL',
        'name TEXT NOT NULL',
        'TFN TEXT NOT NULL',
        'PRIMARY KEY (id)'),
    'insert': ('id', 'name', 'TFN')}

ticket_table_props = {
    'name': 'ticket',
    'props': (
        'id INTEGER NOT NULL',
        'performer_type TEXT NOT NULL',
        'performer_id INTEGER NOT NULL',
        'shipping_address TEXT NOT NULL',
        'shipment_date TEXT NOT NULL',
        'category_enum INTEGER NOT NULL',
        'issue_enum INTEGER NOT NULL',
        'group_enum INTEGER NOT NULL',
        'product_enum INTEGER NOT NULL',
        'PRIMARY KEY (id)',
        'FOREIGN KEY (performer_id) REFERENCES user(id)',
        'FOREIGN KEY (category_enum) REFERENCES enum_category(id)',
        'FOREIGN KEY (issue_enum) REFERENCES enum_issue(id)',
        'FOREIGN KEY (group_enum) REFERENCES enum_group(id)',
        'FOREIGN KEY (product_enum) REFERENCES enum_product(id)',),
    'insert': (
        'id',
        'performer_type',
        'performer_id',
        'shipping_address',
        'shipment_date',
        'category_enum',
        'issue_enum',
        'group_enum',
        'product_enum'
    )}

activity_table_props = {
    'name': 'activity',
    'props': (
        'id INTEGER NOT NULL',
        'ticket_id INTEGER NOT NULL',
        'performed_at INTEGER NOT NULL',
        'contacted_customer BOOLEAN NOT NULL',
        'source INTEGER NOT NULL',
        'status_enum INTEGER NOT NULL',
        'priority INTEGER NOT NULL',
        'agent_id INTEGER NOT NULL',
        'requester INTEGER NOT NULL',
        'PRIMARY KEY (id)',
        'FOREIGN KEY (ticket_id) REFERENCES ticket(id)',
        'FOREIGN KEY (status_enum) REFERENCES enum_status(id)',
        'FOREIGN KEY (agent_id) REFERENCES agent(id)',
        'FOREIGN KEY (requester) REFERENCES user(id)'),
    'insert': (
        'id',
        'ticket_id',
        'performed_at',
        'contacted_customer',
        'source',
        'status_enum',
        'priority',
        'agent_id',
        'requester'
    )}
# table_props end
