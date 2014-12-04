# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 12:53:23 2014

@author: jpoeppel & adreyer
"""

import unittest
import osmData

class TestRelationObject(unittest.TestCase):
  
  def setUp(self):
    self.id = "0001"
    self.members = [("way",8125151,"outer"),("way",249285853,"inner")]
    self.tags = {"name":"Tween Pond", "natural":"water"}
    
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
    
    self.wayType=self.testOSM8.ways[8].__class__
    self.relType=self.testOSM8.relations[1].__class__
    
  
  #========================================================
  #Tests for isInside
  #========================================================
  def test_isInsideCombinedPoly(self):
    trueResult = (True,([1,2,5],self.wayType))
    result=self.testOSM6.relations[1].isInside((2.0,7.0),self.testOSM6)
    self.assertEqual(result,trueResult)
  
  def test_isInsideOutside(self):
    trueResult = (False,("-1",None))
    result=self.testOSM6.relations[1].isInside((2.0,9.0),self.testOSM6)
    self.assertEqual(result,trueResult)
  
  def test_isInsideWithMoreRelations(self):
    trueResult = (True,([1],self.relType))
    result=self.testOSM8.relations[2].isInside((2.0,7.0),self.testOSM8)
    self.assertEqual(result,trueResult)
    
  def test_isInsideComplex(self):
    trueResult = (True,([7],self.wayType))
    result=self.testOSM5.relations[1].isInside((2.5,2.5),self.testOSM5)
    self.assertEqual(result,trueResult)
    
  def test_isInsideComplex2(self):
    trueResult = (True,([2],self.wayType))
    result=self.testOSM5.relations[1].isInside((2.18,2.18),self.testOSM5)
    self.assertEqual(result,trueResult)
  #========================================================
  
  def test_createRelation(self):
    testRelation = osmData.Relation(self.id, self.members, self.tags)
    self.assertIsNotNone(testRelation)
    self.assertEqual(testRelation.id, self.id)
    self.assertEqual(testRelation.members, self.members)
    self.assertEqual(testRelation.tags, self.tags)
    
  def test_createRelationFail(self):
    testRelation = osmData.Relation(23, [self.members[0]], self.tags)
    self.assertNotEqual(testRelation.id, self.id)
    self.assertNotEqual(testRelation.members, self.members)
    self.assertEqual(testRelation.tags, self.tags)
    
  def test_createRelationWithIntId(self):
    testRelation = osmData.Relation(int(self.id), self.members, self.tags)
    self.assertNotEqual(testRelation.id, self.id)
    self.assertEqual(testRelation.id, "1")
    
  def test_createRealtionFailMembersNoList(self):
    with self.assertRaises(TypeError):
      testRelation = osmData.Relation(self.id, "fail", self.tags)
      
  def test_createRelationFailNotADictionary(self):
    with self.assertRaises(TypeError):
      testRelation = osmData.Relation(self.id, self.members, "a:b")
  
  def test_isRelationEqual(self):
    testRelation = osmData.Relation(self.id, self.members, self.tags)
    #Deliberatly not using the self variables to make sure it is filled with
    #other objects
    otherRelation = osmData.Relation("0001", 
                  [("way",8125151,"outer"),("way",249285853,"inner")], 
                   {"name":"Tween Pond", "natural":"water"})
    self.assertEqual(testRelation, otherRelation)
    
  def test_isRelationNotEqual(self):
    testRelation = osmData.Relation(self.id, self.members, self.tags)
    #Deliberatly not using the self variables to make sure it is filled with
    #other objects
    otherRelation = osmData.Relation("0002", 
                  [("way",8125151,"outer"),("way",249285853,"inner")], 
                   {"name":"Tween Pond", "natural":"water"})
    self.assertNotEqual(testRelation, otherRelation)
    
  def test_addPolygon(self):
    testRelation = osmData.Relation(self.id, self.members, self.tags)
    polyList = [[1,2,3,4,5]]
    emptyList = []
    self.assertEqual(testRelation.polygons, emptyList)
    testRelation.addPolygon([1,2,3,4,5])
    self.assertEqual(testRelation.polygons, polyList)
    
  def test_addPolygonList(self):
    testRelation = osmData.Relation(self.id, self.members, self.tags)
    emptyList = []
    polyList = [[1,2,3,4], [5,6,7]]
    self.assertEqual(testRelation.polygons, emptyList)
    testRelation.addPolygonList([[1,2,3,4], [5,6,7]])
    self.assertEqual(testRelation.polygons, polyList)
  

if __name__ == '__main__':
  unittest.main()
