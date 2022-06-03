import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ['tkinter', 'os', 'time', 'csv', 'reportlab', 'locale', 'webbrowser']}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Seet",
        version = "3.6.20",
        description = "Sistema para controle de devolução de peças.",
        options = {"build_exe": build_exe_options},
        executables = [Executable("seet.py", base=base)])