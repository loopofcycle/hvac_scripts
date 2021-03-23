# -*- coding: utf-8 -*-
import os
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

txt_merger = 'C:\\Users\\igor\\gdrive\\Code\\revit_scripts\\ExportSchedules\\txt_merger.py'
schedules_merger = 'C:\\Users\\igor\\gdrive\\Code\\revit_scripts\\ExportSchedules\\merge_schedules.py'
desktop = os.path.expanduser("~\\Desktop")
prefix = 'ОВ.С_'
vseop = ViewScheduleExportOptions()

schedules = []
for schedule in FilteredElementCollector(doc).OfClass(ViewSchedule).ToElements():
	if schedule.Name.StartsWith(prefix): schedules.append(schedule)
		
for schedule in schedules:
	filename = "".join(x for x in schedule.ViewName if x not in ['*']) + '.txt'
	schedule.Export(desktop, filename, vseop)

os.system("python {path}".format(path=schedules_merger))
#os.system("python {path}".format(path=txt_merger))
__window__.Close()