# coding: utf8
import time, csv, clr
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import Form, Label, ListBox, Button
#clr.AddReference("System.Windows")
#from System.Windows import Point
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, View
from Autodesk.Revit.UI import *
clr.AddReference("RevitServices")
import RevitServices

def dialog_form(views_list=[]):
	form = Form()
	form.AutoSize = True
	lb=ListBox()
	lb.AutoSize = True
	lb.BeginUpdate()
	for view in views_list: lb.Items.Add(view.Title)
	lb.EndUpdate()
	form.Controls.Add(lb)
	#button = Button()
	#button.Location = Point(10,10)
	#form.AcceptButton = button
	form.ShowDialog()
	lb.SetSelected(1, True)
	return lb.SelectedItems[1].ToString() 

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
views = sorted(FilteredElementCollector(doc).OfClass(View).ToElements())
selected_view = dialog_form(views)
for view in views:
	if view.Title == selected_view: uidoc.ActiveView = view