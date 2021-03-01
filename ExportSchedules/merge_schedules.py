import os, csv, codecs

HEADER_blanks = 8
delimiter = '\t'
docx_file_name = 'specification.docx'
csv_file_name = 'specification.csv'
desktop = os.path.expanduser("~\\Desktop")
prefix = 'ОВ.С_'

spec_dict = {}
filenames = { int(file.split('_')[1]): str(file)
                for file in os.listdir(desktop)
                if file.startswith(prefix) }

for number, name in sorted(filenames.items()):
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
    #os.remove(os.path.join(desktop, name))

with codecs.open(csv_file_name, 'w', 'utf-16') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter= delimiter)
    for header, data in spec_dict.items():
        for row in data: spamwriter.writerow(row) 
print(len(filenames), 'files have been merged !')