# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 14:58:31 2014

@author: adreyer & jpoeppel
"""

import unittest
import argparse

def parseArguments():
    print "parseArgs being called"
    parser = argparse.ArgumentParser(description='A script running all the tests present in the current directory.')
    parser.add_argument('-v', '--verbosity', type=int, default=3,
                        help='Verbosity the tests should run with.')
    return parser.parse_args()

if __name__ == '__main__':
  args = parseArguments()
  testLoader = unittest.TestLoader()
  suite = testLoader.discover('.')
  unittest.TextTestRunner(verbosity=args.verbosity).run(suite)