import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["pygame", "random", "math"],
                     "excludes": ["numpy", "pytz", "asyncio", "concurrent", "ctypes", "distutils", "email", "html",
                                  "http", "json", "logging", "multiprocessing", "neat", "pkg_resources", "pydoc_data",
                                  "test", "tkinter", "unittest", "urllib", "xmlrpc"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="MeteorDestroyer",
    options={"build_exe": build_exe_options},
    version="1.0",
    description='David Lu',
    executables=[Executable("MeteorDestroyer.py", base=base, icon='data\\meteor.ico')]
)




