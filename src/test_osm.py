# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 11:46:54 2014

@author: jpoeppel & adreyer
"""


import unittest
import osm

class TestOSMObject(unittest.TestCase):
  
  def setUp(self):
    pass
  
  def test_createOSM(self):
    testOSM = osm.OSM()
    self.assertIsNotNone(testOSM)
    testOSM.nodes
    testOSM.ways
    testOSM.relations
  
  


if __name__ == '__main__':
  unittest.main()
