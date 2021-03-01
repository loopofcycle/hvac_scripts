# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import ViewSchedule, ViewScheduleExportOptions
from Autodesk.Revit.DB import ExportColumnHeaders, ExportTextQualifier
from Autodesk.Revit.DB import BuiltInCategory, ViewSchedule
from Autodesk.Revit.UI import *

import os
import subprocess
txt_merger = 'C:\\Users\\igor\\Google Диск\\Code\\pyExportSchedules\\txt_merger.py'
schedules_merger = 'C:\\Users\\igor\\Google Диск\\Code\\pyExportSchedules\\merge_schedules.py'

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

desktop = os.path.expanduser("~\\Desktop")
vseop = ViewScheduleExportOptions()
spec_name = 'specification.csv'
prefix = 'ОВ.С_'

schedules = []
for schedule in FilteredElementCollector(doc).OfClass(ViewSchedule).ToElements():
	if schedule.Name.StartsWith(prefix): schedules.append(schedule)
		
for schedule in schedules:
	filename = "".join(x for x in schedule.ViewName if x not in ['*']) + '.txt'
	schedule.Export(desktop, filename, vseop)

PYTHON3 = r"C://Users//igor//AppData//Local//Programs//Python//Python38-32"
if os.path.exists(PYTHON3):
	#os.system('start python \"{path}\"'.format(path=schedules_merger))
	print('Done')
