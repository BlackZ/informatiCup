# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 11:46:54 2014

@author: jpoeppel & adreyer
"""


import unittest
import osmData

class TestOSMObject(unittest.TestCase):
  
  def setUp(self):
    
    self.testNode = osmData.Node(1, 0.1, 2.1, {"highway":"traffic_signals"})
    self.testWay = osmData.Way(3, [1,2,3,1], {"highway":"residential",
                                              "name":"Clipstone Street"})
    self.testRelation = osmData.Relation(5, [("way",8125151,"outer"),("way",249285853,"inner")], 
                                             {"name":"Tween Pond", "natural":"water"})
    
    self.testOSM = osmData.OSM()
    
    self.testOSM2=osmData.OSM()
    self.testOSM2.addNodeList([osmData.Node(1, 52.12, 4.12, {}),
                               osmData.Node(2, 52.13, 4.12, {}),
                               osmData.Node(3, 52.12, 4.13, {})])
    self.testOSM2.addWay(self.testWay)

    #Test Point for Nearest Functions
    self.testPoint = (2,1)
    
    #Nearest Poly Function Variables
    self.testOSM3 = osmData.OSM()
    self.testOSM3.addNodeList([osmData.Node(1, 6, 3, {}),
                               osmData.Node(2, 8, 1, {}),
                               osmData.Node(3, 10, 3, {}),
                               osmData.Node(4, 10, 7, {}),
                               osmData.Node(5, 3, 7, {}),
                               osmData.Node(6, 5, 8, {}),
                               osmData.Node(7, 2, 10, {})])
    self.testOSM3.addWay(osmData.Way(1,[1,2,3,4,1]))
    self.testOSM3.addWay(osmData.Way(2,[5,6,7,5]))
    
    #Nearest Poly (fail)/Node Function Variables
    self.testOSM4 = osmData.OSM()
    self.testOSM4.addNodeList([osmData.Node(1, 6, 3, {}),
                               osmData.Node(2, 8, 1, {}),
                               osmData.Node(3, 10, 3, {}),
                               osmData.Node(4, 10, 7, {})])
    self.testOSM4.addWay(osmData.Way(1, [1,2]))
    self.testOSM4.addWay(osmData.Way(2, [3,4]))
    

  def test_getNearestNode(self):
    nearestPoint = (1, 5.385164807) #sqrt(29)
    self.assertEqual(nearestPoint, self.testOSM4.getNearestNode(self.testPoint))

  def test_getNearestRelation(self):
    pass

  def test_getNearestPoly(self):
    nearestPoly = (1, 4.242640687) #3*sqrt(2)
    self.assertEqual(nearestPoly, self.testOSM3.getNearestPoly(self.testPoint))

  def test_getNearestPolyFail(self):
    nearestPoly = (-1,-2)
    self.assertEqual(nearestPoly, self.testOSM4.getNearestPoly(self.testPoint))

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
