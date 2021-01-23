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
uploaded_families = 0
for name, family in families.items():
    t = Transaction(doc, 'new transaction')
    t.Start()
    fam_path = fam_dir + '\\' + name + '.rfa'
    doc.LoadFamily(fam_path)
    t.Commit()
    print(name)
    print('\t\tuploaded')
    uploaded_families += 1
print(uploaded_families,' families uploaded succesfully')