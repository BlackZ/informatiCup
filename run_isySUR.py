#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 18:36:46 2014
Main entrance point for the informatiCup program.
Name should change once a final name for the program has been found.
@author: adreyer & jpoeppel
"""

import isySUR.program
import os
import argparse
import sys

def parseArguments():
    parser = argparse.ArgumentParser(description='isySUR script to calculate the subjective area of \
          influence of space usage rules (SURs).')
    parser.add_argument('-in', '--input', type=str,
                        help='Input file containing the SURs which area of influence is to be computed.')
    parser.add_argument('-out', '--output', type=str,
                        help='Path for the resulting KML(s). If the path points to a file, only one KML \
                          file will be created, containing all calculated areas. If path points to a directory \
                          a KML file for each SUR will be created as well as one containing all areas.')
    parser.add_argument('-c','--config', type=str, default='',
                        help='Path to config file for SUR classification (indoor, outdoor, both).')
    parser.add_argument('-g','--gui', action='store_true',
                        help='Starts the Programm with a GUI. Using it with Windows you need to specify \
                             the path to the kivy.bat with the paramenter -kivy.')
    parser.add_argument('--kivy', type=str, default='',
                        help='Specifies the location of the kivy.bat. Only neccessary for windows users.')
    return parser.parse_args()

if __name__ == '__main__':
  args = parseArguments()
  print args.gui
  if not args.gui:
    isySUR.program.Pipeline().computeKMLsAndStore(args.input, args.output, args.config)
  else:
    sys = sys.platform
    if "linux" in sys:
      isySUR.gui.MapGUI.MapApp().run()
    elif "win" in sys:
      try:
        isySUR.gui.MapGUI.MapApp().run()
      except:
        if args.kivy == '':
          raise Exception('Unknown location of kivy.bat!')        
        os.system(args.kivy + " ./isySUR/gui/MapGUI.py")
