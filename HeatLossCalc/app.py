import time, csv, os, clr
from pprint import pprint
from datetime import datetime
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory 
#from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference('RevitServices')
os.chdir('C:\\Users\\igor\\gdrive\\Code\\revit_scripts\\HeatLossCalc\\')
from models import modelPerimeter, modelRoom

def draw_line(doc, point):
	end_point = XYZ(point.X + 1, point.Y + 2, point.Z)
	t = Transaction(doc, 'drawing line')
	t.Start()
	curve = Line.CreateBound(point, end_point)
	detail_curve = doc.Create.NewDetailCurve(doc.ActiveView, curve)
	t.Commit()

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()

tree = { level.Name : [] for level in levels }
for room in rooms:
	tree[room.Level.Name].append(modelRoom(room))
	
perimeter = modelPerimeter(tree.values())

print('marking all points')
for boundary in perimeter.boundaries.values():
	for level, segment in boundary.segments.items():
		# testing
		if  '-' in level: 
			print('printing points on level', level)
			for point in segment.data.values():
				draw_line(doc, point)

print(datetime.now().isoformat(), 'succesfully')
