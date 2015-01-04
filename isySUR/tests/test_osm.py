# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 11:46:54 2014

@author: jpoeppel & adreyer
"""

import unittest
from isySUR import osmData
from isySUR import osmAPI
import sys

class TestOSMObject(unittest.TestCase):
  
  def setUp(self):
    self.testOSM = osmData.OSM()
    self.testNode = osmData.Node(1, 0.1, 2.1, {"highway":"traffic_signals"})
    self.testRelation=osmData.Relation(5, [("way",1,"outer"),("way",2,"inner")], 
                                       {"name":"Tween Pond", "natural":"water"},self.testOSM)
    self.testOSM.addRelation(self.testRelation)

    
    self.testOSM2=osmData.OSM()
    self.testWay = osmData.Way(3, [1,2,3,1], {"highway":"residential",
                                              "name":"Clipstone Street"},self.testOSM2)
    self.testOSM2.addNodeList([osmData.Node(1, 52.12, 4.12, {}),
                               osmData.Node(2, 52.13, 4.12,{}),
                               osmData.Node(3, 52.12, 4.13, {})])
    self.testOSM2.addWay(self.testWay)
    self.testOSM2.addRelation(osmData.Relation(1, [("way", 3, "outer")], {"boundary":"postal_code","type":"boundary", "postal_code":"33615"},self.testOSM2))

    #Test Point for Nearest Functions
    self.testPoint = (2.0,1.0)
    self.testPoint2 = (15.0,15.0)
    self.testPoint3= (4.0, 2.0)
    
    
    #Nearest Poly Function Variables
    self.testOSM3 = osmData.OSM()
    self.testOSM3.addNodeList([osmData.Node(1, 6, 3, {}),
                               osmData.Node(2, 8, 1, {}),
                               osmData.Node(3, 10, 3, {}),
                               osmData.Node(4, 10, 7, {}),
                               osmData.Node(5, 2, 3, {}),
                               osmData.Node(6, 5, 8, {}),
                               osmData.Node(7, 2, 10, {}),
                               osmData.Node(8, 5, 6, {})])
    self.testOSM3.addWay(osmData.Way(1,[1,2,3,4,1],{"testTag":"testValue"},self.testOSM3))
    self.testOSM3.addWay(osmData.Way(2,[5,8,7],{},self.testOSM3))
    self.testOSM3.addWay(osmData.Way(3,[5,6,7,5],{},self.testOSM3))
    
    #Nearest Poly (fail)/Node Function Variables
    self.testOSM4 = osmData.OSM()
    self.testOSM4.addNodeList([osmData.Node(1, 6.0, 3.0, {}),
                               osmData.Node(2, 8.0, 1.0, {"testTag":"testValue"}),
                               osmData.Node(3, 10.0, 3.0, {"testTag":"testValue"}),
                               osmData.Node(4, 10.0, 7.0, {})])
    self.testOSM4.addWay(osmData.Way(1, [1,2],{},self.testOSM4))
    self.testOSM4.addWay(osmData.Way(2, [3,4],{},self.testOSM4))
    
    #Nearest Relation Variables
    self.testOSM5 = osmData.OSM()
    self.testOSM5.addNodeList([osmData.Node(1, 0, 0, {}),
                           osmData.Node(2, 0, 4, {}),
                           osmData.Node(3, 4, 4, {}),
                           osmData.Node(4, 4, 0, {}),
                           osmData.Node(5, 2, 2, {}),
                           osmData.Node(6, 2, 3, {}),
                           osmData.Node(7, 3, 3, {}),
                           osmData.Node(8, 3, 2, {}),
                           osmData.Node(20, 2.2, 2.2, {}),
                           osmData.Node(21, 2.2, 2.8, {}),
                           osmData.Node(22, 2.8, 2.8, {}),
                           osmData.Node(23, 2.8, 2.2, {})])
    self.testOSM5.addWay(osmData.Way(1, [1,2,3,4,1],{},self.testOSM5))
    self.testOSM5.addWay(osmData.Way(2, [5,6,7,8,5],{},self.testOSM5))
    self.testOSM5.addWay(osmData.Way(7, [20,21,22,23,20],{},self.testOSM5))
    self.testOSM5.addRelation(osmData.Relation(1, [("way",1,"outer"),("way",2,"inner"),("way",7,"outer")], 
                                       {"name":"Tween", "natural":"water", "type":"multipolygon"},self.testOSM5))
    
    self.testOSM5.addNodeList([osmData.Node(9, 8, 8, {}),
                           osmData.Node(10, 8, 9, {}),
                           osmData.Node(11, 9, 9, {}),
                           osmData.Node(12, 9, 8, {}),
                           osmData.Node(13, 9, 10, {}),
                           osmData.Node(14, 10, 10, {}),
                           osmData.Node(15, 10, 8, {})])
    self.testOSM5.addWay(osmData.Way(3, [9,10,11,12,9],{},self.testOSM5))
    self.testOSM5.addWay(osmData.Way(4, [11,13,14,15,11],{},self.testOSM5))
    self.testOSM5.addRelation(osmData.Relation(2, [("way",3,"outer"),("way",4,"outer")], 
                                       {"name":"Tween Pond", "natural":"water","type":"multipolygon"},self.testOSM5))
    
    self.testOSM5.addNodeList([osmData.Node(16, 8, 8, {}),
                           osmData.Node(17, 8, 9, {}),
                           osmData.Node(18, 9, 9, {}),
                           osmData.Node(19, 9, 8, {})])
    self.testOSM5.addWay(osmData.Way(5, [16,17],{},self.testOSM5))
    self.testOSM5.addWay(osmData.Way(6, [18,19],{},self.testOSM5))
    self.testOSM5.addRelation(osmData.Relation(3, [("way",5,"road"),("way",6,"road")], 
                                       {"name":"Tween Pond", "natural":"water","type":"route"},self.testOSM5))
    
    #OSM for Poly in Poly with multiple Ways
    self.testOSM6 = osmData.OSM()
    self.testOSM6.addNodeList([osmData.Node(1, 4, 0, {}),
                               osmData.Node(2, 8, 3, {}),
                               osmData.Node(3, 7, 7, {}),
                               osmData.Node(4, 3, 9, {}),
                               osmData.Node(5, 0, 4, {}),
                               osmData.Node(6, 2, 5, {}),
                               osmData.Node(7, 5, 7, {}),
                               osmData.Node(8, 6, 5, {}),
                               osmData.Node(9, 5, 2, {}),
                               osmData.Node(10, 3, 2, {})])
    
    self.testOSM6.addWay(osmData.Way(1, [1, 2, 3], {},self.testOSM6))
    self.testOSM6.addWay(osmData.Way(2, [3, 4], {},self.testOSM6))
    self.testOSM6.addWay(osmData.Way(5, [4, 5, 1], {},self.testOSM6))
    self.testOSM6.addWay(osmData.Way(3, [6, 7, 8], {},self.testOSM6))
    self.testOSM6.addWay(osmData.Way(4, [8, 9, 10, 6], {},self.testOSM6))
    self.testOSM6.addWay(osmData.Way(6, [1, 2], {},self.testOSM6))
    self.testOSM6.addWay(osmData.Way(7, [2, 3, 1], {},self.testOSM6))
    
    self.testOSM6.addRelation(osmData.Relation(1,
                                               [("way", 1, "outer"),("way", 2, "outer"),("way", 5, "outer"),("way", 3, "inner"), ("way", 4, "inner"),("way", 6, "inner"),("way", 7, "outer") ],
                                               {"type":"multipolygon"},self.testOSM6))
    
    #OSM with Poly in Poly in Poly
    self.testOSM7 = osmData.OSM()
    self.testOSM7.addNodeList([osmData.Node(1, 4, 0, {}),
                               osmData.Node(2, 8, 3, {}),
                               osmData.Node(3, 7, 7, {}),
                               osmData.Node(4, 3, 9, {}),
                               osmData.Node(5, 0, 4, {}),
                               osmData.Node(6, 2, 5, {}),
                               osmData.Node(7, 5, 7, {}),
                               osmData.Node(8, 6, 5, {}),
                               osmData.Node(9, 5, 2, {}),
                               osmData.Node(10, 3, 2, {}),
                               osmData.Node(11, 4, 3, {}),
                               osmData.Node(12, 5, 4, {}),
                               osmData.Node(13, 3, 5, {})])
    
    self.testOSM7.addWay(osmData.Way(1, [1, 2, 3], {},self.testOSM7))
    self.testOSM7.addWay(osmData.Way(2, [3, 4], {},self.testOSM7))
    self.testOSM7.addWay(osmData.Way(5, [4, 5, 1], {},self.testOSM7))
    self.testOSM7.addWay(osmData.Way(3, [6, 7, 8], {},self.testOSM7))
    self.testOSM7.addWay(osmData.Way(4, [8, 9, 10, 6], {},self.testOSM7))
    self.testOSM7.addWay(osmData.Way(6, [1, 2], {},self.testOSM7))
    self.testOSM7.addWay(osmData.Way(7, [2, 3, 1], {},self.testOSM7))
    self.testOSM7.addWay(osmData.Way(5, [11, 12, 13, 11], {},self.testOSM7))
    
    self.testOSM7.addRelation(osmData.Relation(1,
                                               [("way", 1, "outer"),("way", 2, "outer"),("way", 3, "inner"), ("way", 4, "inner"), ("way", 5, "outer")],
                                               {"type":"multipolygon"},self.testOSM7))
    
    #Site Relation
    self.testOSM8 = osmData.OSM()
    self.testOSM8.addNodeList([osmData.Node(1, 4, 0, {}),
                               osmData.Node(2, 8, 3, {}),
                               osmData.Node(3, 7, 7, {}),
                               osmData.Node(4, 3, 9, {}),
                               osmData.Node(5, 0, 4, {}),
                               osmData.Node(6, 2, 5, {}),
                               osmData.Node(7, 5, 7, {}),
                               osmData.Node(8, 6, 5, {}),
                               osmData.Node(9, 5, 2, {}),
                               osmData.Node(10, 3, 2, {}),
                               osmData.Node(11, 0, 0, {}),
                               osmData.Node(12, 1, 0, {}),
                               osmData.Node(13, 0, -1, {})])
    
    self.testOSM8.addWay(osmData.Way(1, [1, 2, 3], {},self.testOSM8))
    self.testOSM8.addWay(osmData.Way(2, [3, 4], {},self.testOSM8))
    self.testOSM8.addWay(osmData.Way(5, [4, 5, 1], {},self.testOSM8))
    self.testOSM8.addWay(osmData.Way(3, [6, 7, 8], {},self.testOSM8))
    self.testOSM8.addWay(osmData.Way(4, [8, 9, 10, 6], {},self.testOSM8))
    self.testOSM8.addWay(osmData.Way(6, [1, 2], {},self.testOSM8))
    self.testOSM8.addWay(osmData.Way(7, [2, 3, 1], {},self.testOSM8))
    self.testOSM8.addWay(osmData.Way(8, [11, 12, 13, 11], {},self.testOSM8))
    
    self.testOSM8.addRelation(osmData.Relation(1,
                                               [("way", 1, "outer"),("way", 2, "outer"),("way", 3, "inner"), ("way", 4, "inner"), ("way", 5, "outer")],
                                               {"type":"multipolygon"},self.testOSM8))
    self.testOSM8.addRelation(osmData.Relation(2,
                                               [("way", 8, "outer"),("relation", 1, "parking")],
                                               {"type":"site"},self.testOSM8))
    self.testOSM8.addRelation(osmData.Relation(3,
                                               [("way", 8, "outer"),("relation", 1, "parking")],
                                               {"type":"site"},self.testOSM8))
    

    
    self.nodeType=self.testOSM8.nodes[1].__class__
    self.wayType=self.testOSM8.ways[8].__class__
    self.relType=self.testOSM8.relations[1].__class__
    
    self.api = osmAPI.osmAPI()
  
  
  #========================================================
  #Tests for getNearestNode
  #========================================================
  def test_getNearestNode(self):
    nearestPoint=[osmData.distanceResult(4.47213595,(1,self.nodeType))]
    result=self.testOSM4.getNearestNode(self.testPoint)
    self.assertEqual(nearestPoint[0].nearestObj, result[0].nearestObj)
    self.assertEqual(nearestPoint[0].distance, result[0].distance)
    self.assertEqual(nearestPoint[0].nearestSubObj, result[0].nearestSubObj)
    self.assertEqual(len(nearestPoint),1)
  
  def test_getNearestNodeWithTagFilter(self):
    nearestPoint = [osmData.distanceResult(6.0,(2,self.nodeType))]
    result=self.testOSM4.getNearestNode(self.testPoint, {"testTag":"testValue"})
    self.assertEqual(nearestPoint[0].nearestObj, result[0].nearestObj)
    self.assertEqual(nearestPoint[0].distance, result[0].distance)
    self.assertEqual(nearestPoint[0].nearestSubObj, result[0].nearestSubObj)
    self.assertEqual(len(nearestPoint),1)
    
  def test_getNearestNodeWithTagFilterWildcard(self):
    nearestPoint = [osmData.distanceResult(6.0,(2,self.nodeType))]
    result=self.testOSM4.getNearestNode(self.testPoint, {"testTag":"*"})
    self.assertEqual(nearestPoint[0].nearestObj, result[0].nearestObj)
    self.assertEqual(nearestPoint[0].distance, result[0].distance)
    self.assertEqual(nearestPoint[0].nearestSubObj, result[0].nearestSubObj)
    self.assertEqual(len(nearestPoint),1)
    
  def test_getNearestNodeWithTagFilterWildcardWrong(self):
    nearestPoint = [osmData.distanceResult(4.47213595,(1,self.nodeType))]
    result=self.testOSM4.getNearestNode(self.testPoint, {"*":"*"})
    self.assertEqual(nearestPoint[0].nearestObj, result[0].nearestObj)
    self.assertEqual(nearestPoint[0].distance, result[0].distance)
    self.assertEqual(nearestPoint[0].nearestSubObj, result[0].nearestSubObj)
    self.assertEqual(len(nearestPoint),1)
    
  def test_getNearestNodeFailWithTagFilter(self):
    with self.assertRaises(TypeError):
      self.testOSM4.getNearestNode(self.testPoint, "asd")
  
  def test_getNearestNodeFail(self):
    with self.assertRaises(TypeError):
      self.testOSM4.getNearestNode((1,0))
      
  def test_getNearestNodeFailPoint(self):
    with self.assertRaises(TypeError):
      self.testOSM3.getNearestNode((1,0),True)

  def test_getNearestNodeFailFilter(self):
    with self.assertRaises(TypeError):
      self.testOSM3.getNearestNode(self.testPoint,True,"asd")
  
  def test_getNearestNodeNothingFound(self):
    result=self.testOSM4.getNearestNode(self.testPoint, {"asd":"asd"})
    self.assertEqual(len(result),0)
  #========================================================


  #========================================================
  #Tests for getNearestRelation
  #========================================================
  def test_getNearestRelationProblem(self):
    point = (50.9262, 5.3968)
    bBox = [50.92575, 5.396042, 50.92665, 5.397558]
    testData = self.api.performRequest(bBox)
    res = testData.getNearestRelation(point)
    #In the list of nearestSubObjects should not be dublicates
    self.assertTrue(len(res[0].nearestSubObj)==len(set(res[0].nearestSubObj)))
  
  
  def test_getNearestRelation(self):
    nearestRelation = [osmData.distanceResult(7.07106781,(2,self.relType),[(4,self.wayType)])]
    
    result=self.testOSM5.getNearestRelation(self.testPoint2)
    self.assertEqual(nearestRelation[0].nearestObj, result[0].nearestObj)
    self.assertEqual(nearestRelation[0].distance, result[0].distance)
    self.assertEqual(nearestRelation[0].nearestSubObj, result[0].nearestSubObj)
    self.assertEqual(len(result),1)
    
  def test_getNearestRelationInsideCombinedPoly(self):
    nearestRelation = [osmData.distanceResult(0.17149859,(1,self.relType),[(5,self.wayType)])]
    
    result=self.testOSM6.getNearestRelation((2.0,7.0))
    self.assertEqual(nearestRelation[0].nearestObj, result[0].nearestObj)
    self.assertEqual(nearestRelation[0].distance, result[0].distance)
    self.assertEqual(nearestRelation[0].nearestSubObj, result[0].nearestSubObj)
    self.assertEqual(len(result),1)
    
  def test_getNearestRelationInside(self):
    nearestRelation =[osmData.distanceResult(0.9,(1,self.relType),[(2,self.wayType)])]
    
    result=self.testOSM5.getNearestRelation((3.0,1.1))
    self.assertEqual(nearestRelation[0].nearestObj, result[0].nearestObj)
    self.assertEqual(nearestRelation[0].distance, result[0].distance)
    self.assertEqual(nearestRelation[0].nearestSubObj, result[0].nearestSubObj)
    self.assertEqual(len(result),1)
  
  def test_getNearestRelationInsideInnerPoly(self):
    nearestRelation =[osmData.distanceResult(0.1,(1,self.relType),[(2,self.wayType)])]
    
    result=self.testOSM5.getNearestRelation((2.1,2.1))
    self.assertEqual(nearestRelation[0].nearestObj, result[0].nearestObj)
    self.assertEqual(nearestRelation[0].distance, result[0].distance)
    self.assertEqual(nearestRelation[0].nearestSubObj, result[0].nearestSubObj)
    self.assertEqual(len(result),1)
    
  def test_getNearestRelationInsideInnerInsideOuterPoly(self):
    nearestRelation =[osmData.distanceResult(0.3,(1,self.relType),[(7,self.wayType)])]
    
    result=self.testOSM5.getNearestRelation((2.5,2.5))
    self.assertEqual(nearestRelation[0].nearestObj, result[0].nearestObj)
    self.assertEqual(nearestRelation[0].distance, result[0].distance)
    self.assertEqual(nearestRelation[0].nearestSubObj, result[0].nearestSubObj)
    self.assertEqual(len(result),1)
  
  def test_getNearestRelationFilterByTags(self):
    nearestRelation= [osmData.distanceResult(15.55634919,(1,self.relType),[(1,self.wayType)])]
    
    result=self.testOSM5.getNearestRelation(self.testPoint2,{"name":"Tween"})
    self.assertEqual(nearestRelation[0].nearestObj, result[0].nearestObj)
    self.assertEqual(nearestRelation[0].distance, result[0].distance)
    self.assertEqual(nearestRelation[0].nearestSubObj, result[0].nearestSubObj)
    self.assertEqual(len(result),1)
  
  def test_getNearestRelationFilterByWildcard(self):
    nearestRelation= [osmData.distanceResult(7.07106781,(2,self.relType),[(4,self.wayType)])]
    
    result=self.testOSM5.getNearestRelation(self.testPoint2,{"name":"*"})
    self.assertEqual(nearestRelation[0].nearestObj, result[0].nearestObj)
    self.assertEqual(nearestRelation[0].distance, result[0].distance)
    self.assertEqual(nearestRelation[0].nearestSubObj, result[0].nearestSubObj)
    self.assertEqual(len(result),1)
    
  def test_getNearestRelationFilterByWildcardWrong(self):
    nearestRelation= [osmData.distanceResult(7.07106781,(2,self.relType),[(4,self.wayType)])]
    
    result=self.testOSM5.getNearestRelation(self.testPoint2,{"name":"Tween", "*":"*"})
    self.assertEqual(nearestRelation[0].nearestObj, result[0].nearestObj)
    self.assertEqual(nearestRelation[0].distance, result[0].distance)
    self.assertEqual(nearestRelation[0].nearestSubObj, result[0].nearestSubObj)
    self.assertEqual(len(result),1)
  
  def test_getNearestRelationFailFilterByTags(self):
    with self.assertRaises(TypeError):
      self.testOSM5.getNearestRelation(self.testPoint, "asd")
  
  def test_getNearestRelationTypeSite(self):
    nearestRelation= [osmData.distanceResult(0.17149859,(2,self.relType),[(1,self.relType)]),osmData.distanceResult(0.17149859,(3, self.relType),[(1,self.relType)])]
    result=self.testOSM8.getNearestRelation((2.0,7.0))
    self.assertEqual(nearestRelation[0].nearestObj, result[0].nearestObj)
    self.assertEqual(nearestRelation[0].distance, result[0].distance)
    self.assertEqual(nearestRelation[0].nearestSubObj, result[0].nearestSubObj)
    self.assertEqual(len(result),2)
    
  def test_getNearestRealtionNothinFound(self):
    result=self.testOSM5.getNearestRelation(self.testPoint, {"asd":"asd"})
    self.assertEqual(len(result),0)
  #========================================================


  #========================================================
  #Tests for getNearestWay
  #========================================================
  def test_getNearestWayOnlyPoly(self):
    nearestWay=[osmData.distanceResult(2.0,(3,self.wayType),[([(2.0, 3.0), (5.0, 8.0)],self.nodeType),([(2.0, 10.0), (2.0, 3.0)],self.nodeType)])]
    result=self.testOSM3.getNearestWay(self.testPoint,True)
    self.assertEqual(nearestWay[0].nearestObj, result[0].nearestObj)
    self.assertEqual(nearestWay[0].distance, result[0].distance)
    self.assertEqual(nearestWay[0].nearestSubObj, result[0].nearestSubObj)
    self.assertEqual(len(result),1)
    
  def test_getNearestWayOtherWayList(self):
    nearestWay=[osmData.distanceResult(2.0,(3,self.wayType),[([(2.0, 3.0), (5.0, 8.0)], self.nodeType),([(2.0, 10.0), (2.0, 3.0)],self.nodeType)])]
    result=self.testOSM3.getNearestWay(self.testPoint,False,{},[1,3])
    self.assertEqual(nearestWay[0].nearestObj, result[0].nearestObj)
    self.assertEqual(nearestWay[0].distance, result[0].distance)
    self.assertEqual(nearestWay[0].nearestSubObj, result[0].nearestSubObj)
    self.assertEqual(len(result),1)
  
  def test_getNearestWayAll(self):
    nearestWay=[osmData.distanceResult(2.12132034,(2,self.wayType),[([(2.0, 3.0), (5.0, 6.0)],self.nodeType)])]
    result=self.testOSM3.getNearestWay(self.testPoint3,False)
    self.assertEqual(nearestWay[0].nearestObj, result[0].nearestObj)
    self.assertEqual(nearestWay[0].distance, result[0].distance)
    self.assertEqual(nearestWay[0].nearestSubObj, result[0].nearestSubObj)
    self.assertEqual(len(result),1)
    
  def test_getNearestWayWithTagFilter(self):
    nearestWay=[osmData.distanceResult(4.47213595,(1,self.wayType),[([(6.0, 3.0), (8.0, 1.0)], self.nodeType), ([(10.0, 7.0), (6.0, 3.0)], self.nodeType)])]
    result=self.testOSM3.getNearestWay(self.testPoint,False, {"testTag":"testValue"})
    self.assertEqual(nearestWay[0].nearestObj, result[0].nearestObj)
    self.assertEqual(nearestWay[0].distance, result[0].distance)
    self.assertEqual(nearestWay[0].nearestSubObj, result[0].nearestSubObj)
    self.assertEqual(len(result),1)
    
  def test_getNearestWayWithTagFilterWildcard(self):
    nearestWay=[osmData.distanceResult(4.47213595,(1,self.wayType),[([(6.0, 3.0), (8.0, 1.0)], self.nodeType), ([(10.0, 7.0), (6.0, 3.0)], self.nodeType)])]
    result=self.testOSM3.getNearestWay(self.testPoint,False, {"testTag":"*"})
    self.assertEqual(nearestWay[0].nearestObj, result[0].nearestObj)
    self.assertEqual(nearestWay[0].distance, result[0].distance)
    self.assertEqual(nearestWay[0].nearestSubObj, result[0].nearestSubObj)
    self.assertEqual(len(result),1)
    
  def test_getNearestWayWithTagFilterWildcardWrong(self):
    nearestWay=[osmData.distanceResult(2.0,(2,self.wayType),[([(2.0, 3.0), (5.0, 6.0)],self.nodeType)]),([(2.0, 3.0), (5.0, 8.0)], self.nodeType)]
    result=self.testOSM3.getNearestWay(self.testPoint,False, {"*":"*"})
    self.assertEqual(nearestWay[0].distance, result[0].distance)
    self.assertEqual(nearestWay[0].nearestObj, result[0].nearestObj)
    self.assertEqual(nearestWay[0].nearestSubObj, result[0].nearestSubObj)
    self.assertEqual(len(result),2)

  def test_getNearestWayNothinFound(self):
    result= self.testOSM4.getNearestWay(self.testPoint,True, {"asd":"asd"})
    self.assertEqual(len(result),0)
  #========================================================

  
  def test_createOSM(self):
    self.assertIsNotNone(self.testOSM)
    self.assertIsNotNone(self.testOSM.nodes)
    self.assertIsNotNone(self.testOSM.ways)
    self.assertIsNotNone(self.testOSM.relations)
    
  def test_addNode(self):
    self.testOSM.addNode(self.testNode)
    self.assertEqual(self.testOSM.nodes[self.testNode.id], self.testNode)
    
  def test_addNodeFail(self):
    with self.assertRaises(TypeError):
      self.testOSM.addNode("blub")
  
  def test_addNodeTwice(self):
    self.testOSM.addNode(self.testNode)
    self.assertEqual(len(self.testOSM.nodes),1)
    self.testOSM.addNode(self.testNode)
    self.assertEqual(len(self.testOSM.nodes),1)
    
  def test_addTwoNodes(self):
    self.testOSM.addNode(self.testNode)
    secondNode = self.testNode
    secondNode.id = 2
    self.testOSM.addNode(self.testNode)
    self.assertEqual(len(self.testOSM.nodes),2)
    self.assertEqual(self.testOSM.nodes[secondNode.id], secondNode)
    
  def test_addNodeList(self):
    testNodeList = [self.testNode, osmData.Node("0002", 0.123, 0.12312, {"building":"university"})]
    self.testOSM.addNodeList(testNodeList)
    self.assertEqual(len(self.testOSM.nodes), len(testNodeList))
    for node in testNodeList:
      self.assertEqual(self.testOSM.nodes[node.id], node)
    
  def test_addNodeListFailNoList(self):
    with self.assertRaises(TypeError):
      self.testOSM.addNodeList(self.testNode)
    
  def test_addWay(self):
    self.testOSM.addWay(self.testWay)
    self.assertEqual(self.testOSM.ways[self.testWay.id], self.testWay)
    
  def test_addWayFail(self):
    with self.assertRaises(TypeError):
      self.testOSM.addWay(self.testNode)
  
  def test_addRelation(self):
    self.testOSM.addRelation(self.testRelation)
    self.assertEqual(self.testOSM.relations[self.testRelation.id], self.testRelation)
    
  def test_addRelationFail(self):
    with self.assertRaises(TypeError):
      self.testOSM.addRelation(42)
      

if __name__ == '__main__':
  unittest.main()
