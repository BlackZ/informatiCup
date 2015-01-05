# -*- coding: utf-8 -*-
"""
Created on Mon Jan 05 18:51:36 2015

@author: adreyer
"""

from distutils.core import setup

setup( 
     name = "isyenv", 
     version = "1.0", 
     author = "Adriana-Victoria Dreyer, Jacqueline Hemminghaus, Jan Pöppel, Thorsten Schodde", 
     author_email = "adreyer@techfak.uni-bielefeld.de, jhemming@techfak.uni-bielefeld.de, jpoeppel@techfak.uni-bielefeld.de, tschodde@techfak.uni-bielefeld.de", 
     packages=['isySUR','isySUR.gui','isySUR.gui.mapview'],
     package_dir={'isyenv': 'isyenv'},
     package_data = {"isySUR.gui.mapview" : ["isySUR/gui/mapview/icons/marker.png"]} 
     )

