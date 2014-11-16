# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 15:17:08 2014

@author: jpoeppel & adreyer
"""


import unittest
import kml
import osmData

class TestPlacemarkObject(unittest.TestCase):
  
  def setUp(self):
    self.testName = "0002"
    self.ruleType = ("key", "value")
    self.nodeList = [osmData.Node(1, 52.12, 4.12, {}), osmData.Node(2, 52.13, 4.12, {}), osmData.Node(3, 52.12, 4.13, {})]


  def test_createPlacemark(self):  
    placemarkObj = kml.Placemark(self.testName, self.ruleType)
    self.assertIsNotNone(placemarkObj)
    self.assertEqual(placemarkObj.name, self.testName)
    self.assertEqual(placemarkObj.ruleType, self.ruleType)
    self.assertIsNotNone(placemarkObj.polygon)
    self.assertEqual(len(placemarkObj.polygon),0)
    
  def test_createPlacemarkWithPolygon(self):
    placemarkObj = kml.Placemark(self.testName, self.ruleType, self.nodeList)
    self.assertIsNotNone(placemarkObj)
    self.assertEqual(placemarkObj.name, self.testName)
    self.assertEqual(placemarkObj.ruleType, self.ruleType)
    self.assertIsNotNone(placemarkObj.polygon)
    self.assertEqual(len(placemarkObj.polygon),len(self.nodeList))
    
        
  def test_addNode(self):
    placemarkObj = kml.Placemark(self.testName, self.ruleType)
    placemarkObj.addNode(self.nodeList[0])
    self.assertEqual(len(placemarkObj.polygon),1)
    self.assertEqual(placemarkObj.polygon[-1], self.nodeList[0])
    
  def test_addNodeFail(self):
    placemarkObj = kml.Placemark(self.testName, self.ruleType)
    with self.assertRaises(SystemExit) as errorMessage:
      placemarkObj.addNode(self.testName)
    self.assertEqual(errorMessage.exception.code, -1)
    
  def test_hasPolygonFail(self):
    placemarkObj = kml.Placemark(self.testName, self.ruleType)
    self.assertFalse(placemarkObj.hasPolygon())
  
  def test_addNodeList(self):
    self.fail()
  
  def test_hasPolygonWith2Nodes(self):
    placemarkObj = kml.Placemark(self.testName, self.ruleType)
    placemarkObj.addNode(self.nodeList[0])
    placemarkObj.addNode(self.nodeList[1])
    self.assertFalse(placemarkObj.hasPolygon())    
    
  def test_hasPolygon(self):
    placemarkObj = kml.Placemark(self.testName, self.ruleType, self.nodeList)
    self.assertTrue(placemarkObj.hasPolygon())    
  

if __name__ == '__main__':
  unittest.main()