import clr, json
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

file='C:\Users\Igor\Google Диск\Code\Projects\pyRevit\catalogue.txt'

doc = __revit__.ActiveUIDocument.Document
catalogue={}
if doc.IsFamilyDocument:
	for type in doc.FamilyManager.Types:
		catalogue[type.Name]={}
		for p in doc.FamilyManager.Parameters:
			#catalogue[type.Name][p.Definition.Id.IntegerValue]=type.AsValueString(p)
			catalogue[type.Name][p.Definition.Name]=type.AsValueString(p)
			
for k,v in catalogue.items():
	print '\t\t',k
	for par, value in v.items():
		print par, value
		
#with open(file, 'w') as outfile:
	#json.dump(catalogue, outfile)