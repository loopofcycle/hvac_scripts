import time, csv, os
from pprint import pprint
from datetime import datetime
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory 
#from Autodesk.Revit.UI import *
#from Autodesk.Revit.DB import *
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference('RevitServices')
os.chdir('C:\\Users\\igor\\gdrive\\Code\\revit_scripts\\HeatLossCalc\\')
from models import modelPerimeter, modelRoom

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()

tree = { level.Name : [] for level in levels }
for room in rooms:
	tree[room.Level.Name].append(modelRoom(room))
	
perimeter = modelPerimeter(tree.values())
print(datetime.now().isoformat(), 'succesfully')