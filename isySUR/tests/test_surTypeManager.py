# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 16:22:04 2014

@author: jpoeppel
"""

import unittest
import os
from isySUR import surTypeManager as stm

class TestsurTypeManager(unittest.TestCase):

  def setUp(self):
    self.testConfigFile = "testData/dataOnlyForTests/testConfig.cfg"
    
  
  def test_createTypeManager(self):
    typeManager = stm.surTypeManager(self.testConfigFile)
    self.assertIsNotNone(typeManager)
    
  def test_createTypeManagerFailNoConfigFileFound(self):
    with self.assertRaises(IOError):
      typeManager = stm.surTypeManager("testData/noConfigFile.cfg")
      
    
  def test_parseConfig(self):
    typeManager = stm.surTypeManager(self.testConfigFile)
    truthDic = {"access:age=\"21+\"": "I", "access:car:lpg=\"no\"": "I", 
                "fishing=\"no\"":"O", "animal_feeding=\"no\"":"IO"}
    self.assertEqual(truthDic, typeManager.ruleTypes)
    
  def test_getSURType(self):
    testRule = "access:age=\"21+\""
    typeManager = stm.surTypeManager(self.testConfigFile)
    self.assertEqual(typeManager.getSURType(testRule), "I")
    
  def test_getSURTypeRuleUnknown(self):
    testRule = "access:age=\"123+\""
    typeManager = stm.surTypeManager(self.testConfigFile)
    self.assertEqual(typeManager.getSURType(testRule), "IO")
    

if __name__ == '__main__':
  os.chdir("../..")
  unittest.main()