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
    self.testWay = osmData.Way(3, [1,2,3], {"highway":"residential","name":"Clipstone Street"})
    self.testRelation = osmData.Relation(5, [("way",8125151,"outer"),("way",249285853,"inner")], {"name":"Tween Pond", "natural":"water"})
    
    self.testOSM = osmData.OSM()
  
  def test_createOSM(self):
    self.assertIsNotNone(self.testOSM)
    self.assertIsNotNone(self.testOSM.nodes)
    self.assertIsNotNone(self.testOSM.ways)
    self.assertIsNotNone(self.testOSM.relations)
    
  def test_addNode(self):
    self.testOSM.addNode(self.testNode)
    self.assertEqual(self.testOSM.nodes[self.testNode.id], self.testNode)
    
  def test_addNodeFail(self):
    with self.assertRaises(SystemExit) as errorMessage:
      self.testOSM.addNode("blub")
    self.assertEqual(errorMessage.exception.code, -1)
  
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
    
  def test_addWay(self):
    self.testOSM.addWay(self.testWay)
    self.assertEqual(self.testOSM.ways[self.testWay.id], self.testWay)
    
  def test_addWayFail(self):
    with self.assertRaises(SystemExit) as errorMessage:
      self.testOSM.addWay(self.testNode)
    self.assertEqual(errorMessage.exception.code, -1)
  
  def test_addRelation(self):
    self.testOSM.addRelation(self.testRelation)
    self.assertEqual(self.testOSM.relations[self.testRelation.id], self.testRelation)
    
  def test_addRelationFail(self):
    with self.assertRaises(SystemExit) as errorMessage:
      self.testOSM.addRelation(42)
    self.assertEqual(errorMessage.exception.code, -1)
  


if __name__ == '__main__':
  unittest.main()
