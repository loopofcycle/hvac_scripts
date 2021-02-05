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
    path_to_scripts = os.path.abspath(r"C:\\Users\\igor\\Google Диск\\Code\\revit_scripts\\")
    scripts = {
        'PrintPDF':
        {
            'folder': os.path.join(path_to_scripts, 'pyPrintPDF'),
            'name': r"print_sheets.py",
            'dll': r"RPS_print_sheets.dll",
            'large_img': r"PythonScript32x32.png",
            'small_img': r"PythonScript16x16.png",
            'description': 'print sheets',
            'pb_name': 'pb_PrintPDF'
        },
        'AddParameters':
        {
            'folder': os.path.join(path_to_scripts, 'pyAddParameters'),
            'name': r"add_parameters.py",
            'dll': r"RPS_add_parameters.dll",
            'large_img': r"PythonScript32x32.png",
            'small_img': r"PythonScript16x16.png",
            'description': 'add parameters',
            'pb_name': 'pb_AddParameters'
        },
        'UnloadFamilies':
        {
            'folder': os.path.join(path_to_scripts, 'pyUnloadUploadFamilies'),
            'name': r"unload_families.py",
            'dll': r"RPS_unload_families.dll",
            'large_img': r"PythonScript32x32.png",
            'small_img': r"PythonScript16x16.png",
            'description': 'unload families',
            'pb_name': 'pb_unload families'
        },
        'NumerateHoles':
        {
            'folder': os.path.join(path_to_scripts, 'pyNumerateHoles'),
            'name': r"pyNumerateHoles.py",
            'dll': r"RPS_numerate_holes.dll",
            'large_img': r"PythonScript32x32.png",
            'small_img': r"PythonScript16x16.png",
            'description': 'numerate holes',
            'pb_name': 'pb_numerate holes'
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