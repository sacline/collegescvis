import json
import sqlite3

def main():
    db_name = 'college-scorecard.sqlite'
    global data_types
    with open('data_types.txt', 'r') as f:
        data_types = json.loads(f.readline())

    global conn
    global cur
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    build_database()
    populate_database()

def build_database():
    build_college_table()
    build_year_tables()

def build_college_table():
    cur.execute('''
        CREATE TABLE IF NOT EXISTS College (
        college_id INTEGER PRIMARY KEY AUTOINCREMENT
        )''')
    for data_type in data_types:
        if data_type[2] < 36:
            try:
                cur.execute(
                    '''ALTER TABLE College ADD COLUMN %s %s'''
                    % (sanitize(data_type[0]), sanitize(data_type[1])))
            except sqlite3.OperationalError:
                pass

def build_year_tables():
    #This is hardcoded for now, but can be taken from input
    for year in range(1999, 2014):
        table_name = str(year)
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS "%s" (
            college_id INTEGER PRIMARY KEY
            )''' % (sanitize(table_name)))
        for data_type in data_types:
            if data_type[2] >= 36:
                try:
                    cur.execute(
                        '''ALTER TABLE "%s" ADD COLUMN %s %s'''
                        % (sanitize(table_name), sanitize(data_type[0]),
                        sanitize(data_type[1])))
                except sqlite3.OperationalError:
                    pass

'''
Needed for table names, column names, and data types that cannot be
specified with parameter substitution.
'''
def sanitize(string):
    bad_chars = ['"', "'", ';', '\\', '/']
    for char in bad_chars:
        if char in string:
            raise ValueError('Table input contains ' + badchar)
    return string

def populate_database():
    cur.execute('''''')

if __name__ == '__main__':
    main()
