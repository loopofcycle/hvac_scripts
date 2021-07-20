import time, csv, os, clr, json
from pprint import pprint
from datetime import datetime
from System.Collections.Generic import List
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference('RevitServices')

def get_shared_parameters(doc, group_number = '12.'):
	parameters_to_add = []
	spf = doc.Application.OpenSharedParameterFile()
	for group in spf.Groups:
		for parameter in group.Definitions:
			if parameter.OwnerGroup.Name.Contains(group_number):
				parameters_to_add.append(parameter)
	return parameters_to_add

def get_projects_parameters(doc):
	proj_params = {}
	map = doc.ParameterBindings
	iter = map.ForwardIterator()
	iter.Reset()
	while iter.MoveNext():
		proj_params[iter.Key] = iter.Current
		#print(iter.Key.Name)
		#print(iter.Key)
		#print(iter.Current)
		#iter.Key.ParameterGroup = BuiltInParameterGroup.PG_DATA
		#pprint( {'group': iter.Key.ParameterGroup,
		#		'type': iter.Key.ParameterType} )
	
	return proj_params

class ParameterBinder:
	def __init__(self, doc):
		parameters_map = {}	
		with open(doc.PathName.replace('.rvt', '_parameters.json'), 'r') as f:
			parameters_map = json.load(f)

	def get_binding(parameter):
		map = doc.ParameterBindings
		iter = map.ForwardIterator()
		iter.Reset()
		iter.MoveNext()
		binding = iter.Current
		ib = doc.Application.Create.NewInstanceBinding(binding.Categories)
		return ib

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
fn = list(doc.PathName.Split('\\')).pop().Replace('.rvt', None)
sp = get_shared_parameters(doc)
pb = ParameterBinder(doc)

t = Transaction(doc, 'adding parameters')
t.Start()

map = doc.ParameterBindings

for p in sp:
	if map.Contains(p):
		print('\talready in doc.ParameterBindings')
		print(p.Name)
		# map.ReInsert(p, ib, BuiltInParameterGroup.PG_DATA)
	
	if not map.Contains(p):
		print('\tnot in doc.ParameterBindings, inserting')
		print(p.Name)
		
		ib = pb.get_binding()
		map.Insert(p, ib, BuiltInParameterGroup.PG_DATA)

t.Commit()

print(datetime.now().isoformat(), 'succesfully')
