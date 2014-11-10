# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 12:53:23 2014

@author: jpoeppel & adreyer
"""

import unittest
import osmData

class TestRelationObject(unittest.TestCase):
  
  def setUp(self):
    self.id = 1
    self.members = [("way",8125151,"outer"),("way",249285853,"inner")]
    self.tags = {"name":"Tween Pond", "natural":"water"}
    
  
  def test_createRelation(self):
    testRelation = osmData.Relation(self.id, self.members, self.tags)
    self.assertIsNotNone(testRelation)
    self.assertEqual(testRelation.id, self.id)
    self.assertEqual(testRelation.members, self.members)
    self.assertEqual(testRelation.tags, self.tags)
    
  def test_createRelationFail(self):
    testRelation = osmData.Relation(23, self.members[0], self.tags)
    self.assertNotEqual(testRelation.id, self.id)
    self.assertNotEqual(testRelation.members, self.members)
    self.assertEqual(testRelation.tags, self.tags)
  
  def test_isRelationEqual(self):
    testRelation = osmData.Relation(self.id, self.members, self.tags)
    #Deliberatly not using the self variables to make sure it is filled with
    #other objects
    otherRelation = osmData.Relation(1, 
                  [("way",8125151,"outer"),("way",249285853,"inner")], 
                   {"name":"Tween Pond", "natural":"water"})
    self.assertEqual(testRelation, otherRelation)
    
  def test_isRelationNotEqual(self):
    testRelation = osmData.Relation(self.id, self.members, self.tags)
    #Deliberatly not using the self variables to make sure it is filled with
    #other objects
    otherRelation = osmData.Relation(2, 
                  [("way",8125151,"outer"),("way",249285853,"inner")], 
                   {"name":"Tween Pond", "natural":"water"})
    self.assertNotEqual(testRelation, otherRelation)

if __name__ == '__main__':
  unittest.main()
