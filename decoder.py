import glob
import os

def main():
    datapath = 'data/merged_*.csv'
    data_types = get_data_types(glob.glob(datapath))

#Returns a list of tuples containing indices that have data, the data type, and the index.
def get_data_types(data_path):
    tuple_list = []
    for input_file in data_path:
        print(input_file)
        with open(input_file, 'r', encoding = 'latin-1') as f:
            lines = f.readlines()
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
                data_counts = read_values(data_list[data_index])
                if data_counts[0] != 0: good_indices.append(data_index)
            print(len(good_indices))
            for index in good_indices:
                if index == 6:
                    data_type = 'TEXT'
                else:
                    data_type = find_type(data_list[index])
                tup = (data_list[index][0], data_type, index)
                if tup not in tuple_list: tuple_list.append(tup)
    return sorted(tuple_list, key = lambda x: x[2])

#Accepts a data entry containing [Category, value1, value2...]
#Returns counts of real values, PrivacySuppressed values, and Null values.
def read_values(entry):
    counts = [0, 0, 0] #values, privacy, null
    for value in entry[1:]:
        if value == 'NULL':
            counts[2] += 1
        elif value == 'PrivacySuppressed':
            counts[1] += 1
        else:
            counts[0] += 1
    return counts

#Accepts a list of data [CATEGORY, value1, value2...]
#Returns a string based on the type of data (TEXT, INTEGER, or REAL)
def find_type(data_entry):
    data_type = 'INTEGER'
    for value in data_entry[1:]:
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

if __name__ == "__main__":
    main()
