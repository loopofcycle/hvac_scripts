import time, csv, os, clr, logging
from pprint import pprint
from datetime import datetime
from System.Collections.Generic import List
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference('RevitServices')

doc = __revit__.ActiveUIDocument.Document

counter = 0
with Transaction(doc, 'Простановка ID') as tr:
	tr.Start()
	dont_have_parameter = 0
	read_only = 0
	for element in FilteredElementCollector(doc).WhereElementIsNotElementType():

		param = element.LookupParameter('ID_элемента')
		
		if param is None:
			dont_have_parameter =+ 1
			continue

		if param.IsReadOnly:
			read_only =+ 1
			continue

		param.Set(str(element.Id.IntegerValue))
		counter += 1

	tr.Commit()
if counter == 0:
	TaskDialog.Show('Результат', 'Не добавлен ни один ID. Вероятно, у вас не настроен параметер "ID_элемента"')  
else:
    TaskDialog.Show('Результат', 'Добавлены id для %d элементов' % counter)

print(dont_have_parameter, read_only)
print(datetime.now().isoformat(), 'succesfully')
