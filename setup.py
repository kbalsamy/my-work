import sys
import os
import platform
from cx_Freeze import setup, Executable


base = None
if sys.platform == 'win32':
    base = 'Win32GUI'


if platform.system() == "Windows":
    PYTHON_DIR = os.path.dirname(os.path.abspath(__file__))
    os.environ['TCL_LIBRARY'] = "C:\\Users\\Karthikeyan\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
    os.environ['TK_LIBRARY'] = "C:\\Users\\Karthikeyan\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"


executables = [Executable('GUI_APP.py', targetName='AmrExtractor.exe', base=base)]


options = {

    'build_exe': {

        'include_files': ['geckodriver.exe', (os.path.join(PYTHON_DIR, 'DLLs', 'tcl86t.dll'), ''),
                          (os.path.join(PYTHON_DIR, 'DLLs', 'tk86t.dll'), ''),
                          (os.path.join(PYTHON_DIR, 'DLLs', 'sqlite3.dll'), '')]

    }

}


setup(name='Amr Extractor',

      version='1.0',

      description='Application',

      executables=executables,

      options=options

      )
