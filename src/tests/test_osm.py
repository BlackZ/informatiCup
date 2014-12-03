# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 11:46:54 2014

@author: jpoeppel & adreyer
"""

import unittest
import osmData
import sys

class TestOSMObject(unittest.TestCase):
  
  def setUp(self):
    
    self.testNode = osmData.Node(1, 0.1, 2.1, {"highway":"traffic_signals"})
    self.testWay = osmData.Way(3, [1,2,3,1], {"highway":"residential",
                                              "name":"Clipstone Street"})
    self.testRelation=osmData.Relation(5, [("way",1,"outer"),("way",2,"inner")], 
                                       {"name":"Tween Pond", "natural":"water"})
    
    self.testOSM = osmData.OSM()
    
    self.testOSM2=osmData.OSM()
    self.testOSM2.addNodeList([osmData.Node(1, 52.12, 4.12, {}),
                               osmData.Node(2, 52.13, 4.12,{}),
                               osmData.Node(3, 52.12, 4.13, {})])
    self.testOSM2.addWay(self.testWay)
    self.testOSM2.addRelation(osmData.Relation(1, [("way", 3, "outer")], {"boundary":"postal_code","type":"boundary", "postal_code":"33615"}))

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
    self.testOSM3.addWay(osmData.Way(1,[1,2,3,4,1],{"testTag":"testValue"}))
    self.testOSM3.addWay(osmData.Way(2,[5,8,7],{}))
    self.testOSM3.addWay(osmData.Way(3,[5,6,7,5],{}))
    
    #Nearest Poly (fail)/Node Function Variables
    self.testOSM4 = osmData.OSM()
    self.testOSM4.addNodeList([osmData.Node(1, 6.0, 3.0, {}),
                               osmData.Node(2, 8.0, 1.0, {"testTag":"testValue"}),
                               osmData.Node(3, 10.0, 3.0, {"testTag":"testValue"}),
                               osmData.Node(4, 10.0, 7.0, {})])
    self.testOSM4.addWay(osmData.Way(1, [1,2],{}))
    self.testOSM4.addWay(osmData.Way(2, [3,4],{}))
    
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
    self.testOSM5.addWay(osmData.Way(1, [1,2,3,4,1],{}))
    self.testOSM5.addWay(osmData.Way(2, [5,6,7,8,5],{}))
    self.testOSM5.addWay(osmData.Way(7, [20,21,22,23,20],{}))
    self.testOSM5.addRelation(osmData.Relation(1, [("way",1,"outer"),("way",2,"inner"),("way",7,"outer")], 
                                       {"name":"Tween", "natural":"water", "type":"multipolygon"}))
    
    self.testOSM5.addNodeList([osmData.Node(9, 8, 8, {}),
                           osmData.Node(10, 8, 9, {}),
                           osmData.Node(11, 9, 9, {}),
                           osmData.Node(12, 9, 8, {}),
                           osmData.Node(13, 9, 10, {}),
                           osmData.Node(14, 10, 10, {}),
                           osmData.Node(15, 10, 8, {})])
    self.testOSM5.addWay(osmData.Way(3, [9,10,11,12,9],{}))
    self.testOSM5.addWay(osmData.Way(4, [11,13,14,15,11],{}))
    self.testOSM5.addRelation(osmData.Relation(2, [("way",3,"outer"),("way",4,"outer")], 
                                       {"name":"Tween Pond", "natural":"water","type":"multipolygon"}))
    
    self.testOSM5.addNodeList([osmData.Node(16, 8, 8, {}),
                           osmData.Node(17, 8, 9, {}),
                           osmData.Node(18, 9, 9, {}),
                           osmData.Node(19, 9, 8, {})])
    self.testOSM5.addWay(osmData.Way(5, [16,17],{}))
    self.testOSM5.addWay(osmData.Way(6, [18,19],{}))
    self.testOSM5.addRelation(osmData.Relation(3, [("way",5,"road"),("way",6,"road")], 
                                       {"name":"Tween Pond", "natural":"water","type":"route"}))
    
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
    
    self.testOSM6.addWay(osmData.Way(1, [1, 2, 3], {}))
    self.testOSM6.addWay(osmData.Way(2, [3, 4], {}))
    self.testOSM6.addWay(osmData.Way(5, [4, 5, 1], {}))
    self.testOSM6.addWay(osmData.Way(3, [6, 7, 8], {}))
    self.testOSM6.addWay(osmData.Way(4, [8, 9, 10, 6], {}))
    self.testOSM6.addWay(osmData.Way(6, [1, 2], {}))
    self.testOSM6.addWay(osmData.Way(7, [2, 3, 1], {}))
    
    self.testOSM6.addRelation(osmData.Relation(1,
                                               [("way", 1, "outer"),("way", 2, "outer"),("way", 5, "outer"),("way", 3, "inner"), ("way", 4, "inner"),("way", 6, "inner"),("way", 7, "outer") ],
                                               {"type":"multipolygon"}))
    
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
    
    for way in self.testOSM6.ways:
      self.testOSM7.addWay(self.testOSM6.ways[way])
    self.testOSM7.addWay(osmData.Way(5, [11, 12, 13, 11], {}))
    
    self.testOSM7.addRelation(osmData.Relation(1,
                                               [("way", 1, "outer"),("way", 2, "outer"),("way", 3, "inner"), ("way", 4, "inner"), ("way", 5, "outer")],
                                               {"type":"multipolygon"}))
    
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
    
    for way in self.testOSM6.ways:
      self.testOSM8.addWay(self.testOSM6.ways[way])
    self.testOSM8.addWay(osmData.Way(8, [11, 12, 13, 11], {}))
    
    self.testOSM8.addRelation(osmData.Relation(1,
                                               [("way", 1, "outer"),("way", 2, "outer"),("way", 3, "inner"), ("way", 4, "inner"), ("way", 5, "outer")],
                                               {"type":"multipolygon"}))
    self.testOSM8.addRelation(osmData.Relation(2,
                                               [("way", 8, "outer"),("relation", 1, "parking")],
                                               {"type":"site"}))
    
    self.testOSM9=osmData.OSM()
    self.testWay9 = osmData.Way(3, [1,2,3], {"highway":"residential",
                                              "name":"Clipstone Street"})
    self.testOSM9.addNodeList([osmData.Node(1, 52.12, 4.12, {}),
                               osmData.Node(2, 52.13, 4.12, {}),
                               osmData.Node(3, 52.12, 4.13, {})])
    self.testOSM9.addWay(self.testWay9)
    self.testOSM9.addRelation(osmData.Relation(1, [("way", 3, "outer")], {"boundary":"postal_code","type":"boundary", "postal_code":"33615"}))

  #========================================================
  #Tests for _searchforPolygons
  #========================================================
  def test_searchForPolygons(self):
    trueValue=[[1, 2, 5], [3, 4]]
    self.testOSM6._searchForPolygons(self.testOSM6.relations[1])
    self.assertEqual(self.testOSM6.relations[1].polygons,trueValue)
  
  def test_searchForPolygonsNoPoly(self):
    trueValue=[]
    self.testOSM9._searchForPolygons(self.testOSM9.relations[1])
    self.assertEqual(self.testOSM9.relations[1].polygons,trueValue)
    
  def test_searchForPolygonsWithNaturalPoly(self):
    trueValue=[[3]]
    self.testOSM2._searchForPolygons(self.testOSM2.relations[1])
    self.assertEqual(self.testOSM2.relations[1].polygons,trueValue)
  
  def test_searchForPolygonsNoRealtion(self):
    with self.assertRaises(TypeError):
      self.testOSM6._searchForPolygons("asd")
  #========================================================
  
  
  #========================================================
  #Tests for getNearestNode
  #========================================================
  def test_getNearestNode(self):
    nearestPoint=osmData.distanceResult(4.47213595499958,(1,"node"))
    result=self.testOSM4.getNearestNode(self.testPoint)
    self.assertEqual(nearestPoint.nearestObj, result.nearestObj)
    self.assertEqual(nearestPoint.distance, result.distance)
    self.assertEqual(nearestPoint.nearestSubObj, result.nearestSubObj)
  
  def test_getNearestNodeWithTagFilter(self):
    nearestPoint = osmData.distanceResult(6.0,(2,"node"))
    result=self.testOSM4.getNearestNode(self.testPoint, {"testTag":"testValue"})
    self.assertEqual(nearestPoint.nearestObj, result.nearestObj)
    self.assertEqual(nearestPoint.distance, result.distance)
    self.assertEqual(nearestPoint.nearestSubObj, result.nearestSubObj)
    
  def test_getNearestNodeFailWithTagFilter(self):
    with self.assertRaises(TypeError):
      self.testOSM4.getNearestNode(self.testPoint, "asd")
  
  def test_getNearestNodeFail(self):
    with self.assertRaises(TypeError):
      self.testOSM4.getNearestNode((1,0))
      
  def test_getNearestNodeFailPoint(self):
    with self.assertRaises(TypeError):
      self.testOSM3.getNearestWay((1,0),True)

  def test_getNearestNodeFailFilter(self):
    with self.assertRaises(TypeError):
      self.testOSM3.getNearestWay(self.testPoint,True,"asd")
  
  def test_getNearestNodeNothnigFound(self):
    nearestPoint = osmData.distanceResult(sys.float_info.max,("-1",None))
    result=self.testOSM4.getNearestNode(self.testPoint, {"asd":"asd"})
    self.assertEqual(nearestPoint.nearestObj, result.nearestObj)
    self.assertEqual(nearestPoint.distance, result.distance)
    self.assertEqual(nearestPoint.nearestSubObj, result.nearestSubObj)
  #========================================================

  #========================================================
  #Tests for getNearestRelation
  #========================================================
  def test_isInsideCombinedPoly(self):
    trueResult = (True,([1,2,5],"way"))
    result=self.testOSM6.isInside((2.0,7.0),1)
    self.assertEqual(result,trueResult)
  
  def test_isInsideWithMoreRelations(self):
    trueResult = (True,([1],"relation"))
    result=self.testOSM8.isInside((2.0,7.0),2)
    self.assertEqual(result,trueResult)
  #========================================================

  #========================================================
  #Tests for getNearestRelation
  #========================================================
  def test_getNearestRelation(self):
    nearestRelation = osmData.distanceResult(7.0710678118654755,(2,"relation"),(4,"way"))
    
    result=self.testOSM5.getNearestRelation(self.testPoint2)
    self.assertEqual(nearestRelation.nearestObj, result.nearestObj)
    self.assertEqual(nearestRelation.distance, result.distance)
    self.assertEqual(nearestRelation.nearestSubObj, result.nearestSubObj)
    
  def test_getNearestRelationInsideCombinedPoly(self):
    nearestRelation = osmData.distanceResult(0.17149858514250862,(1,"relation"),(5,"way"))
    
    result=self.testOSM6.getNearestRelation((2.0,7.0))
    self.assertEqual(nearestRelation.nearestObj, result.nearestObj)
    self.assertEqual(nearestRelation.distance, result.distance)
    self.assertEqual(nearestRelation.nearestSubObj, result.nearestSubObj)
    
  def test_getNearestRelationInside(self):
    nearestRelation =osmData.distanceResult(0.8999999999999999,(1,"relation"),(2,"way"))
    
    result=self.testOSM5.getNearestRelation((3.0,1.1))
    self.assertEqual(nearestRelation.nearestObj, result.nearestObj)
    self.assertEqual(nearestRelation.distance, result.distance)
    self.assertEqual(nearestRelation.nearestSubObj, result.nearestSubObj)
  
  def test_getNearestRelationInsideInnerPoly(self):
    nearestRelation =osmData.distanceResult(0.10000000000000009,(1,"relation"),(2,"way"))
    
    result=self.testOSM5.getNearestRelation((2.1,2.1))
    self.assertEqual(nearestRelation.nearestObj, result.nearestObj)
    self.assertEqual(nearestRelation.distance, result.distance)
    self.assertEqual(nearestRelation.nearestSubObj, result.nearestSubObj)
    
  def test_getNearestRelationInsideInnerInsideOuterPoly(self):
    nearestRelation =osmData.distanceResult(0.2999999999999998,(1,"relation"),(7,"way"))
    
    result=self.testOSM5.getNearestRelation((2.5,2.5))
    self.assertEqual(nearestRelation.nearestObj, result.nearestObj)
    self.assertEqual(nearestRelation.distance, result.distance)
    self.assertEqual(nearestRelation.nearestSubObj, result.nearestSubObj)
  
  def test_getNearestRelationFilterByTags(self):
    nearestRelation= osmData.distanceResult(15.556349186104045,(1,"relation"),(1,"way"))
    
    result=self.testOSM5.getNearestRelation(self.testPoint2,{"name":"Tween"})
    self.assertEqual(nearestRelation.nearestObj, result.nearestObj)
    self.assertEqual(nearestRelation.distance, result.distance)
    self.assertEqual(nearestRelation.nearestSubObj, result.nearestSubObj)
  
  def test_getNearestRelationFailFilterByTags(self):
    with self.assertRaises(TypeError):
      self.testOSM5.getNearestRelation(self.testPoint, "asd")
  
  def test_getNearestRelationTypeSite(self):
    nearestRelation= osmData.distanceResult(0.17149858514250862,(2,"relation"),(1,"relation"))
    result=self.testOSM8.getNearestRelation((2.0,7.0))
    self.assertEqual(nearestRelation.nearestObj, result.nearestObj)
    self.assertEqual(nearestRelation.distance, result.distance)
    self.assertEqual(nearestRelation.nearestSubObj, result.nearestSubObj)
  #========================================================


  #========================================================
  #Tests for getNearestWay
  #========================================================
  def test_getNearestWayOnlyPoly(self):
    nearestWay=osmData.distanceResult(2.0,(3,"way"))
    result=self.testOSM3.getNearestWay(self.testPoint,True)
    self.assertEqual(nearestWay.nearestObj, result.nearestObj)
    self.assertEqual(nearestWay.distance, result.distance)
    self.assertEqual(nearestWay.nearestSubObj, result.nearestSubObj)
    
  def test_getNearestWayOtherWayList(self):
    nearestWay=osmData.distanceResult(2.0,(3,"way"))
    result=self.testOSM3.getNearestWay(self.testPoint,False,{},[1,3])
    self.assertEqual(nearestWay.nearestObj, result.nearestObj)
    self.assertEqual(nearestWay.distance, result.distance)
    self.assertEqual(nearestWay.nearestSubObj, result.nearestSubObj)
  
  def test_getNearestWayAll(self):
    nearestWay=osmData.distanceResult(2.1213203435596424,(2,"way"))
    result=self.testOSM3.getNearestWay(self.testPoint3,False)
    self.assertEqual(nearestWay.nearestObj, result.nearestObj)
    self.assertEqual(nearestWay.distance, result.distance)
    self.assertEqual(nearestWay.nearestSubObj, result.nearestSubObj)
    
  def test_getNearestWayWithTagFilter(self):
    nearestWay =osmData.distanceResult(4.47213595499958,(1,"way"))
    result=self.testOSM3.getNearestWay(self.testPoint,False, {"testTag":"testValue"})
    self.assertEqual(nearestWay.nearestObj, result.nearestObj)
    self.assertEqual(nearestWay.distance, result.distance)
    self.assertEqual(nearestWay.nearestSubObj, result.nearestSubObj)

  def test_getNearestWayNothinFound(self):
    nearestWay = osmData.distanceResult(sys.float_info.max,("-1",None))
    result= self.testOSM4.getNearestWay(self.testPoint,True, {"asd":"asd"})
    self.assertEqual(nearestWay.nearestObj, result.nearestObj)
    self.assertEqual(nearestWay.distance, result.distance)
    self.assertEqual(nearestWay.nearestSubObj, result.nearestSubObj)
  #========================================================


  def test_verticies(self):
    trueList=[(52.12, 4.12),(52.13, 4.12),(52.12, 4.13),(52.12, 4.12)]
    self.assertEqual(self.testOSM2._vertices(self.testWay.refs),trueList)
  
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
