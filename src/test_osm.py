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
  
  def test_createOSM(self):
    testOSM = osmData.OSM()
    self.assertIsNotNone(testOSM)
    self.assertIsNotNone(testOSM.nodes)
    self.assertIsNotNone(testOSM.ways)
    self.assertIsNotNone(testOSM.relations)
    testOSM.addNode(self.testNode)
    testOSM.addWay(self.testWay)
    testOSM.addRelation(self.testRelation)
    self.assertEqual(testOSM.nodes[1], self.testNode)
    self.assertEqual(testOSM.ways[3], self.testWay)
    self.assertEqual(testOSM.relations[5], self.testRelation)


if __name__ == '__main__':
  unittest.main()
