# -*- coding: utf-8 -*-
import clr, json, os
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
os.chdir('C:\\Users\\igor\\Google Диск\\Code\\pyAddParameters\\')
from parameters_manager import ParametersManager

doc = __revit__.ActiveUIDocument.Document
t = Transaction(doc, 'adding parameters')
t.Start()
pm = ParametersManager()
this_family = doc.OwnerFamily
omni_param = this_family.GetParameters('Номер OmniClass')
omni_param = omni_param[0]
omni_param.Set(pm.get_omni_class_num(doc.Title))
print('omni class number is', omni_param.AsString())
parameters_list = pm.get_parameters(doc.Title)
parameters_to_add = []
spf = doc.Application.OpenSharedParameterFile()
for group in spf.Groups:
    for parameter in group.Definitions:
        if parameter.Name in parameters_list:
            parameters_to_add.Add(parameter)

fm = doc.FamilyManager
for parameter in parameters_to_add:
    try:
        fm.AddParameter(parameter, BuiltInParameterGroup.PG_GENERAL, False)
        print(parameter.Name)
        print('\t\tadded')
    except:
        print(parameter.Name)
        print('\t\talready exists in family')
t.Commit()