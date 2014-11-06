# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 13:20:21 2014

@author: jpoeppel & adreyer
"""

import unittest
import sur

class TestSURObject(unittest.TestCase):
  
  def setUp(self):
    self.testString =("0001, 50.9304, 5.33901, access:dog=\"no\"")
    self.id = "0001"
    self.lat = 50.9304
    self.long = 5.33901
    self.ruleNameString = "access:dog=\"no\""
    self.ruleName = {"access:dog": "no"}
  
  def test_createSUR(self):
    testSUR = sur.SUR(self.id, self.ruleNameString, self.lat, self.long)
    self.assertIsNotNone(testSUR)
    self.assertEqual(testSUR.id, self.id)
    self.assertEqual(testSUR.latitude, self.lat)
    self.assertEqual(testSUR.longitude, self.long)
    self.assertEqual(testSUR.ruleName, self.ruleName)
    
  def test_parseSUR(self):
    testSUR = sur.SUR.fromString(self.testString)
    self.assertIsNotNone(testSUR)
    self.assertEqual(testSUR.id, self.id)
    self.assertEqual(testSUR.latitude, self.lat)
    self.assertEqual(testSUR.longitude, self.long)
    self.assertEqual(testSUR.ruleName, self.ruleName)
    
  def test_parseSURFromFile(self):
    # set up
    testFile = open('../testData/TestData.txt','r')
    ruleName1_2 = {"smoking": "no", "access:dog": "no"}
    id2 = "0002"
    lat2 = 50.9325
    long2 = 5.34174
    ruleName2 = {"cellphone": "no"}
    
    # do it!
    testSURs = sur.SUR.fromFile(testFile)
    
    # check first sur
    self.assertIsNotNone(testSURs)
    self.assertEqual(testSURs[0].id, self.id)
    self.assertEqual(testSURs[0].latitude, self.lat)
    self.assertEqual(testSURs[0].longitude, self.long)
    self.assertEqual(testSURs[0].ruleName, ruleName1_2)
    # check second sur
    self.assertEqual(testSURs[1].id, id2)
    self.assertEqual(testSURs[1].latitude, lat2)
    self.assertEqual(testSURs[1].longitude, long2)
    self.assertEqual(testSURs[1].ruleName, ruleName2)


if __name__ == '__main__':
  unittest.main()
