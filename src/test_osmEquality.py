# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 13:02:21 2014

Note 15.11: Deliberatly left the ids here as ints to show that 
this does not make a difference for the datatypes and they still work as intended
as of now.
@author: jpoeppel
"""

import unittest
import osmData

class TestOSMObjectEquality(unittest.TestCase):
  
  def setUp(self):
    
    self.testNode = osmData.Node(1, 0.1, 2.1, {"highway":"traffic_signals"})
    self.testWay = osmData.Way(3, [1,2,3], {"highway":"residential","name":"Clipstone Street"})
    self.testRelation = osmData.Relation(5, [("way",8125151,"outer"),("way",249285853,"inner")], 
                                             {"name":"Tween Pond", "natural":"water"})
    
    self.testOSM = osmData.OSM()
    self.testOSM.addNode(self.testNode)
    self.testOSM.addRelation(self.testRelation)
    self.testOSM.addWay(self.testWay)    
    
    
  def test_isOSMEqual(self):
    
    compareNode = osmData.Node(1, 0.1, 2.1, {"highway":"traffic_signals"})
    compareWay = osmData.Way(3, [1,2,3], {"highway":"residential","name":"Clipstone Street"})
    compareRelation = osmData.Relation(5, [("way",8125151,"outer"),("way",249285853,"inner")], 
                                             {"name":"Tween Pond", "natural":"water"})
    compareOSMObject = osmData.OSM()
    compareOSMObject.addNode(compareNode)
    compareOSMObject.addWay(compareWay)
    compareOSMObject.addRelation(compareRelation)
    
    self.assertEqual(self.testOSM, compareOSMObject)
    
    
  def test_isOSMNotEqualMoreNodes(self):
    #Deliberatly not using the self variables to make sure it is filled with
    #other objects
    compareNode = osmData.Node(1, 0.1, 2.1, {"highway":"traffic_signals"})
    secondCompareNode = osmData.Node(2, 0.1, 2.1, {"highway":"traffic_signals"})
    compareWay = osmData.Way(3, [1,2,3], {"highway":"residential","name":"Clipstone Street"})
    compareRelation = osmData.Relation(5, [("way",8125151,"outer"),("way",249285853,"inner")], 
                                             {"name":"Tween Pond", "natural":"water"})
    compareOSMObject = osmData.OSM()
    compareOSMObject.addNode(compareNode)
    compareOSMObject.addNode(secondCompareNode)
    compareOSMObject.addWay(compareWay)
    compareOSMObject.addRelation(compareRelation)
    
    self.assertNotEqual(self.testOSM, compareOSMObject)
    
  def test_isOSMNotEqualWrongNode(self):
    #Deliberatly not using the self variables to make sure it is filled with
    #other objects
    compareNode = osmData.Node(2, 0.1, 2.1, {"highway":"traffic_signals"})
    compareWay = osmData.Way(3, [1,2,3], {"highway":"residential","name":"Clipstone Street"})
    compareRelation = osmData.Relation(5, [("way",8125151,"outer"),("way",249285853,"inner")], 
                                             {"name":"Tween Pond", "natural":"water"})
    compareOSMObject = osmData.OSM()
    compareOSMObject.addNode(compareNode)
    compareOSMObject.addWay(compareWay)
    compareOSMObject.addRelation(compareRelation)
    self.assertNotEqual(self.testOSM, compareOSMObject)
    
    
  def test_isOSMNotEqualWrongWay(self):
    #Deliberatly not using the self variables to make sure it is filled with
    #other objects
    compareNode = osmData.Node(1, 0.1, 2.1, {"highway":"traffic_signals"})
    compareWay = osmData.Way(3, [1,2,4], {"highway":"residential","name":"Clipstone Street"})
    compareRelation = osmData.Relation(5, [("way",8125151,"outer"),("way",249285853,"inner")], 
                                             {"name":"Tween Pond", "natural":"water"})
    compareOSMObject = osmData.OSM()
    compareOSMObject.addNode(compareNode)
    compareOSMObject.addWay(compareWay)
    compareOSMObject.addRelation(compareRelation)
    self.assertNotEqual(self.testOSM, compareOSMObject)
    
    
  def test_isOSMNotEqualWrongRelation(self):
    #Deliberatly not using the self variables to make sure it is filled with
    #other objects
    compareNode = osmData.Node(2, 0.1, 2.1, {"highway":"traffic_signals"})
    compareWay = osmData.Way(3, [1,2,3], {"highway":"residential","name":"Clipstone Street"})
    compareRelation = osmData.Relation(8, [("way",8125151,"outer"),("way",249285853,"inner")], 
                                             {"name":"Tween Pond", "natural":"water"})
    compareOSMObject = osmData.OSM()
    compareOSMObject.addNode(compareNode)
    compareOSMObject.addWay(compareWay)
    compareOSMObject.addRelation(compareRelation)
    self.assertNotEqual(self.testOSM, compareOSMObject)

if __name__ == '__main__':
  unittest.main()
