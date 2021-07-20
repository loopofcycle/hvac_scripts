import time, csv, os, clr, logging, json
from pprint import pprint
from datetime import datetime
from System.Collections.Generic import List
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference('RevitServices')

def get_elevation(element):
	result = None

	if element.Location.GetType() == LocationPoint:
		result = element.Location.Point.Z
	
	if element.Location.GetType() == LocationCurve:
		midle_of_curve = (element.Location.Curve.GetEndPoint(0) + element.Location.Curve.GetEndPoint(1)) / 2
		result = midle_of_curve.Z

	return result

def get_actual_level_id(element):
	
	def is_allowed(level_name):
		required_levels = {}	
		json_path = doc.PathName.replace('.rvt', '.json')
		with open(json_path, 'r') as f:
				required_levels = json.load(f)	

		return level_name in required_levels.keys()
	
	levels_list = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
	levels = { l.ProjectElevation: l.Id for l in levels_list if is_allowed(l.Name)}

	elev, actual_level_id = sorted(levels.items(), reverse=True).pop()
	for elevation, level_id in sorted(levels.items()):
		if get_elevation(element) > elevation:
			actual_level_id = level_id

	return actual_level_id

def get_elements_of_category(doc, category):
	print('\nprocessing category:')
	print(category)
	elements = FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType().ToElements()
	leveled_elements = dict()
	
	for e in elements:
		
		if e.LevelId.IntegerValue > 0:
			level_id = e.LevelId
		elif e.LevelId.IntegerValue < 0:
			level_id = e.ReferenceLevel.Id

		actual_level_id = get_actual_level_id(e)

		if actual_level_id == level_id:
			#print('--- skipping element', e.Id)
			continue
		
		if actual_level_id != level_id:
			pprint({
					'-': '-',
					'1. element': e.Id,
					'2. level': level_id,
					'3. actual level': actual_level_id,
					})

		if leveled_elements.get(level_id):
			leveled_elements[level_id].append(e)
		else:
			leveled_elements[level_id] = list()
			leveled_elements[level_id].append(e)
			
	# pprint(leveled_elements, depth=2)
	return leveled_elements

def change_level(doc, element):
	
	levels_list = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
	levels = {l.Id: l.ProjectElevation for l in levels_list }
	
	level_param = element.get_Parameter(BuiltInParameter.FAMILY_LEVEL_PARAM)
	new_lvl_id = get_actual_level_id(element)

	if level_param is not None and not level_param.IsReadOnly:
		level_param.Set(new_lvl_id)
	
	curve_level_param = element.get_Parameter(BuiltInParameter.RBS_START_LEVEL_PARAM)
	if curve_level_param is not None and not curve_level_param.IsReadOnly:
		curve_level_param.Set(new_lvl_id)

	new_elevation = get_elevation(element) - levels[new_lvl_id]
	elevation = element.LookupParameter('Отметка от уровня')
	if elevation is not None and not elevation.IsReadOnly:
		print('setting elevation')
		elevation.Set(new_elevation)
	else:
		comment = element.LookupParameter('Комментарии')
		comment.Set(str('level is wrong'))

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

categories = [
				BuiltInCategory.OST_MechanicalEquipment,
				BuiltInCategory.OST_PipeCurves,
				BuiltInCategory.OST_PipeFitting,
				BuiltInCategory.OST_PipeAccessory,
				BuiltInCategory.OST_DuctCurves,
				BuiltInCategory.OST_DuctFitting,
				BuiltInCategory.OST_DuctAccessory,
				BuiltInCategory.OST_DuctTerminal,
			]

with Transaction(doc, 'placement according allowed levels') as t:
	t.Start()
	for category in categories:
		leveled_elements = get_elements_of_category(doc, category)
		for elements in leveled_elements.values():
			for element in elements:
				change_level(doc, element)
	t.Commit()

print(datetime.now().isoformat(), ' done')

