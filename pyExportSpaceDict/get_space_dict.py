def find_closest(xyz_point=XYZ(), s=[], d=0, lev_id=0, rad=0, axis=0, forward=True):
	print(lev_id,'at point', xyz_point.ToString())
	closest=False
	limit=rad
	for space in spaces:
		if space.LevelId.IntegerValue==lev_id:
			if forward: space_point=space.get_BoundingBox(doc.ActiveView).Min 
			else: space_point=space.get_BoundingBox(doc.ActiveView).Max
			distance=space_point.DistanceTo(xyz_point)
			#print(space.Number, distance, limit)
			if abs(xyz_point[0]-space_point[0])<d and distance<limit:
				print(xyz_point.ToString(),space_point.ToString(),'d=',xyz_point[0]-space_point[0],space.Number,distance, limit)
				if (xyz_point[axis]<space_point[axis])==forward:
					limit=distance
					closest=space
					#print('bingo', space.Number)
	if closest: print('returned',closest.Number)
	return(closest)

import time, csv
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
file='C:\Users\Igor\Google Диск\Code\Projects\pyRevit\spaces.csv'

spaces, levels, surfaces, spaces_result=[], {}, {}, {}

x_max, x_min, y_max, y_min, z_min, z_max = 0,0,0,0,0,0
radius, delta, x_pos, y_pos, z_pos = 10,9,0,1,2
xyz_min, xyz_max=XYZ(0,0,0), XYZ(0,0,0)
sqft_sqm, ft_m=0.092903, 0.3048

spaces_col=FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_MEPSpaces).WhereElementIsNotElementType().ToElements()
lines = FilteredElementCollector(doc).OfClass(CurveElement).OfCategory(BuiltInCategory.OST_Lines)

for space in spaces_col:
	bb=space.get_BoundingBox(doc.ActiveView)
	if x_max<bb.Max[0]: x_max=bb.Max[0]
	if y_max<bb.Max[1]: y_max=bb.Max[1]
	if z_max<bb.Max[2]: z_max=bb.Max[2]
	if x_min>bb.Min[0]: x_min=bb.Min[0]
	if y_min>bb.Min[1]: y_min=bb.Min[1]
	if z_min>bb.Min[2]: z_min=bb.Min[2]
	levels[space.LevelId.IntegerValue]=space.Level
	spaces.Add(space)

directions={
	'left':['west', x_min, y_min, True, 1],
	'down':['south', x_min, y_min, True, 0],
	'up':['north', x_max, y_max, False, 0],
	#'right':['east', x_max, y_max, False, 1],
	}

for direction, walk in directions.items():
	surfaces[walk[0]]=[]
	for levelid, level in levels.items():
		start=XYZ(walk[1], walk[2], level.Elevation)
		closest=find_closest(xyz_point=start, s=spaces, lev_id=levelid, d=delta, rad=20, forward=walk[3], axis=walk[4])
		while closest:
			current=closest
			surfaces[walk[0]].Add(current)
			if walk[3]: start=current.get_BoundingBox(doc.ActiveView).Min 
			else: start=current.get_BoundingBox(doc.ActiveView).Max
			closest=find_closest(xyz_point=start, s=spaces, lev_id=levelid, d=delta, rad=50, forward=walk[3], axis=walk[4])
		
directions['top']=['-', x_min, y_min, 'forward']
directions['bottom']=['-', x_min, y_min, 'forward']

print('total count of spaces', spaces_result.Count,'executed at - ',time.localtime()[3:-4])