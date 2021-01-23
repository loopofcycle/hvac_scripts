import clr, json, os
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

doc = __revit__.ActiveUIDocument.Document
dir, name = os.path.split(doc.PathName)
fam_dir = dir + '\\families'
if not os.path.exists(fam_dir): os.mkdir(fam_dir)

families = {}
equipment = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_MechanicalEquipment).ToElements()
for e in equipment:
    try:
        families[e.Symbol.FamilyName] = e.Symbol.Family
    except:
        families[e.FamilyName] = e.Family

for name, family in families.items():
    fam_path = fam_dir + '\\' + name + '.rfa'
    if os.path.exists(fam_path): os.remove(fam_path)
    famDoc = doc.EditFamily(family)
    famDoc.SaveAs(fam_path)
    print(name)
    print('\t\tunloaded')
print(len(families), ' families unloaded succesfully')