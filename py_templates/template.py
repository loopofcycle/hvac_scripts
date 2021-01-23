import time, csv
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

file='C:\Users\Igor\Google Диск\Code\Projects\pyRevit\spaces.csv'

spaces=FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_MEPSpaces).WhereElementIsNotElementType().ToElements()
lines = FilteredElementCollector(doc).OfClass(CurveElement).OfCategory(BuiltInCategory.OST_Lines)

spaces_num=sorted(spaces_result)
with open(file, 'wb') as csvfile:
	writer=csv.writer(csvfile, delimiter=';')
	writer.writerow([r[0],r[1],r[2],r[3],s[0],s[1],s[2]]) # row for each surface in space
