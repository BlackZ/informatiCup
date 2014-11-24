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
    self.testRelation=osmData.Relation(5, [("way","1","outer"),("way","2","inner")], 
                                       {"name":"Tween Pond", "natural":"water"})
    
    self.testOSM = osmData.OSM()
    
    self.testOSM2=osmData.OSM()
    self.testOSM2.addNodeList([osmData.Node(1, 52.12, 4.12, {}),
                               osmData.Node(2, 52.13, 4.12, {}),
                               osmData.Node(3, 52.12, 4.13, {})])
    self.testOSM2.addWay(self.testWay)

    #Test Point for Nearest Functions
    self.testPoint = (2.0,1.0)
    self.testPoint2 = (15.0,15.0)
    
    #Nearest Poly Function Variables
    self.testOSM3 = osmData.OSM()
    self.testOSM3.addNodeList([osmData.Node(1, 6, 3, {}),
                               osmData.Node(2, 8, 1, {}),
                               osmData.Node(3, 10, 3, {}),
                               osmData.Node(4, 10, 7, {}),
                               osmData.Node(5, 2, 3, {}),
                               osmData.Node(6, 5, 8, {}),
                               osmData.Node(7, 2, 10, {})])
    self.testOSM3.addWay(osmData.Way(1,[1,2,3,4,1],{"testTag":"testValue"}))
    self.testOSM3.addWay(osmData.Way(2,[5,6,7],{}))
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
                           osmData.Node(8, 3, 2, {})])
    self.testOSM5.addWay(osmData.Way(1, [1,2,3,4,1],{}))
    self.testOSM5.addWay(osmData.Way(2, [5,6,7,8,5],{}))
    self.testOSM5.addRelation(osmData.Relation(1, [("way","1","outer"),("way","2","inner")], 
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
    self.testOSM5.addRelation(osmData.Relation(2, [("way","3","outer"),("way","4","outer")], 
                                       {"name":"Tween Pond", "natural":"water","type":"multipolygon"}))
    
    self.testOSM5.addNodeList([osmData.Node(16, 8, 8, {}),
                           osmData.Node(17, 8, 9, {}),
                           osmData.Node(18, 9, 9, {}),
                           osmData.Node(19, 9, 8, {})])
    self.testOSM5.addWay(osmData.Way(5, [16,17],{}))
    self.testOSM5.addWay(osmData.Way(6, [18,19],{}))
    self.testOSM5.addRelation(osmData.Relation(3, [("way","5","road"),("way","6","road")], 
                                       {"name":"Tween Pond", "natural":"water","type":"route"}))
    

  def test_getNearestNode(self):
    nearestPoint = ("1", 4.47213595499958)
    self.assertEqual(nearestPoint, self.testOSM4.getNearestNode(self.testPoint))
  
  def test_getNearestNodeWithTagFilter(self):
    nearestPoint = ("2", 6.0)
    self.assertEqual(nearestPoint, self.testOSM4.getNearestNode(self.testPoint, {"testTag":"testValue"}))
    
  def test_getNearestNodeFailWithTagFilter(self):
    with self.assertRaises(TypeError):
      self.testOSM4.getNearestNode(self.testPoint, "asd")
  
  def test_getNearestNodeFail(self):
    with self.assertRaises(TypeError):
      self.testOSM4.getNearestNode((1,0))
  
  def test_getNearestNodeNothnigFound(self):
    nearestPoint = (None, sys.float_info.max)
    self.assertEqual(nearestPoint, self.testOSM4.getNearestNode(self.testPoint, {"asd":"asd"}))

  def test_getNearestRelation(self):
    nearestRelation = (("2","4"), 7.0710678118654755)
    self.assertEqual(nearestRelation, self.testOSM5.getNearestRelation(self.testPoint2,False))
    
  def test_getNearestRelationInside(self):
    nearestRelation = (("1","1"), -1)
    self.assertEqual(nearestRelation, self.testOSM5.getNearestRelation(self.testPoint,False))
  
  def test_getNearestRelationOnlyPolygon(self):
    pass
  
  def test_getNearestRelationFilterByTags(self):
    nearestRelation = (("1","1"), 15.556349186104045)
    self.assertEqual(nearestRelation, self.testOSM5.getNearestRelation(self.testPoint2,False,{"name":"Tween"}))
  
  def test_getNearestRelationFailFilterByTags(self):
    with self.assertRaises(TypeError):
      self.testOSM5.getNearestRelation(self.testPoint,False, "asd")

  def test_getNearestNodeFailPoint(self):
    with self.assertRaises(TypeError):
      self.testOSM3.getNearestWay((1,0),True)

  def test_getNearestNodeFailFilter(self):
    with self.assertRaises(TypeError):
      self.testOSM3.getNearestWay(self.testPoint,True,"asd")

  def test_getNearestWayOnlyPoly(self):
    nearestPoly = ("3", 2.0) 
    self.assertEqual(nearestPoly, self.testOSM3.getNearestWay(self.testPoint,True))
    
  def test_getNearestWayOtherWayList(self):
    nearestPoly = ("3", 2.0) 
    self.assertEqual(nearestPoly, self.testOSM3.getNearestWay(self.testPoint,False,{},["1","3"]))
    
  def test_getNearestWayAll(self):
    nearestPoly = ("3", 2.0)
    self.assertEqual(nearestPoly, self.testOSM3.getNearestWay(self.testPoint,False))
    
  def test_getNearestWayWithTagFilter(self):
    nearestPoly = ("1", 4.47213595499958)
    self.assertEqual(nearestPoly, self.testOSM3.getNearestWay(self.testPoint,False, {"testTag":"testValue"}))

  def test_getNearestWayNothinFound(self):
    nearestPoly = (None, sys.float_info.max)
    self.assertEqual(nearestPoly, self.testOSM4.getNearestWay(self.testPoint,True, {"asd":"asd"}))

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
