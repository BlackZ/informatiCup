===============================================================================
isySUR
===============================================================================
14/01/2015

-------------------------------------------------------------------------------
Description
-------------------------------------------------------------------------------
isySUR is a tool to automatically compute the area of application for space
usage rules (SURs). This was developed as part of the informatiCup 2015. 
We would appreciate if you would give us some feedback if this is useful for you.
The Data directory contains the testdata that was provided by the competition.
We were also povided with images of the SUR signs but they were not used in this
program. All provided data can be found here:
http://informaticup.gi.de/fileadmin/testdaten-sur-20102014.zip
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
When GUI could not be loaded, command line version is used.
 
When just tiping
 $ python run_isySUR.py
the GUI version is used as default.

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
version and implementation details see manual in doc/manual.pdf.

===============================================================================
Authors
===============================================================================
Adriana-Victoria Dreyer	adreyer@techfak.uni-bielefeld.de
Jacqueline Hemminghaus	jhemming@techfak.uni-bielefeld.de
Jan Pöppel		jpoeppel@techfak.uni-bielefeld.de
Thorsten Schodde	tschodde@techfak.uni-bielefeld.de
===============================================================================
