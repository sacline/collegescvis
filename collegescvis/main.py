"""Entry point for the College Scorecard Visualizer.

Functions:
    main(): main entry point into the College Scorecard Visualizer.
"""
import os
import sys
import time
from dbbuilder import Dbbuilder
import decoder
from PyQt4 import QtGui
from interface import Interface


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
    builder = Dbbuilder(db_path, types_dest_path)
    if os.path.isfile(db_path):
        print('Database found.')
    else:
        print('Generating database from raw data...')
        start_time = time.time()
        builder.build_database()
        print('Database structure generated in %s seconds.'
              % (time.time() - start_time))
    for year in range(1996, 2014):
        path = ('%s/merged_' + str(year) + '_PP.csv') % (raw_data_path)
        builder.update_database(path, str(year))

    app = QtGui.QApplication(sys.argv)
    interface = Interface(db_path)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
