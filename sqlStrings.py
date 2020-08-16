
create_enum_table = (
    'CREATE TABLE enum_{name}( '
    'id INTEGER NOT NULL, '
    '{name}_type TEXT NOT NULL, '
    'PRIMARY KEY (id));'
)

insert_enum_table = 'INSERT INTO enum_{name}(id, {name}_type) VALUES( ?, ? );'

create_rel_table = 'CREATE TABLE {table_name}( {table_props} );'

insert_rel_table = 'INSERT INTO {table_name}( {table_props} ) VALUES( {param_styles} );'

user_table_props = {
    'name': 'user',
    'props': (
        'id INTEGER NOT NULL',
        'first_name TEXT',
        'last_name TEXT',
        'email TEXT',
        'PRIMARY KEY (id)'
    )}

agent_table_props = {
    'name': 'agent',
    'props': (
        'id INTEGER NOT NULL',
        'first_name TEXT',
        'last_name TEXT',
        'department TEXT',
        'PRIMARY KEY (id)'
    )}

ticket_table_props = {
    'name': 'ticket',
    'props': (
        'id INTEGER NOT NULL',
        'performer_type TEXT NOT NULL',
        'performer_id INTEGER NOT NULL',
        'shipment_address TEXT NOT NULL',
        'shipment_date INTEGER NOT NULL',
        'category_enum INTEGER NOT NULL',
        'issue_enum INTEGER NOT NULL',
        'group_enum INTEGER NOT NULL',
        'product_enum INTEGER NOT NULL',
        'PRIMARY KEY (id)',
        'FOREIGN KEY (performer_id) REFERENCES user(id)',
        'FOREIGN KEY (category_enum) REFERENCES enum_category(id)',
        'FOREIGN KEY (issue_enum) REFERENCES enum_issue(id)',
        'FOREIGN KEY (group_enum) REFERENCES enum_group(id)',
        'FOREIGN KEY (product_enum) REFERENCES enum_product(id)',
    )}

activity_table_props = {
    'name': 'activity',
    'props': (
        'id INTEGER NOT NULL',
        'ticket_id INTEGER NOT NULL',
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
        'FOREIGN KEY (requester) REFERENCES user(id)',
    )}
