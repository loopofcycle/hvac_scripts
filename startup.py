# script that is run when Revit starts in the IExternalApplication.Startup event.
try:
    # add your code here
    from RevitPythonShell.RpsRuntime import ExternalCommandAssemblyBuilder
    from Autodesk.Revit.UI import *
    import os, clr
    clr.AddReference('PresentationCore')
    from System.Windows.Media.Imaging import BitmapImage
    from System import Uri
    #insert path to scripts in next line
    appdata = os.getenv('APPDATA')
    hvac_scripts = 'RevitPythonShell\\hvac_scripts\\'
    path_to_scripts = os.path.join(appdata, hvac_scripts)
    if not os.path.exists(path_to_scripts):
        path_to_scripts = os.path.join('C:\\Users\\igor\\gdrive\\Code\\revit_scripts')
    scripts = {
        'PrintPDF':
        {
            'folder': os.path.join(path_to_scripts, 'PrintPDF'),
            'name': r"print_sheets.py",
            'dll': r"RPS_print_sheets.dll",
            'large_img': r"PythonScript32x32.png",
            'small_img': r"PythonScript16x16.png",
            'description': 'print sheets',
            'pb_name': 'pb_PrintPDF'
        },
        'AddParameters':
        {
            'folder': os.path.join(path_to_scripts, 'AddParameters'),
            'name': r"add_parameters.py",
            'dll': r"RPS_add_parameters.dll",
            'large_img': r"PythonScript32x32.png",
            'small_img': r"PythonScript16x16.png",
            'description': 'add parameters',
            'pb_name': 'pb_AddParameters'
        },
        'UnloadFamilies':
        {
            'folder': os.path.join(path_to_scripts, 'UnloadUploadFamilies'),
            'name': r"unload_families.py",
            'dll': r"RPS_unload_families.dll",
            'large_img': r"PythonScript32x32.png",
            'small_img': r"PythonScript16x16.png",
            'description': 'unload families',
            'pb_name': 'pb_unload families'
        },
        'NumerateHoles':
        {
            'folder': os.path.join(path_to_scripts, 'NumerateHoles'),
            'name': r"pyNumerateHoles.py",
            'dll': r"RPS_numerate_holes.dll",
            'large_img': r"PythonScript32x32.png",
            'small_img': r"PythonScript16x16.png",
            'description': 'numerate holes',
            'pb_name': 'pb_numerate holes'
        },
        'SelectView':
        {
            'folder': os.path.join(path_to_scripts, 'SelectView'),
            'name': r"select_view.py",
            'dll': r"RPSAddin_select_view.dll",
            'large_img': r"PythonScript32x32.png",
            'small_img': r"PythonScript16x16.png",
            'description': 'select view',
            'pb_name': 'pb_select view'
        },
        'ExportSchedules':
        {
            'folder': os.path.join(path_to_scripts, 'ExportSchedules'),
            'name': r"export_specification.py",
            'dll': r"RPSAddin_export_specification.dll",
            'large_img': r"PythonScript32x32.png",
            'small_img': r"PythonScript16x16.png",
            'description': 'export schedules',
            'pb_name': 'pb_export schedules'
        },
        'HeatLossCalc':
        {
            'folder': os.path.join(path_to_scripts, 'HeatLossCalc'),
            'name': r"app.py",
            'dll': r"RPSAddin_heatloss_calc.dll",
            'large_img': r"PythonScript32x32.png",
            'small_img': r"PythonScript16x16.png",
            'description': 'heat loss calc',
            'pb_name': 'pb_heat loss calc'
        },
        'ViewCreator':
        {
            'folder': os.path.join(path_to_scripts, 'ViewCreator'),
            'name': r"app.py",
            'dll': r"RPSAddin_view_creator.dll",
            'large_img': r"PythonScript32x32.png",
            'small_img': r"PythonScript16x16.png",
            'description': 'create views',
            'pb_name': 'pb_create views'
        },
        # 'UploadFamilies':
        # {
        #     'folder': r"C:\\Users\\igor\\Google Диск\\Code\\pyUnloadUploadFamilies",
        #     'name': r"upload_families.py",
        #     'dll': r"RPS_upload_families.dll",
        #     'large_img': r"PythonScript32x32.png",
        #     'small_img': r"PythonScript16x16.png",
        #     'description': 'upload families',
        #     'pb_name': 'pb_upload families'
        # },
    }

    panel = __uiControlledApplication__.CreateRibbonPanel('pyHVAC')
    for script, settings in scripts.items():
        PROJECT_FOLDER = settings['folder']
        SCRIPT_PATH = os.path.join(PROJECT_FOLDER, settings['name'])
        DLL_PATH = os.path.join(PROJECT_FOLDER, settings['dll'])
        LARGE_IMG = os.path.join(PROJECT_FOLDER, settings['large_img'])
        SMALL_IMG = os.path.join(PROJECT_FOLDER, settings['small_img'])
        builder = ExternalCommandAssemblyBuilder()
        builder.BuildExternalCommandAssembly(DLL_PATH, {script: SCRIPT_PATH})
        pdb = PushButtonData(settings['pb_name'], settings['description'], DLL_PATH, script)
        pdb.Image = BitmapImage(Uri(SMALL_IMG))
        pdb.LargeImage = BitmapImage(Uri(LARGE_IMG))
        panel.AddItem(pdb)

    __window__.Close()  # closes the window
except:
    import traceback       # note: add a python27 library to your search path first!
    traceback.print_exc()  # helps you debug when things go wrong