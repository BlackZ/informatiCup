# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 12:25:34 2014

@author: jpoeppel & adreyer
"""

import unittest
import osmData

class TestWayObject(unittest.TestCase):
  
  def setUp(self):
    self.id = "0001"
    self.refs = ["0001","0002","0003"]
    self.tags = {"highway":"residential","name":"Clipstone Street"}
    
  
  def test_createWay(self):
    testWay = osmData.Way(self.id, self.refs, self.tags)
    self.assertIsNotNone(testWay)
    self.assertEqual(testWay.id, self.id)
    self.assertEqual(testWay.refs, self.refs)
    self.assertEqual(testWay.tags, self.tags)
    
  def test_createWayFail(self):
    testWay = osmData.Way(2, self.refs[0:2], self.tags)
    self.assertNotEqual(testWay.id, self.id)
    self.assertNotEqual(testWay.refs, self.refs)
    self.assertEqual(testWay.tags, self.tags)
    
  def test_createWayWithIntId(self):
    testWay = osmData.Way(int(self.id), self.refs, self.tags)
    self.assertNotEqual(testWay.id, self.id)
    self.assertEqual(testWay.id, "1")
    
  def test_createWayFailNoList(self):
    with self.assertRaises(TypeError):
      testWay = osmData.Way(self.id, "asd", self.tags)
      
  def test_createWayFailNotADictionary(self):
    with self.assertRaises(TypeError):
      testWay = osmData.Way(self.id, self.refs, "a:b")
    
  def test_isWayEqual(self):
    testWay = osmData.Way(self.id, self.refs, self.tags)
    #Deliberatly not using the self variables to make sure it is filled with
    #other objects
    otherWay = osmData.Way("0001", ["0001","0002","0003"], {"highway":"residential","name":"Clipstone Street"})
    
    self.assertEqual(testWay, otherWay)
    
  def test_isWayNotEqual(self):
    testWay = osmData.Way(self.id, self.refs, self.tags)
    #Deliberatly not using the self variables to make sure it is filled with
    #other objects
    otherWay = osmData.Way("0002", ["0001","0002","0003"], {"highway":"residential","name":"Clipstone Street"})
    
    self.assertNotEqual(testWay, otherWay)
  

if __name__ == '__main__':
  unittest.main()
