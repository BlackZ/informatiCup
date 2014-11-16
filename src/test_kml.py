# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 14:10:52 2014

@author: jpoeppel & adreyer
"""

import unittest
import kml
import osmData

class TestKMLObject(unittest.TestCase):
  
  def setUp(self):
    self.testPlacemark = kml.Placemark("0002", ("smoking","no"), 
                        [osmData.Node(1, 52.12, 4.12, {}), osmData.Node(2, 52.13, 4.12, {}), osmData.Node(3, 52.12, 4.13, {})])
    

  def test_createKML(self):  
    kmlObj = kml.KML()
    self.assertIsNotNone(kmlObj)
    self.assertIsNotNone(kmlObj.placemarks)
    
    
  def test_createKMLWithPlacemark(self):
    kmlObj = kml.KML(self.testPlacemark)
    self.assertIsNotNone(kmlObj)
    self.assertIsNotNone(kmlObj.placemarks)
    self.assertEqual(len(kmlObj.placemarks), 1)
    self.assertEqual(kmlObj.placemarks[-1], self.testPlacemark)
    
    
  def test_addPlacemark(self):
    kmlObj = kml.KML(self.testPlacemark)
    kmlObj.addPlacemark(self.testPlacemark)
    self.assertEqual(len(kmlObj.placemarks), 1)
    self.assertEqual(kmlObj.placemarks[-1], self.testPlacemark)
    
    
  def test_parseKML(self):
    self.fail()
    
  def test_getXML(self):
    self.fail()
      

  def test_getAllStyles(self):
    self.fail()  
  

if __name__ == '__main__':
  unittest.main()