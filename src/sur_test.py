# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 13:20:21 2014

@author: jpoeppel
"""

import unittest
import sur

class TestSurObject(unittest.TestCase):
  
  def setUp(self):
    self.testString =("""0001, 50.9304, 5.33901, access:dog="no" """).strip() #Strip the whitespace at the end
    self.ruleName = ("""access:dog="no" """).strip() #Strip the whitespace at the end
    self.lat = 50.9304
    self.long = 5.33901
    self.id = "0001"
  
  def test_createSur(self):
    testSur = sur.SUR(self.id, self.ruleName, self.lat, self.long)
    self.assertIsNotNone(testSur)
    self.assertEqual(testSur.id, self.id)
    self.assertEqual(testSur.latitude, self.lat)
    self.assertEqual(testSur.longitude, self.long)
    self.assertEqual(testSur.ruleName, self.ruleName)
    
  def test_parseSur(self):
    testSur = sur.SUR.fromString(self.testString)
    self.assertIsNotNone(testSur)
    self.assertEqual(testSur.id, self.id)
    self.assertEqual(testSur.latitude, self.lat)
    self.assertEqual(testSur.longitude, self.long)
    self.assertEqual(testSur.ruleName, self.ruleName)
    

if __name__ == '__main__':
  unittest.main()
