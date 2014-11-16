# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 13:20:48 2014

@author: jpoeppel
"""


import unittest
import kml
import osmData

class TestPlacemarkDistToPolygonObject(unittest.TestCase):
  
  def setUp(self):
    self.testName = "0002"
    self.ruleType = ("key", "value")
    self.nodeList = [osmData.Node(1, 52.12, 4.12, {}), osmData.Node(2, 52.13, 4.12, {}), osmData.Node(3, 52.12, 4.13, {})]
    self.placemarkObj = kml.Placemark(self.testName, self.ruleType, self.nodeList)
    self.testNode = osmData.Node() # TODO fill
    self.testDistance = 0 # TODO

  def test_distToPolygonOutside(self):
    self.assertEqual(self.placemarkObj.distToPolygon(self.testNode), self.testDistance)

  def test_distToPolygonInside(self):
    self.fail()

  def test_distToPolygonBorder(self):
    self.fail()    
    
  def test_distToPolygonFailNoNode(self):

    with self.assertRaises(SystemExit) as errorMessage:
      self.placemarkObj.distToPolygon("asd")
    self.assertEqual(errorMessage.exception.code, -1) 
    
  def test_distToPolygonFailNoPolygon(self):
    secondPlacemarkObj = kml.Placemark(self.test, self.ruleType, self.nodeList[:2])
    self.assertEqual(secondPlacemarkObj.distToPolygon(self.testNode), -3) # TODO error code
    
  
  

if __name__ == '__main__':
  unittest.main()