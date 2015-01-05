# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 22:59:36 2014

@author: adreyer
"""

from distutils.core import setup

setup( 
     name = "isySUR", 
     version = "1.0", 
     author = "Adriana-Victoria Dreyer, Jacqueline Hemminghaus, Jan Pöppel, Thorsten Schodde", 
     author_email = "adreyer@techfak.uni-bielefeld.de, jhemming@techfak.uni-bielefeld.de, jpoeppel@techfak.uni-bielefeld.de, tschodde@techfak.uni-bielefeld.de", 
     scripts = ["run_isySUR.py"],
     packages = ["isySUR", "isySUR.gui", "isySUR.gui.mapview"],
     package_data = {"isySUR.gui.mapview" : ["./isySUR/gui/mapview/icons/marker.png"]}
     )
