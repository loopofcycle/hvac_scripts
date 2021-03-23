import os, csv, codecs
from pprint import pprint

def create_spec_dict(filenames, delimiter='\t', HEADER_blanks=8):
    spec_dict = dict()
    for name in filenames:
        with codecs.open(os.path.join(desktop, name), 'rU', 'utf-16') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter= delimiter)
            current_header = 'default_header'
            for row in csv_reader:
                is_header = bool(row.count('') == HEADER_blanks)
                header_name = [element for element in row if element != ''].pop()
                if is_header:
                    current_header = header_name
                if current_header not in spec_dict.keys():
                    spec_dict[current_header] = []
                if not is_header:
                    spec_dict[current_header].append(row)
    return spec_dict

def write_to_csv(data_dict, path_to_csv, delimiter='\t'):
    with codecs.open(path_to_csv, 'w', 'utf-16') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter= delimiter)
        for header, data in data_dict.items():
            spamwriter.writerow([header]) 
            for row in data: spamwriter.writerow(row) 

csv_file_name = 'specification.csv'
desktop = os.path.expanduser("~\\Desktop")
prefix = 'ОВ.С_'

filenames = [str(file) for file in os.listdir(desktop) if file.startswith(prefix)]

spec_dict = create_spec_dict(filenames)

write_to_csv(spec_dict, os.path.join(desktop, csv_file_name))

for name in filenames:
    os.remove(os.path.join(desktop, name))
