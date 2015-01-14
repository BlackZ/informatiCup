===============================================================================
isySUR
===============================================================================
14/01/2015

-------------------------------------------------------------------------------
General usage
-------------------------------------------------------------------------------

isySUR is a Python script that computes the sphere of influence of space usage
rules which coordinates are given. It comes with a Python package with several
tools.

For the command line version type:
 $ python run_isySUR.py cli {inPath} {outPath}
 
For the GUI version type:
 $ python run_isySUR.py gui
 
When just tiping
 $ python run_isySUR.py
the GUI version is used as default. When GUI could not be loaded, command line
version is used.

For more information about optional and required parameters (cli/gui, inPath,
outPath) check the help parameter (-h) or the manual.

-------------------------------------------------------------------------------
Installation on Linux
-------------------------------------------------------------------------------

Requirements for command line version:
- Python 2.7
- requests (HTTP library)
- internet connection

Further requirements for the GUI verson:
- futures
- Kivy (http://kivy.org)

Because isySUR is in Python you do not need to make an installation. Just
browse into the directory and call the script run_isySUR.py with Python.

For installation you also use Python:
 $ python setup.py install
Afterwards you can call run_isySUR.py from every directory you want and can
import the isySUR package in your own projects.

-------------------------------------------------------------------------------
Further information
-------------------------------------------------------------------------------

For information about the requirements, the installation and usage of the GUI
version and implementation details see the manual.

===============================================================================
Authors
===============================================================================
Adriana-Victoria Dreyer	adreyer@techfak.uni-bielefeld.de
Jacqueline Hemminghaus	jhemming@techfak.uni-bielefeld.de
Jan Pöppel		jpoeppel@techfak.uni-bielefeld.de
Thorsten Schodde	tschodde@techfak.uni-bielefeld.de
===============================================================================
