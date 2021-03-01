import time, csv
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

file='C:\Users\Igor\Google Диск\Code\Projects\pyRevit\spaces.csv'
x_max, x_min, y_max, y_min, z_min, z_max = 0,0,0,0,0,0
delta, x_pos, y_pos, z_pos= 9,0,1,2
right, left, up, down, roof, floor ='east','west','north','south','roof','floor'
sqft_sqm, ft_m=0.092903, 0.3048

spaces=FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_MEPSpaces).WhereElementIsNotElementType().ToElements()
lines = FilteredElementCollector(doc).OfClass(CurveElement)

results={}
for space in spaces:
	windows={}
	walls={}
	for line in lines:
		c=line.Location.Curve.GetEndPoint(1)
		if line.LineStyle.Name.ToString()=='windows':
			if space.IsPointInSpace(c): windows[line.LineStyle.Name.ToString()]=int(line.GeometryCurve.Length*304.8)
		if line.LineStyle.Name.ToString()=='<Разделение пространств>':
			if space.IsPointInSpace(c): walls['wall']=int(line.GeometryCurve.Length*304.8)
	if windows: results[space.Id.IntegerValue]={'walls':walls, 'windows':windows}
for k,v in results.items(): print(k,v)	
print(results.Count)
		