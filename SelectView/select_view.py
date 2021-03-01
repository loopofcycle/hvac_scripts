# coding: utf8
import time, csv, clr, os, subprocess
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

def get_views(doc):
	all_views = sorted(FilteredElementCollector(doc).OfClass(View).ToElements())
	views = [] 
	for view in all_views:
		if view.GetTypeId().IntegerValue > 0:
			views.append(view)
	return views

def views_as_args(views):
	args = "'"
	for view in views:
		args += '"' + view.Name + '" '
	args += "'"
	return args

def show_dialog(args):
	dialog_window = 'C:\dialog_window.py'
	output = subprocess.check_output("python {path} {args}".format(path=dialog_window, args=args))
	return output

def activate_selected_view(uidoc, views, view_name):
	for view in views:
		if view.Name == view_name:
			uidoc.ActiveView = view

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
views = get_views(doc)
args = views_as_args(views)
selected_view_number = show_dialog(args)
view_name = views[int(selected_view_number)].Name
activate_selected_view(uidoc, views, view_name)
__window__.Close()