"""
decoder.py
Copyright (C) <2017>  <S. Cline>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import glob
import json

def write_data_types(data_path, dest_path):
    """Write the data index information in JSON format to a target file.

    Args:
        data_path: Path to the folder containing Scorecard data files.
        dest_path: Path to the destination data_types file.
    """
    _validate_data_path(data_path)
    data_types = _get_data_types(glob.glob(data_path))
    with open(dest_path, 'w') as data_file:
        data_file.write(json.dumps(data_types))
        data_file.close()

def _validate_data_path(data_path):
    """Raise exceptions for invalid raw data paths.

    Args:
        data_path: Path to the folder containing Scorecard raw data files.

    Raises:
        TypeError: If the data path was not correctly formatted as a string.
        FileNotFoundError: If the data path glob was empty.
    """
    if not isinstance(data_path, str):
        raise TypeError('Data path is not a string')
    if not glob.glob(data_path):
        raise FileNotFoundError('No raw data files found')

def _get_data_types(data_path):
    """Return a list of data-containing indices, the data type, and the index.

    Each input file is read to see if there is some valid data for each
    category within the College Scorecard raw data. If a category has no valid
    data, it is ignored and not included in the list.

    Args:
        data_path: Path to the folder containing Scorecard data files.

    Returns:
        tuple_list: A list of tuples containing the name of the data, the type,
        and the index. The list is returned sorted by the index. An example is
        below:

        [ ('UNITID', 'INTEGER', 0), ('OPEID', 'TEXT', 1), ... ]
    """
    tuple_list = []
    for input_file in data_path:
        print('Reading...', input_file)
        with open(input_file, 'r', encoding='utf-8-sig') as data_file:
            lines = data_file.readlines()

            #One empty list for each data type found in the first line of the
            #raw data file.
            data_list = [[] for count in lines[0].split(',')]

            #Fill each list with all the values for the data type
            for line in lines:
                new_line = replace_commas(line)
                index = 0
                for entry in new_line.split(','):
                    if entry[-1] == '\n': entry = entry[:-1]
                    data_list[index].append(entry)
                    index += 1

            #Add only the data types that contain valid data
            good_indices = []
            for data_index in range(len(data_list)):
                #Skip if the data index is already in the tuple list
                if any(data_index == entry[2] for entry in tuple_list): continue
                if _is_good_data(data_list[data_index]):
                    good_indices.append(data_index)
            print(
                str(len(good_indices)) + ' data types added to list.')
            for index in good_indices:
                #Special case: make zip code data TEXT instead of INTEGER
                if index == 6:
                    data_type = 'TEXT'
                else:
                    data_type = _find_type(data_list[index])
                tup = (data_list[index][0], data_type, index)
                if tup not in tuple_list: tuple_list.append(tup)
    return sorted(tuple_list, key=lambda x: x[2])

def replace_commas(string):
    """Replace commas that exist in the data as part of string data.

    Some string data can contain commas that interfere with
    the breaking apart of the csv data. These commas need to be
    replaced before calling line.split(','). In the data these
    commas are surrounded by quotation marks ("), making them
    easy to replace.

    Args:
        string: line of data from data file to check.

    Returns:
        new_line: line that has had data-commas removed.
    """
    if '"' not in string:
        return string
    else:
        index1 = 0
        index2 = 0
        while True:
            index1 = string.find('"', index2+1)
            index2 = string.find('"', index1+1)
            if index1 == -1 or index2 == -1:
                return string
            first_substring = string[0:index1]
            new_substring = string[index1:index2].replace(',', ';')
            last_substring = string[index2:]
            string = first_substring + new_substring + last_substring

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

def _is_good_data(entry):
    """Create a count of valid data within a Scorecard entry.

    Args:
        entry: List of Scorecard data - [Category, value1, value2, ...]

    Returns:
        boolean: True if there is at least one good data value in entry
    """
    for value in entry[1:]:
        if value in ('NULL', 'PrivacySuppressed'):
            continue
        else:
            return True
    return False

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
