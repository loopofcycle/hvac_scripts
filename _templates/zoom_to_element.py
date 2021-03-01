import time
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

#All Elements Of Walls Category.
spaces=FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_MEPSpaces).WhereElementIsNotElementType().ToElements()
selected_ids = uidoc.Selection.GetElementIds()
for id in selected_ids:
	element = doc.GetElement(id)
	uidoc.ShowElements(element)
	print(element)
	print(id)

print(time.localtime()[3:-4])