import cx_Freeze
executables = [cx_Freeze.Executable("Test.py")]

cx_Freeze.setup(
    version = "1.1",
    name="Motherload",
    options={"build_exe":{"packages":["pygame","random","math"],
             "include_files":["Untitled1.wav","Untitled2.wav","Untitled3.wav","Untitled4.wav",
                               "Untitled5.wav","Untitled6.wav","Music.wav","Music2.wav","dolarium1.wav",
                               "dolarium2.wav","dolarium3.wav","dolarium4.wav","Burnt.wav","freesansbold.ttf",
                              "rectangle.jpg"]}},
    executables = executables
    )
