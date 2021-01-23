# -*- coding: utf-8 -*-
import os
import csv
import codecs
from docx_printer import DocxPrinter

HEADER_blanks = 8
delimiter = '\t'
docx_file_name = 'specification.docx'
docx_template = 'C:\\Users\\igor\\Google Диск\\Code\\pyExportSchedules\\specification.docx'
desktop = os.path.expanduser("~\\Desktop")
prefix = 'ОВ.С_'

spec_dict = {}
filenames = [str(file) for file in os.listdir(desktop) if file.startswith(prefix)]
print(filenames)
for fname in filenames:
    csv_reader = csv.reader(codecs.open(os.path.join(desktop, fname), 'rU', 'utf-16'),
                            delimiter= delimiter)
    current_header = 'common'
    for row in csv_reader:
        is_header = bool(row.count('') == HEADER_blanks)
        header_name = [element for element in row if element != ''].pop()
        if is_header:
            current_header = header_name
        if current_header not in spec_dict.keys():
            spec_dict[current_header] = []
        if not is_header:
            spec_dict[current_header].append(row)
printer = DocxPrinter(docx_template, print_path= desktop)
printer.print(docx_file= docx_file_name, specification= spec_dict)
print('files', filenames, 'have been merged !')