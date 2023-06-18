import cx_Freeze

executables= [cx_Freeze.Executable("railway.py", base=None)]

cx_Freeze.setup(
    name="Railway Management System",
    options={"build_exe" : {"packages":["random", "datetime", "pandas", "tkinter", "mysql.connector", "os"], "include_files":["railway.sql", "tcl86t.dll", "tk86t.dll"]}},
    version="2.4.16",
    description="Railway Management System",
    executables=executables
)

