import time, csv
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

file='C:\Users\Igor\Google Диск\Code\Projects\pyRevit\spaces.csv'
x_max, x_min, y_max, y_min, z_min, z_max = 0,0,0,0,0,0
delta, x_pos, y_pos, z_pos= 9,0,1,2
right, left, up, down, roof, floor ='east','west','north','south','roof','floor'
sqft_sqm, ft_m=0.092903, 0.3048
n_wall, n_window, ='wall','window'

spaces=FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_MEPSpaces).WhereElementIsNotElementType().ToElements()
lines = FilteredElementCollector(doc).OfClass(CurveElement).OfCategory(BuiltInCategory.OST_Lines)
spaces_result={}

for space in spaces:
	space_bb=space.get_BoundingBox(doc.ActiveView)
	if x_max<space_bb.Max[0]: x_max=space_bb.Max[0]
	if y_max<space_bb.Max[1]: y_max=space_bb.Max[1]
	if z_max<space_bb.Max[2]: z_max=space_bb.Max[2]
	if x_min>space_bb.Min[0]: x_min=space_bb.Min[0]
	if y_min>space_bb.Min[1]: y_min=space_bb.Min[1]
	if z_min>space_bb.Min[2]: z_min=space_bb.Min[2]
	
#region responsible for retrivieng surfaces of space
for space in spaces:
	walls, properties={},{}
	directions={}
	properties.Add('id',space.Id.IntegerValue)
	properties.Add('number',space.LookupParameter('Номер').AsString())
	properties.Add('temp',space.LookupParameter('ADSK_Температура в помещении').AsValueString())
		
	space_bb=space.get_BoundingBox(doc.ActiveView)
			
	#collect walls
	if x_max-space_bb.Max[x_pos]<delta: walls.Add(right,float((space_bb.Max[y_pos]-space_bb.Min[y_pos])*ft_m))
	if y_max-space_bb.Max[y_pos]<delta: walls.Add(up,float((space_bb.Max[x_pos]-space_bb.Min[x_pos])*ft_m))
	if space_bb.Min[x_pos]-x_min<delta: walls.Add(left,float((space_bb.Max[y_pos]-space_bb.Min[y_pos])*ft_m))
	if space_bb.Min[y_pos]-y_min<delta: walls.Add(down,float((space_bb.Max[x_pos]-space_bb.Min[x_pos])*ft_m))
	
	for way, length in walls.items():
		directions[way]=[]
		directions[way].Add({n_wall:length})
	#collect windows
	for line in lines:
		center=(line.GeometryCurve.GetEndPoint(1)+line.GeometryCurve.GetEndPoint(0))/2
		if space.IsPointInSpace(center):
			for way in directions: directions[way].Add({n_window:float(line.GeometryCurve.Length*ft_m)})
	#collect floor and roof
	if z_max-space_bb.Max[z_pos]<delta: directions['-']=[{roof:space.Area*sqft_sqm}]
	if space_bb.Min[z_pos]-z_min<delta: directions['-']=[{floor:space.Area*sqft_sqm}]
	
	if walls:
		properties.Add('directions',directions)
		spaces_result.Add(space.LookupParameter('Номер').AsString(),properties)
#end of region	

spaces_num=sorted(spaces_result)
with open(file, 'wb') as csvfile:
	writer=csv.writer(csvfile, delimiter=';')
	for num in spaces_num:
		r=[spaces_result[num]['number'],spaces_result[num]['id'],spaces_result[num]['temp'],''] # header for each space
		for direction, surfaces in spaces_result[num]['directions'].items():
			r[3]=direction
			for p in surfaces:
				s=[p.keys()[0],'',p.values()[0]]
				if p.keys()[0]==n_window: s=['',p.keys()[0],p.values()[0]]
				writer.writerow([r[0],r[1],r[2],r[3],s[0],s[1],s[2]]) # row for each surface in space
				r=['','','','']
print('total count of spaces', spaces_result.Count,'executed at - ',time.localtime()[3:-4])