import sys
from cx_Freeze import setup, Executable
import os
import platform

base = None

if sys.platform == "win32":
  base = "Win32GUI"

if platform.system() == "Windows":
  PYTHON_DIR = os.path.dirname(os.path.abspath(__file__))
  os.environ['TCL_LIBRARY'] = 'C:\\Users\\home\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6'
  os.environ['TK_LIBRARY'] = 'C:\\Users\\home\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6'


include_files = [('geckodriver.exe'), ('transmission.ico')]
include_files += [(os.path.join(PYTHON_DIR, 'DLLs', 'tcl86t.dll'), ''),
                  (os.path.join(PYTHON_DIR, 'DLLs', 'tk86t.dll'), ''),
                  (os.path.join(PYTHON_DIR, 'DLLs', 'sqlite3.dll'), ''), ]


build_exe_options = {"packages": ['Pmw'], "includes": ["idna.idnadata"], "excludes": [], "include_files": include_files, 'include_msvcr': True, "optimize": 2}


setup(name="AMR Extractor",
      version="1.0",
      description="Automatic EB Meter reading extractor",
      options={"build_exe": build_exe_options},
      executables=[Executable("GUI_APP.py", targetName="AMR.exe", base=base, icon="transmission.ico")])
