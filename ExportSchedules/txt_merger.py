# -*- coding: utf-8 -*-
import os, csv, codecs
from docx_printer import DocxPrinter

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

docx_file_name = 'specification.docx'
docx_template = 'C:\\Users\\igor\\gdrive\\Code\\revit_scripts\\ExportSchedules\\specification.docx'
desktop = os.path.expanduser("~\\Desktop")
prefix = 'ОВ.С_'

filenames = [str(file) for file in os.listdir(desktop) if file.startswith(prefix)]

spec_dict = create_spec_dict(filenames)

printer = DocxPrinter(docx_template, print_path= desktop)
printer.print(docx_file= docx_file_name, specification= spec_dict)

for name in filenames:
    os.remove(os.path.join(desktop, name))

print('files', filenames, 'have been merged !')
