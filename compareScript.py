# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 11:41:33 2015

@author: jpoeppel
"""

import sys
import os

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print "Usage: %s <ReferenceDirectory> <TestDirectory>" % sys.argv[0]
    sys.exit(1)
    
  refDir = sys.argv[1]
  testDir = sys.argv[2]
  incorrectFiles = []
  for f in os.listdir(refDir):
    
    print "Checking file:", f
    ref = open(refDir + "/" + f,'r')
    refString = ref.read()
    
    test = open(testDir + "/" + f)
    testString = test.read()
    
    if refString != testString:
      incorrectFiles.append(f)
      
  print "Unequal files: ", incorrectFiles