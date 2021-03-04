import clr
import os
import json
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *


def GetFormatAndOrientation(width, height):
    formats = json.load(open("C:\\Users\\igor\\gdrive\\Code\\revit_scripts\\PrintPDF\\formats.json"))
    for format_name, properties in formats.items():
        if properties['width'] == width and properties['height'] == height:
            return [properties['name'], properties['orientation']]
    return ['not defined', 'not defined']


def PrintSheet(properties):
    doc = __revit__.ActiveUIDocument.Document
    ps = doc.PrintManager.PrintSetup
    t=Transaction(doc,'debug') 
    t.Start()
    ps.SaveAs('debug')
    for setting in sorted(FilteredElementCollector(doc).OfClass(PrintSetting).ToElements()):
        if setting.Name == 'debug':
            ps.CurrentPrintSetting = setting
            print doc.PrintManager.PrintSetup.CurrentPrintSetting.Name

	# code region for making PrintManager.PrintSetup.Save() available
    if ps.CurrentPrintSetting.PrintParameters.PageOrientation == PageOrientationType.Landscape:
        ps.CurrentPrintSetting.PrintParameters.PageOrientation = PageOrientationType.Portrait
    else:
        ps.CurrentPrintSetting.PrintParameters.PageOrientation = PageOrientationType.Landscape

    # end of region
    ps.CurrentPrintSetting.PrintParameters.PageOrientation = PageOrientationType.Landscape
    if properties['orientation'] == 'v':
    	ps.CurrentPrintSetting.PrintParameters.PageOrientation = PageOrientationType.Portrait
    ps.CurrentPrintSetting.PrintParameters.ColorDepth = ColorDepthType.Color
    ps.CurrentPrintSetting.PrintParameters.ZoomType = ZoomType.Zoom
    ps.CurrentPrintSetting.PrintParameters.Zoom = 100
    ps.CurrentPrintSetting.PrintParameters.PaperPlacement = PaperPlacementType.Center
    for size in doc.PrintManager.PaperSizes:
        if properties['format'] == size.Name:
            print('identified format: ', size.Name)
            ps.CurrentPrintSetting.PrintParameters.PaperSize = size
    try:
        ps.Save()
        doc.PrintManager.SubmitPrint(properties['view'])
    finally:
        doc.PrintManager.PrintSetup.Delete()
        t.Commit()
        print properties['title'],'; format -', properties['format'],'; orient.-', properties['orientation']


printer_name = "PDF reDirect v2"
inch_to_mm = 304.8
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
views = sorted(FilteredElementCollector(doc).OfClass(View).ToElements())
sheets = {}
for view in views:
	if view.ViewType == ViewType.DrawingSheet:
		sheets[view.SheetNumber] = {'view': view}
		sheets[view.SheetNumber]['title'] = view.Title
		width = round((view.Outline.Max - view.Outline.Min)[0] * inch_to_mm)
		height = round((view.Outline.Max - view.Outline.Min)[1] * inch_to_mm)
		sheets[view.SheetNumber]['format'] = GetFormatAndOrientation(width, height)[0]
		sheets[view.SheetNumber]['orientation'] = GetFormatAndOrientation(width, height)[1]
for sheet, properties in sorted(sheets.items()): PrintSheet(properties)
__window__.Close()