"""Examine Scorecard raw data to determine its characteristics.

In order to build a database, information is needed about the type of data in
the Scorecard .csv files. This script examines the data and extracts the
essential information: the name of the data category, the type of data, and the
index it is located at in the raw data files. This information is then saved in
JSON format.

Functions:
    _validate_data_path(data_path): Raise exceptions for invalid data paths.
    write_data_types(data_path, dest_path): Write data index info to file.
    _get_data_types(data_path): Find valid data and their types.
    _validate_scorecard_entry(entry): Raise an exception if entry is invalid.
    _read_values(entry): Count valid data within a scorecard entry.
    _find_type(entry): Return a data type based on the entry.
"""
import glob
import json


def _validate_data_path(data_path):
    """Raise exceptions for invalid raw data paths.

    Args:
        data_path: Path to the folder containing Scorecard data files.

    Raises:
        TypeError: If the data path was not correctly formatted as a string.
        FileNotFoundError: If the data path glob was empty.
    """
    if not isinstance(data_path, str):
        raise TypeError('Data path is not a string')
    if not glob.glob(data_path):
        raise FileNotFoundError('No raw data files found')

def write_data_types(data_path, dest_path):
    """Write the data index information in JSON format to a target file.

    Args:
        data_path: Path to the folder containing Scorecard data files.
        dest_path: Path to the destination file.
    """
    _validate_data_path(data_path)
    data_types = _get_data_types(glob.glob(data_path))
    with open(dest_path, 'w') as data_file:
        data_file.write(json.dumps(data_types))
        data_file.close()

def _get_data_types(data_path):
    """Return a list of data-containing indices, the data type, and the index.

    Each input file is read to see if there is some valid data for each
    category within the College Scorecard raw data. If a category has no valid
    data, it is ignored and not included in the list.

    Args:
        data_path: Path to the folder containing Scorecard data files.

    Returns:
        A list of tuples containing the name of the data, the type, and the
        index. The list is returned sorted by the index. An example is below:

        [ ('UNITID', 'INTEGER', 0), ('OPEID', 'TEXT', 1), ... ]
    """
    tuple_list = []
    for input_file in data_path:
        print('Reading...', input_file)
        with open(input_file, 'r', encoding='latin-1') as data_file:
            lines = data_file.readlines()
            data_list = [[] for count in lines[0].split(',')]
            for line in lines:
                index = 0
                for entry in line.split(','):
                    if entry[-1] == '\n': entry = entry[:-1]
                    data_list[index].append(entry)
                    index += 1
            good_indices = []
            for data_index in range(len(data_list)):
                if any(data_index == entry[2] for entry in tuple_list): continue
                data_counts = _read_values(data_list[data_index])
                if data_counts[0] != 0: good_indices.append(data_index)
            print(len(good_indices))
            for index in good_indices:
                if index == 6:
                    data_type = 'TEXT'
                else:
                    data_type = _find_type(data_list[index])
                tup = (data_list[index][0], data_type, index)
                if tup not in tuple_list: tuple_list.append(tup)
    return sorted(tuple_list, key=lambda x: x[2])

def _validate_scorecard_entry(entry):
    """Check a Scorecard entry, raising an exception if data is invalid.

    Args:
        entry: List of Scorecard data - [Category, value1, value2, ...]

    Raises:
        TypeError: If the entry is an invalid data type.
        ValueError: If the entry is an empty list containing no data.
    """
    if not isinstance(entry, list):
        raise TypeError('Scorecard entry not formatted as a list.')
    if not entry:
        raise ValueError('Scorecard data entry is empty.')
    for value in entry:
        if not isinstance(value, str):
            raise TypeError('Scorecard entry contains non-string value.')

def _read_values(entry):
    """Create a count of valid data within a Scorecard entry.

    Args:
        entry: List of Scorecard data - [Category, value1, value2, ...]

    Returns:
        counts: List of counts of valid data, 'PrivacySuppressed', and 'NULL'
            values.
    """
    _validate_scorecard_entry(entry)
    counts = [0, 0, 0]
    for value in entry[1:]:
        if value == 'NULL':
            counts[2] += 1
        elif value == 'PrivacySuppressed':
            counts[1] += 1
        else:
            counts[0] += 1
    return counts

def _find_type(entry):
    """Return a data type based on the entry.

    Args:
        entry: List of Scorecard data - [Category, value1, value2, ...]

    Returns:
        data_type: String description of the data type - 'INTEGER', 'REAL', or
            'TEXT'.
    """
    _validate_scorecard_entry(entry)
    data_type = 'INTEGER'
    for value in entry[1:]:
        if value in ('NULL', 'PrivacySuppressed'):
            continue
        else:
            try:
                int(value)
            except ValueError:
                try:
                    float(value)
                    data_type = 'REAL'
                except ValueError:
                    str(value)
                    data_type = 'TEXT'
    return data_type
