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
    build_table('College')
    build_year_tables()

def build_year_tables():
    #This is hardcoded for now, but can be taken from input
    build_table('1999')
    for year in range(2000, 2014):
        copy_table('1999', str(year))

def build_table(table_name):
    lower_limit = 1 if table_name == 'College' else 37
    upper_limit = 36 if table_name == 'College' else 1728
    autoincrement = "AUTOINCREMENT" if table_name == 'College' else ''

    cur.execute('''
        CREATE TABLE IF NOT EXISTS "%s" (
        college_id INTEGER PRIMARY KEY %s
        )''' % (sanitize(table_name), autoincrement))

    for data_type in data_types:
        if data_type[2] > upper_limit: break
        if data_type[2] < lower_limit: continue
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

def copy_table(source_table, target_table):
    cur.execute(
        '''SELECT sql FROM sqlite_master WHERE type='table' AND name ="%s"
        ''' % (sanitize(source_table)))
    statement = cur.fetchone()[0]
    new_statement = statement.replace(
        sanitize(source_table), sanitize(target_table), 1)
    cur.execute(new_statement)

def populate_database():
    cur.execute('''''')

if __name__ == '__main__':
    main()
