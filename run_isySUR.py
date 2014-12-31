#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 18:36:46 2014
Main entrance point for the informatiCup program.
Name should change once a final name for the program has been found.
@author: adreyer & jpoeppel
"""

import isySUR.program
import argparse

def parseArguments():
    parser = argparse.ArgumentParser(description='[NAME] to calculate the subjective area of \
          influence of space usage rules (SURs).')
    parser.add_argument('input', type=str,
                        help='Input file containing the SURs which area of influence is to be computed.')
    parser.add_argument('output', type=str,
                        help='Path for the resulting KML(s). If the path points to a file, only one KML \
                          file will be created, containing all calculated areas. If path points to a directory \
                          a KML file for each SUR will be created as well as one containing all areas.')
    return parser.parse_args()

if __name__ == '__main__':
  args = parseArguments()
  isySUR.program.Pipeline().computeKMLs(args.input, args.output)