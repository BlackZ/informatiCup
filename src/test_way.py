# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 12:25:34 2014

@author: jpoeppel & adreyer
"""

import unittest
import osmData

class TestWayObject(unittest.TestCase):
  
  def setUp(self):
    self.id=1
    self.refs=[1,2,3]
    self.tags={"highway":"residential","name":"Clipstone Street"}
    
  
  def test_createWay(self):
    testWay = osmData.Way(self.id, self.refs, self.tags)
    self.assertIsNotNone(testWay)
    self.assertEqual(testWay.id, self.id)
    self.assertEqual(testWay.refs, self.refs)
    self.assertEqual(testWay.tags, self.tags)
  

if __name__ == '__main__':
  unittest.main()
