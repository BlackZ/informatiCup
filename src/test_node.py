# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 12:23:35 2014

@author: jpoeppel & adreyer
"""


import unittest
import osmData

class TestNodeObject(unittest.TestCase):
  
  def setUp(self):
    self.id = 1
    self.lat = 0.1
    self.lon = 2.1
    self.tags = {"highway":"traffic_signals"}
    
  
  def test_createNode(self):
    testNode = osmData.Node(self.id, self.lat, self.lon, self.tags)
    self.assertIsNotNone(testNode)
    self.assertEqual(testNode.id, self.id)
    self.assertEqual(testNode.lat, self.lat)
    self.assertEqual(testNode.lon, self.lon)
    self.assertEqual(testNode.tags, self.tags)
    
  def test_createNodeFail(self):
    testNode = osmData.Node(self.id, self.lon, self.lat, self.tags)
    self.assertEqual(testNode.id, self.id)
    self.assertNotEqual(testNode.lat, self.lat)
    self.assertNotEqual(testNode.lon, self.lon)
    self.assertEqual(testNode.tags, self.tags)
  

if __name__ == '__main__':
  unittest.main()
