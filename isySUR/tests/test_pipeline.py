# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 11:53:07 2014

@author: jhemming
"""

import unittest
from isySUR import program
from isySUR import sur
from isySUR import kmlData
import os

class TestProgrammPipeline(unittest.TestCase):
  
  def setUp(self):
    self.kmlObject = None
    self.pipeObj = program.Pipeline()
    self.SUR_with_one = sur.SUR.fromString('0001, 50.9262, 5.39680, smoking="no"')
    
    self.SUR_with_two = sur.SUR.fromString('0002, 50.9304, 5.33901, access:dog="no"')
    self.SUR_with_two.addRuleName('smoking="no"')
    
  
  def test_calcKML_simpleSUR(self):
    kml = self.pipeObj.calcKML(self.SUR_with_one)
    self.assertEqual(kml.__class__, kmlData.KMLObject)
    self.assertTrue(len(kml.placemarks)>0)
    for pl in kml.placemarks:
      self.assertTrue(pl.hasPolygon())
  
  def test_calcKML_tupleSUR(self):
    kml = self.pipeObj.calcKML(self.SUR_with_two)
    self.assertEqual(kml.__class__, kmlData.KMLObject)
    self.assertTrue(len(kml.placemarks)>0)
    for pl in kml.placemarks:
      self.assertTrue(pl.hasPolygon())
  
  def test_createBBox(self):
    centralPoint = (53.86351, 8.65816)
    upperRight = (53.86396, 8.658918)
    lowerLeft = (53.86306, 8.657402)
    
    bBox = self.pipeObj._createBBox(centralPoint)
    
    self.assertEqual([lowerLeft[0], lowerLeft[1], upperRight[0], upperRight[1]], bBox)
    
  def test_computeKMLs_OutputFile(self):
    surFilePath="testData/dataOnlyForTests/TestData3.txt"
    kmlFilePath="testData/dataOnlyForTests/Output.kml"
    self.pipeObj.computeKMLsAndStore(surFilePath, kmlFilePath)
    resultKML = kmlData.KMLObject.parseKML(kmlFilePath)
    self.assertIsNotNone(resultKML)
    
  def test_computeKMLs_OutputPath(self):
    #result should be 3 KMLs (2 individual + 1 containing all placemarks)
    surFilePath="testData/dataOnlyForTests/TestData.txt"
    kmlDirectoryPath="testData/dataOnlyForTests/"
    self.pipeObj.computeKMLsAndStore(surFilePath, kmlDirectoryPath, '')
    kmlFile1Path = "testData/dataOnlyForTests/0001.kml"
    kmlFile2Path = "testData/dataOnlyForTests/0002.kml"
    kmlFile3Path = "testData/dataOnlyForTests/complete.kml"    
    resultKML1 = kmlData.KMLObject.parseKML(kmlFile1Path)
    resultKML2 = kmlData.KMLObject.parseKML(kmlFile2Path)
    resultKML3 = kmlData.KMLObject.parseKML(kmlFile3Path)
    self.assertIsNotNone(resultKML1)
    self.assertIsNotNone(resultKML2)
    self.assertIsNotNone(resultKML3)

if __name__ == '__main__':
  os.chdir("../..")
  unittest.main()