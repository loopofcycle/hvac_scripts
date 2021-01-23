#import libraries and reference the RevitAPI and RevitAPIUI
import clr
import math
import time
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI') 
from Autodesk.Revit.DB import * 
 
#set the active Revit application and document
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document

fec=FilteredElementCollector(doc)
fec.OfCategory(BuiltInCategory.OST_MechanicalEquipment)
fec.OfClass(FamilySymbol)

all_p={}

for element in fec:
	parameters=element.Parameters
	#print('\nFamilySymbol')
	#print(element.FamilyName)
	
	for p in parameters:
		#temp= str.decode(p.Definition.Name, 'unicode-escape')
		p_names=all_p.viewkeys()
		#if p.Definition.Name not in p_names: 
		all_p[p.Definition.Name]=p.Definition
		#print '\t' + temp

#define a transaction variable and describe the transaction
t = Transaction(doc, 'This is my new transaction')

#print(time.gmtime(time.time())[1:-3])
print('executed at -', time.localtime()[1:-3])
#start a transaction in the Revit database
t.Start()
 
#perform some action here...
 
#commit the transaction to the Revit database
t.Commit()