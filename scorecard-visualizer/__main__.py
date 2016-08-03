"""Entry point for the College Scorecard Visualizer."""
import glob
import json
import os
import time
import dbbuilder
import decoder

def main():
    print('Beginning College Scorecard Visualizer...')
    print('Checking database...')

    raw_data_path = os.path.join(
        os.path.dirname(__file__), os.pardir, 'data', 'raw_data')
    glob_path = '%s/merged_*.csv' % (raw_data_path)

    types_dest_path = os.path.join(
        os.path.dirname(__file__), os.pardir, 'data', 'temp', 'data_types.txt')
    if os.path.isfile(types_dest_path):
        print('Data types file found.')
    else:
        print('Generating data type file from raw data...')
        decoder.write_data_types(glob_path, types_dest_path)

    db_path = os.path.join(
        os.path.dirname(__file__), os.pardir, 'data', 'database',
        'college-scorecard.sqlite')
    print(db_path)
    if os.path.isfile(db_path):
        print('Database found.')
    else:
        print('Generating database from raw data...')
        start_time = time.time()
        dbbuilder.initialize_database(db_path, types_dest_path)
        dbbuilder.build_database()
        print('Database generated in %s seconds.' % (time.time() - start_time))

if __name__ == '__main__':
    main()
