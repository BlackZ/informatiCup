# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 13:20:21 2014

@author: jpoeppel & adreyer
"""

import unittest
import sur

class TestSurObject(unittest.TestCase):
  
  def setUp(self):
    self.testString =("0001, 50.9304, 5.33901, access:dog=\"no\"")
    self.id = "0001"
    self.lat = 50.9304
    self.long = 5.33901
    self.ruleNameString = "access:dog=\"no\""
    self.ruleName = {"access:dog": "no"}
  
  def test_createSur(self):
    testSur = sur.SUR(self.id, self.ruleNameString, self.lat, self.long)
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
    
  def test_parseSurFromFile(self):
    # set up
    testFile = open('TestData.txt','r')
    ruleName1_2 = {"smoking": "no", "access:dog": "no"}
    id2 = "0002"
    lat2 = 50.9325
    long2 = 5.34174
    ruleName2 = {"cellphone": "no"}
    
    # do it!
    testSurs = sur.SUR.fromFile(testFile)
    
    # check first sur
    self.assertIsNotNone(testSurs)
    self.assertEqual(testSurs[0].id, self.id)
    self.assertEqual(testSurs[0].latitude, self.lat)
    self.assertEqual(testSurs[0].longitude, self.long)
    self.assertEqual(testSurs[0].ruleName, ruleName1_2)
    # check second sur
    self.assertEqual(testSurs[1].id, id2)
    self.assertEqual(testSurs[1].latitude, lat2)
    self.assertEqual(testSurs[1].longitude, long2)
    self.assertEqual(testSurs[1].ruleName, ruleName2)


if __name__ == '__main__':
  unittest.main()
