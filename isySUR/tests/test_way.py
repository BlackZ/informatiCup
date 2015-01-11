# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 12:25:34 2014

@author: jpoeppel & adreyer
"""

import unittest
from isySUR import osmData

class TestWayObject(unittest.TestCase):
  
  def setUp(self):
    self.id = "0001"
    self.refs = ["0001","0002","0003"]
    self.tags = {"highway":"residential","name":"Clipstone Street"}
    self.testOSM=osmData.OSM()
    self.testOSM.addNodeList([osmData.Node(1, 52.12, 4.12, {}),
                               osmData.Node(2, 52.13, 4.12,{}),
                               osmData.Node(3, 52.12, 4.13, {})])

    self.testWay = osmData.Way(1, [1,2,3,1], {"highway":"residential","name":"Clipstone Street"},self.testOSM)
    self.testWay2 = osmData.Way(2, [1,2], {"highway":"residential","name":"Clipstone Street"},self.testOSM)
    self.testWay3 = osmData.Way(3, [1,2,3,4], {"highway":"residential","name":"Clipstone Street"},self.testOSM)
    self.testOSM.addWay(self.testWay)
    self.testOSM.addWay(self.testWay2)
    self.testOSM.addWay(self.testWay3)
    
    self.wayType=self.testOSM.ways[1].__class__
    self.nodeType=self.testOSM.nodes[1].__class__
  
  def test_verticies(self):
    trueList=[(52.12, 4.12),(52.13, 4.12),(52.12, 4.13),(52.12, 4.12)]
    self.assertEqual(self.testWay._vertices(),trueList)
  
  #============================================================
  #hasPolygon()-Tests
  #============================================================
  def test_isPolygon(self):
    self.assertTrue(self.testWay.isPolygon())
  
  def test_isPolygon_notEnoughPoints(self):
    self.assertFalse(self.testWay2.isPolygon())
  
  def test_isPolygon_notClosed(self):
    self.assertFalse(self.testWay3.isPolygon())
  #============================================================
  
  
  #============================================================
  #isInside()-Tests
  #============================================================  
  def test_isInside_inside(self):
    self.assertTrue(self.testWay.isInside((52.123,4.12003)))
    
  def test_isInside_outside(self):
    self.assertFalse(self.testWay.isInside((52.11,4.11)))
    
  def test_isInside_border(self):
    self.assertTrue(self.testWay.isInside((52.12,4.12)))
  #============================================================
  
  
  #============================================================
  #getDistance()-Tests
  #============================================================  
  def test_getDistanceFailNoTupel(self):
    with self.assertRaises(TypeError):
      self.testWay.getDistance("asd")
      
  def test_getDistance_inside(self):
    trueObj=osmData.distanceResult(0.00282843,(self.testWay.id,self.testWay.__class__),[([(52.13, 4.12), (52.12, 4.13)],self.nodeType)])
    result=self.testWay.getDistance((52.123,4.123))
    self.assertEqual(result.distance,trueObj.distance)
    self.assertEqual(result.nearestObj,trueObj.nearestObj)
    self.assertEqual(result.nearestSubObj,trueObj.nearestSubObj)
  
  def test_getDistance_outside(self):
    trueObj=osmData.distanceResult(0.00424264,(self.testWay.id,self.testWay.__class__),[([(52.12, 4.12), (52.13, 4.12)],self.nodeType),([(52.12, 4.13), (52.12, 4.12)], self.nodeType)])
    result=self.testWay.getDistance((52.117,4.117))
    self.assertEqual(result.distance,trueObj.distance)
    self.assertEqual(result.nearestObj,trueObj.nearestObj)
    self.assertEqual(result.nearestSubObj,trueObj.nearestSubObj)
  
  def test_getDistance_border(self):
    trueObj=osmData.distanceResult(0.0,(self.testWay.id,self.testWay.__class__),[([(52.12, 4.12), (52.13, 4.12)],self.nodeType),([(52.12, 4.13), (52.12, 4.12)], self.nodeType)])
    result=self.testWay.getDistance((52.12,4.12))
    self.assertEqual(result.distance,trueObj.distance)
    self.assertEqual(result.nearestObj,trueObj.nearestObj)
    self.assertEqual(result.nearestSubObj,trueObj.nearestSubObj)
  #============================================================


  #============================================================
  #_distPointLine()-Tests
  #============================================================ 
  def test_distPointLine(self):
    trueDist=2.23606798
    self.assertEqual(self.testWay._distPointLine(3.0,3.0,1.0,1.0,2.0,1.0),trueDist)
    
  def test_distPointLine_border(self):
    trueDist=0.0
    self.assertEqual(self.testWay._distPointLine(52.12,4.12,52.12,4.12,52.13,4.12),trueDist)
  #============================================================

  
  def test_sides(self):
    trueList=[[(52.12, 4.12),(52.13, 4.12)],[(52.13, 4.12),(52.12, 4.13)],[(52.12, 4.13),(52.12, 4.12)]]
    self.assertEqual(self.testWay._sides(),trueList)
  
  def test_createWay(self):
    testWay = osmData.Way(self.id, self.refs, self.tags,self.testOSM)
    self.assertIsNotNone(testWay)
    self.assertEqual(testWay.id, self.id)
    self.assertEqual(testWay.refs, self.refs)
    self.assertEqual(testWay.tags, self.tags)
    self.assertEqual(testWay.osmObj, self.testOSM)
    
  def test_createWayFail(self):
    testWay = osmData.Way(2, self.refs[0:2], self.tags,self.testOSM)
    self.assertNotEqual(testWay.id, self.id)
    self.assertNotEqual(testWay.refs, self.refs)
    self.assertEqual(testWay.tags, self.tags)
    self.assertEqual(testWay.osmObj, self.testOSM)
    
  def test_createWayWithIntId(self):
    testWay = osmData.Way(int(self.id), self.refs, self.tags,self.testOSM)
    self.assertEqual(testWay.id, int(self.id))
    self.assertNotEqual(testWay.id, "1")
    
    
  def test_createWayFailNoList(self):
    with self.assertRaises(TypeError):
      testWay = osmData.Way(self.id, "asd", self.tags,self.testOSM)
      
  def test_createWayFailNotADictionary(self):
    with self.assertRaises(TypeError):
      testWay = osmData.Way(self.id, self.refs, "a:b",self.testOSM)
    
  def test_isWayEqual(self):
    testWay = osmData.Way(self.id, self.refs, self.tags,self.testOSM)
    #Deliberatly not using the self variables to make sure it is filled with
    #other objects
    otherWay = osmData.Way("0001", ["0001","0002","0003"], {"highway":"residential","name":"Clipstone Street"},self.testOSM)
    
    self.assertEqual(testWay, otherWay)
    
  def test_isWayNotEqual(self):
    testWay = osmData.Way(self.id, self.refs, self.tags,self.testOSM)
    #Deliberatly not using the self variables to make sure it is filled with
    #other objects
    otherOSM = osmData.OSM()
    otherWay = osmData.Way("0002", ["0001","0002","0003"], {"highway":"residential","name":"Clipstone Street"}, otherOSM)
    
    self.assertNotEqual(testWay, otherWay)
  

if __name__ == '__main__':
  unittest.main()
