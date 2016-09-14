"""Entry point for the College Scorecard Visualizer.

Functions:
    main(): main entry point into the College Scorecard Visualizer.
"""
import os
import time
from dbbuilder import Dbbuilder
import decoder


def main():
    """Call modules to build database and visualize data."""
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
    print('Database location:', db_path)
    if os.path.isfile(db_path):
        print('Database found.')
    else:
        builder = Dbbuilder(db_path, types_dest_path)
        print('Generating database from raw data...')
        start_time = time.time()
        builder.build_database()
        print('Database generated in %s seconds.' % (time.time() - start_time))
        #path_2000 = '%s/merged_2000_PP.csv' % (raw_data_path)
        #builder.update_database(path_2000, '2000')

if __name__ == '__main__':
    main()
