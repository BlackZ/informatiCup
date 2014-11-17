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
    
  def test_distToPolygonFailNoNode(self):
    with self.assertRaises(TypeError):
      self.placemarkObj.distToPolygon("asd")
    
  def test_distToPolygonFailNoPolygon(self):
    secondPlacemarkObj = kml.Placemark(self.testName, self.ruleType, self.nodeList[:2])
    with self.assertRaises(SystemExit) as cm:
      secondPlacemarkObj.distToPolygon(osmData.Node(7,52.123,4.123,{}))
    self.assertEqual(cm.exception.code, -3)

  def test_isPointInsidePolygon_inside(self):
    self.assertTrue(self.placemarkObj._isPointInsidePolygon(52.123,4.12003))
    
  def test_isPointInsidePolygon_outside(self):
    self.assertFalse(self.placemarkObj._isPointInsidePolygon(52.11,4.11))
    
  def test_isPointInsidePolygon_border(self):
    self.assertFalse(self.placemarkObj._isPointInsidePolygon(52.12,4.12))
    
  def test_distPointLine(self):
    trueDist=0.0030000000000001137
    self.assertEqual(self.placemarkObj._distPointLine(52.123,4.123,52.12,4.12,52.13,4.12),trueDist)
    
  def test_distPointLine_border(self):
    trueDist=0.0
    self.assertEqual(self.placemarkObj._distPointLine(52.12,4.12,52.12,4.12,52.13,4.12),trueDist)
  
  def test_distToPolygon_inside(self):
    trueDist=-0.002828427124749019
    self.assertEqual(self.placemarkObj.distToPolygon(osmData.Node(7,52.123,4.123,{})),trueDist)
  
  def test_distToPolygon_outside(self):
    trueDist=0.004242640687119446
    self.assertEqual(self.placemarkObj.distToPolygon(osmData.Node(7,52.117,4.117,{})),trueDist)
  
  def test_distToPolygon_border(self):
    trueDist=0.0
    self.assertEqual(self.placemarkObj.distToPolygon(osmData.Node(7,52.12,4.12,{})),trueDist)

if __name__ == '__main__':
  unittest.main()