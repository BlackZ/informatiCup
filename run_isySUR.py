#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main entrance point for the informatiCup program.
"""
#@author: adreyer & jpoeppel


import isySUR.program
import argparse
import sys
import os.path

def parseArguments():
  """
    Function that takes program parameters and checks for required arguments.
  """
  parser = argparse.ArgumentParser(description='isySUR script to calculate \
    the subjective area of influence of space usage rules (SURs).')
  subparsers = parser.add_subparsers(title='Version',
                                     description='Please choose whether to \
                                       start with or without GUI.')
  parser_gui = subparsers.add_parser('gui', help='Start with GUI.')
  parser_gui.set_defaults(func=gui)
  parser_gui.add_argument('-c','--config', type=str, default='',
                        help='Path to config file for SUR classification (indoor, outdoor, both).')
  parser_cli = subparsers.add_parser('cli', help='Start with command-line interface.')
  parser_cli.set_defaults(func=cli)
  parser_cli.add_argument('input', type=str,
                        help='Input file containing the SURs which area of influence is to be computed.')
  parser_cli.add_argument('output', type=str,
                        help='Path for the resulting KML(s). If the path points to a file, only one KML \
                          file will be created, containing all calculated areas. If path points to a directory \
                          a KML file for each SUR will be created as well as one containing all areas.')
  parser_cli.add_argument('-c','--config', type=str, default='',
                        help='Path to config file for SUR classification (indoor, outdoor, both).')
  return parser.parse_args()
  
def gui(args=None):
  """
    Function that starts the gui version of the program. When importing fails,
    a message is printed and dealWithImportError is called.
    
    @param args: the arguments to give to the gui version.
    @type argparse.Namespace
  """
  print type(args)
  mapApp = None
  try:
    sys.argv = ['']
    import isySUR.gui.MapGUI as gui
    if hasattr(args, 'config'):
      mapApp = gui.MapApp(args.config)
    else:
      mapApp = gui.MapApp()
    mapApp.run()
  except ImportError:
    print "GUI could not be loaded. Is kivy installed correctly?"
    dealWithImportError()
  except BaseException:
    if mapApp != None:
      mapApp.on_stop()
    import traceback
    traceback.print_exc()
    sys.exit('Program stopped unexpected!')
  
def dealWithImportError():
  """
    Function that gives a prompt to get the parameters for the cli version
    without sys.argv.
  """
  print "You can still use the command line version. Just give the SUR file and output path. Or type 'exit' to close."
  pathin = raw_input("SUR file: ")
  if (pathin=="exit"):
    sys.exit()
  if not (os.path.isfile(pathin)):
    print "input file does not exist"
    sys.exit()
  pathout = raw_input("Path for output: ")
  if (pathout=="exit"):
    sys.exit()
  if (os.path.exists(args.output) or (os.path.exists(os.path.basename(args.output)))):
    isySUR.program.KMLCalculator().computeKMLsAndStore(pathin, pathout)
  else:
    print "output directory does not exist." 
  
def cli(args):
  """
    Function that starts the command line version of the program.
    
    @param args: the arguments to give to the cli version.
    @type argparse.Namespace
  """
  if os.path.isfile(args.input):
    if (os.path.exists(args.output) or (os.path.exists(os.path.basename(args.output)))):
      isySUR.program.KMLCalculator().computeKMLsAndStore(args.input, args.output, args.config)
    else:
      print "output directory does not exist."
  else:
    print "input file does not exist."

if __name__ == '__main__':
  if (('cli' not in sys.argv) and ('gui' not in sys.argv)):
    gui()
  else:
    args = parseArguments()
    args.func(args)