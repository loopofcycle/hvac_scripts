import time, csv, os, clr
from pprint import pprint
from datetime import datetime
from System.Collections.Generic import List
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference('RevitServices')

def find_view3d(doc):
	vft = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()
	for view_type in vft:
		if view_type.ViewFamily == ViewFamily.ThreeDimensional:
			return view_type

def create_filter(doc, view, system_name):
	filters = FilteredElementCollector(doc).OfClass(ParameterFilterElement).ToElements()
	filters_names = [filter.Name for filter in filters]

	if system_name not in filters_names:
		categories = List[ElementId]()
		categories.Add(ElementId(BuiltInCategory.OST_DuctAccessory))
		categories.Add(ElementId(BuiltInCategory.OST_DuctFitting))
		categories.Add(ElementId(BuiltInCategory.OST_DuctCurves))
		categories.Add(ElementId(BuiltInCategory.OST_MechanicalEquipment))
		categories.Add(ElementId(BuiltInCategory.OST_DuctTerminal))
		categories.Add(ElementId(BuiltInCategory.OST_DuctInsulations))
		filter = ParameterFilterElement.Create(doc, system_name, categories)

		fam_name_param_id = ElementId(BuiltInParameter.RBS_SYSTEM_NAME_PARAM)
		rules = List[FilterRule]()
		rules.Add(ParameterFilterRuleFactory.CreateNotEqualsRule(fam_name_param_id, system_name, False))
		filter.SetElementFilter(ElementParameterFilter(rules))

	else:
		print(system_name)
		print('filter already exist')
		for existing_filter in filters:
			if system_name == existing_filter.Name:
				filter = existing_filter

	view.AddFilter(filter.Id)
	view.SetFilterVisibility(filter.Id, False)


def set_template(doc, view):
	views = FilteredElementCollector(doc).OfClass(View).ToElements()
	view_templates = [view for view in views if view.IsTemplate]
	
def create_scheme(doc, name, view3dType):
	views_list = FilteredElementCollector(doc).OfClass(View).ToElements()
	views_names = [view.Name for view in views_list]
	
	if name not in views_names:
		t = Transaction(doc, 'creating isometric 3d view')
		t.Start()
		scheme_view = View3D.CreateIsometric(doc, view3dType.Id)
		scheme_view.Name = name
		create_filter(doc, scheme_view, name)
		set_template(doc, scheme_view)
		t.Commit()
	else:
		print(name)
		print('view already exist')

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
view3dType = find_view3d(doc)

duct_systems = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DuctSystem).WhereElementIsNotElementType().ToElements()
for system in duct_systems:
	create_scheme(doc, system.Name, view3dType)

print(datetime.now().isoformat(), 'succesfully')