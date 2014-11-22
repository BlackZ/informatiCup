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
    self.testWay = osmData.Way(3, [1,2,3,1], {"highway":"residential","name":"Clipstone Street"})
    self.testWay2 = osmData.Way(3, [1,2], {"highway":"residential","name":"Clipstone Street"})
    self.testWay3 = osmData.Way(3, [1,2,3,4], {"highway":"residential","name":"Clipstone Street"})
    self.testVertices=[(52.12, 4.12),(52.13, 4.12),(52.12, 4.13),(52.12, 4.12)]
  
  def test_hasPolygon(self):
    self.assertTrue(self.testWay.hasPolygon())
  
  def test_hasPolygon_notEnoughPoints(self):
    self.assertFalse(self.testWay2.hasPolygon())
  
  def test_hasPolygon_notClosed(self):
    self.assertFalse(self.testWay3.hasPolygon())
  
  def test_distToPolygonFailNoTypel(self):
    with self.assertRaises(TypeError):
      self.testWay.distToPolygon("asd")
    
  def test_distToPolygonFailNoPolygon(self):
    self.assertEqual(self.testWay2.distToPolygon((52.123,4.123),self.testVertices), -2)

  def test_isPointInsidePolygon_inside(self):
    self.assertTrue(self.testWay._isPointInsidePolygon((52.123,4.12003),self.testVertices))
    
  def test_isPointInsidePolygon_outside(self):
    self.assertFalse(self.testWay._isPointInsidePolygon((52.11,4.11),self.testVertices))
    
  def test_isPointInsidePolygon_border(self):
    self.assertFalse(self.testWay._isPointInsidePolygon((52.12,4.12),self.testVertices))
    
  def test_distPointLine(self):
    trueDist=0.0030000000000001137
    self.assertEqual(self.testWay._distPointLine(52.123,4.123,52.12,4.12,52.13,4.12),trueDist)
    
  def test_distPointLine_border(self):
    trueDist=0.0
    self.assertEqual(self.testWay._distPointLine(52.12,4.12,52.12,4.12,52.13,4.12),trueDist)
  
  def test_distToPolygon_inside(self):
    trueDist=-1.0
    self.assertEqual(self.testWay.distToPolygon((52.123,4.123),self.testVertices),trueDist)
  
  def test_distToPolygon_outside(self):
    trueDist=0.004242640687119446
    self.assertEqual(self.testWay.distToPolygon((52.117,4.117),self.testVertices),trueDist)
  
  def test_distToPolygon_border(self):
    trueDist=0.0
    self.assertEqual(self.testWay.distToPolygon((52.12,4.12),self.testVertices),trueDist)
  
  def test_sides(self):
    trueList=[[(52.12, 4.12),(52.13, 4.12)],[(52.13, 4.12),(52.12, 4.13)],[(52.12, 4.13),(52.12, 4.12)]]
    self.assertEqual(self.testWay._sides(self.testVertices),trueList)
  
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
