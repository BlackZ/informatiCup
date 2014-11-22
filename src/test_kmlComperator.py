# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 11:52:04 2014

@author: adreyer
"""

import unittest
import kmlData
import kmlComperator

class TestKMLComperator(unittest.TestCase):
  
  def setUp(self):
    self.Comp = kmlComperator.kmlComperator()
  
  def test_compareWithTwoIdenticKMLs(self):
    filename="../testData/TestOfKmlComperator1.kml"
    testKML=kmlData.KML.parseKML(filename)
    res = self.Comp.compare(testKML,testKML)
    self.assertEqual(res.numberOfPlacemarks,2)
    self.assertEqual(res.percentaceOfOverlab,1)
    
  def test_compareWithTwoDifferentKMLs(self):
    filename1="../testData/TestOfKmlComperator1.kml"
    filename2="../testData/TestOfKmlComperator2.kml"
    testKML1=kmlData.KML.parseKML(filename1)
    testKML2=kmlData.KML.parseKML(filename2)
    res=self.Comp.compare(testKML1,testKML2)
    self.assertEqual(res.numberOfPlacemarks,2)
    self.assertEqual(res.percentaceOfOverlab,0.25)
    
  def test_compareWithTwoKMLsWithDiffernetNumbersOfPlacemarks(self):
    filename1="../testData/TestOfKmlComperator1.kml"
    filename2="../testData/TestOfKmlComperator3.kml"
    testKML1=kmlData.KML.parseKML(filename1)
    testKML2=kmlData.KML.parseKML(filename2)
    res=self.Comp.compare(testKML1,testKML2)
    self.assertEqual(res.numberOfPlacemarks,"different")
    self.assertEqual(res.percentaceOfOverlab,0.7857142857)#TODO check number
                                                          #of Nachkommastellen
  def test_compareWithTwoKMLsWithoutOverlap(self):
    self.fail("TODO implement")
    
  def test_compareWithTwoKMLsWithMultipleOverlaps(self):
    self.fail("TODO implement")
  
if __name__ == '__main__':
  unittest.main()