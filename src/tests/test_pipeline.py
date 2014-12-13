# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 11:53:07 2014

@author: jhemming
"""

import unittest
import programm
import sur
import kmlData

class TestProgrammPipeline(unittest.TestCase):
  
  def setUp(self):
    self.kmlObject = None
    self.pipeObj = pipeObj = programm.Pipeline()
    self.SUR_with_one = sur.SUR.fromString('0001, 50.9262, 5.39680, smoking="no"')
    
    self.SUR_with_two = sur.SUR.fromString('0002, 50.9304, 5.33901, access:dog="no"')
    self.SUR_with_two.addRuleName('smoking="no"')
    
  
  def test_calcKML_simpleSUR(self):
    kml = self.pipeObj.calcKML(self.SUR_with_one)
    self.assertEqual(kml.__class__, kmlData.KMLObject)
  
  def test_calcKML_tupleSUR(self):
    kml = self.pipeObj.calcKML(self.SUR_with_two)
    self.assertEqual(kml.__class__, kmlData.KMLObject)
  
  def test_createBBox(self):
    centralPoint = (53.86351, 8.65816)
    upperRight = (53.86396, 8.658918)
    lowerLeft = (53.86306, 8.657402)
    
    bBox = self.pipeObj._createBBox(centralPoint)
    
    self.assertEqual([lowerLeft[0], lowerLeft[1], upperRight[0], upperRight[1]], bBox)


if __name__ == '__main__':
  unittest.main()