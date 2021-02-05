#import libraries and reference the RevitAPI and RevitAPIUI
import time, os, math, json, pprint, clr
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import * 
 
#set the active Revit application and document
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document

ft_to_mm = 304.8

def define_level():
	fec=FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels)
	fec.WhereElementIsNotElementType()
	#for level in fec.ToElements():
		#print(level.LookupParameter('Фасад').AsDouble())
	print('found', len(fec.ToElements()), 'levels')
	return fec.ToElements()

def elevation_as_comment(hole):
	if hole.Name.Contains('в стене'):
		elevation = hole.LookupParameter('Смещение').AsDouble() - hole.LookupParameter('Высота отверстия').AsDouble()
		elevation = str(int(elevation * ft_to_mm))
		result = elevation[:-3] + ',' + elevation[-3:] 
	if hole.Name.Contains('в перекрытии'):
		result = '-'
	return result

fec=FilteredElementCollector(doc)
fec.OfCategory(BuiltInCategory.OST_GenericModel)
fec.OfClass(FamilyInstance)
fec.WhereElementIsNotElementType()
holes = [hole for hole in fec.ToElements() if hole.Name.Contains('Отверстие')]
print('collected:', len(fec.ToElements()), 'holes')

holes_dict = {}
for hole in holes:
	holes_dict[hole] = {}
	holes_dict[hole]['level'] = hole.LevelId 
	holes_dict[hole]['elevation'] = hole.LookupParameter('Смещение').AsDouble()
	holes_dict[hole]['height'] = hole.LookupParameter('Высота отверстия').AsDouble()
	holes_dict[hole]['width'] = hole.LookupParameter('Ширина отверстия').AsDouble()
	if holes_dict[hole]['elevation'] < 0:
		holes_dict[hole]['new level'] = 'call define level'
		holes_dict[hole]['new elevation'] = 'call define elevation'
	else:
		holes_dict[hole]['new level'] = holes_dict[hole]['level'] 
		holes_dict[hole]['new elevation'] = holes_dict[hole]['elevation']
	holes_dict[hole]['comment'] = elevation_as_comment(hole)
	
levels = define_level()
#pprint.pprint(holes_dict, indent=2)

t = Transaction(doc, 'This is my new transaction')
t.Start()
for hole in holes:
	comment = hole.LookupParameter('Комментарии')
	comment.Set(holes_dict[hole]['comment'])
t.Commit()
print('executed at -', time.localtime()[1:-3])