# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 11:52:04 2014

@author: adreyer
"""

import unittest
import kmlData
import kmlComperator
import Polygon

class TestKMLComperator(unittest.TestCase):
  
  def setUp(self):
    self.Comp = kmlComperator.KMLComperator()
    filename="../testData/dataOnlyForTests/TestOfKmlComperator1.kml"
    self.testKML1=kmlData.KMLObject.parseKML(filename)
    
  def test_compareNoKMLInInput(self):
    with self.assertRaises(TypeError):
      res=self.Comp.compare("test",self.testKML1)
  
  def test_compareWithTwoIdenticKMLs(self):
    res = self.Comp.compare(self.testKML1,self.testKML1)
    self.assertEqual(res.numberOfPlacemarks,1)
    self.assertEqual(res.percentaceOfOverlap,1)
    
  def test_compareWithTwoDifferentKMLs(self):
    filename="../testData/dataOnlyForTests/TestOfKmlComperator2.kml"
    testKML2=kmlData.KMLObject.parseKML(filename)
    res=self.Comp.compare(self.testKML1,testKML2)
    self.assertEqual(res.numberOfPlacemarks,1)
    self.assertEqual(res.percentaceOfOverlap,0.225)
    
  def test_compareWithTwoKMLsWithDiffernetNumbersOfPlacemarks(self):
    filename="../testData/dataOnlyForTests/TestOfKmlComperator3.kml"
    testKML2=kmlData.KMLObject.parseKML(filename)
    res=self.Comp.compare(self.testKML1,testKML2)
    self.assertEqual(res.numberOfPlacemarks,"different")
    self.assertEqual(res.percentaceOfOverlap,0.1625)
  
  def test_compareWithTwoKMLsWithMultipleOverlaps(self):
    filename="../testData/dataOnlyForTests/TestOfKmlComperator4.kml"
    testKML2=kmlData.KMLObject.parseKML(filename)
    res=self.Comp.compare(self.testKML1,testKML2)
    self.assertEqual(res.numberOfPlacemarks,1)
    self.assertEqual(res.percentaceOfOverlap,0.4)
    
  def test_compareWithTwoKMLsWithoutOverlap(self):
    filename="../testData/dataOnlyForTests/TestOfKmlComperator5.kml"
    testKML2=kmlData.KMLObject.parseKML(filename)
    res=self.Comp.compare(self.testKML1,testKML2)
    self.assertEqual(res.numberOfPlacemarks,1)
    self.assertEqual(res.percentaceOfOverlap,0)
    
class TestKMLComperatorHelpFunction(unittest.TestCase):
  
  def setUp(self):
    self.Comp = kmlComperator.KMLComperator()
    
  def test__buildPolygon(self):
    truePoly=Polygon.Polygon(((0,0),(1.5,0),(1.5,0.5),(0.5,0.5),(0.5,1.5),(0,1.5)))
    
    filename="../testData/dataOnlyForTests/TestOfKmlComperator1.kml"
    testKML=kmlData.KMLObject.parseKML(filename)    
    
    poly = self.Comp._buildPolygon(testKML)
    self.assertEqual(poly.area(),truePoly.area())
    self.assertEqual(poly.area(),(poly&truePoly).area())
    self.assertEqual(poly.area(),(poly|truePoly).area())
    
  def test__buildPolygonWithTwoPolygons(self):
    poly1=Polygon.Polygon(((0,1),(1,1),(1,2),(0,2)))    
    poly2=Polygon.Polygon(((1.5,2),(2.5,2),(2.5,3),(1.5,3)))
    truePoly=poly1|poly2
    
    filename="../testData/dataOnlyForTests/TestOfKmlComperator3.kml"
    testKML=kmlData.KMLObject.parseKML(filename)
    
    poly = self.Comp._buildPolygon(testKML)
    self.assertEqual(poly.area(),truePoly.area())
    self.assertEqual(poly.area(),(poly&truePoly).area())
    self.assertEqual(poly.area(),(poly|truePoly).area())
  
if __name__ == '__main__':
  unittest.main()