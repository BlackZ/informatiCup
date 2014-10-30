# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 13:20:21 2014

@author: jpoeppel
"""

import unittest
import sur

class TestSurObject(unittest.TestCase):
  
  def setUp(self):
    self.ruleName = "smoking=no"
    self.lat = 61.35274
    self.long = 48.24532
    self.id = "0001"
  
  def test_createSur(self):
    testSur = sur.SUR(self.id, self.ruleName, self.lat, self.long)
    assertIsNotNone(testSur)
    

if __name__ == '__main__':
  unittest.main()
