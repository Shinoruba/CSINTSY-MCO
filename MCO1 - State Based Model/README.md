# CSINTSY_MCO1

## CSINTSY S16 GROUP 1
- CARDINO, JOAQUIN CARLO E. - 12305766
- CLAVANO, ANGELICA THERESE I. (JACK) - 12206245
- HO, DENISE LIANA P. - 12346101
- HOMSSI, YAZAN M. - 12206824
- SANTOS, EMMANUEL GABRIEL D. - 12229105

## How to run the program
0. Install VsCode and Python. The usage of the built-in terminal in VsCode is recommended so that the colors will appear. If you are using Windows Command Prompt, sometimes the color will not appear and it will be replaced with [31m, [32m, etc.
0. Make sure the path to the Python installation is in your System Environment Variables. This can be set at the end of the installation of Python3.
1. Open the terminal (ctrl+` in Visual Studio Code)
2. Type "python --version" to make sure you have Python installed.
3. To run the program, navigate to the path of the Source/ folder. On VsCode, you can right click the folder and click "Open in Integrated Terminal".
4. In the terminal, type "python main.py" and press enter.

# How to use measurement.py
measurement.py is not part of the main program and is only used for testing purposes and for the section regarding time and space complextity. this file uses memory_profiler and big-o installed by pip. If this file is accessed through the main menu of the program, it will most likely not work. If it is able to run, it will run test_random_connection() by default.

If you would like to test random functions, you can uncomment the function calls at the bottom of the file. 

## Installation of memory_profiler and big-o
1. Open the terminal (ctrl+` in Visual Studio Code)
2. Type "pip install memory_profiler" and press enter.
3. Type "pip install big-o" and press enter.
4. Type "pip install matplotlib" and press enter. (needed for memory_profiler)

## Measuring space complexity (memory_profiler)
1. Open the terminal (ctrl+` in Visual Studio Code)
2. Type "mprof run measurement.py" and press enter.
3. Type "mprof plot" and press enter. It should oppen a new window with the graph of the memory usage.

More on memory_profiler: https://coderzcolumn.com/tutorials/python/how-to-profile-memory-usage-in-python-using-memory-profiler
Github: https://github.com/pythonprofilers/memory_profiler

To remove the memory_profiler log files, type "mprof clean" in the terminal.

## Measuring time complexity (big-o)
1. Open the terminal (ctrl+` in Visual Studio Code)
2. Type "py measurement.py" and press enter. It should display the time taken for each function to run in the console. This also includes a full report of the time taken for each function to run.
3. The same thing can be achieved with "mprof run measurement.py"

Github: https://github.com/pberkes/big_O