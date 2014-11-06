# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 12:53:23 2014

@author: jpoeppel & adreyer
"""

import unittest
import osmData

class TestRelationObject(unittest.TestCase):
  
  def setUp(self):
    self.id=1
    #todo: array von tripel
    self.tags=dict()
    
  
  def test_createRelation(self):
    testRelation = osmData.Node(self.id, self.lat, self.lon, self.tags)
    self.assertIsNotNone(testRelation)
    self.assertEqual(testRelation.id, self.id)
    
    self.assertEqual(testRelation.tags, self.tags)
  

if __name__ == '__main__':
  unittest.main()
