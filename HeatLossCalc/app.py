import time, csv, os
from pprint import pprint
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
#from Autodesk.Revit.UI import *
#from Autodesk.Revit.DB import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()
tree = {}
for level in levels:
	tree[level] = []
pprint(tree)

for room in rooms:
	tree[room.Level].append(room)
pprint(tree)