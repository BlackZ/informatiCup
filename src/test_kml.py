# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 14:10:52 2014

@author: jpoeppel & adreyer
"""

import unittest
import kmlData
import osmData

class TestKMLObject(unittest.TestCase):
  
  def setUp(self):
    self.testPlacemark = kmlData.Placemark("0002", ("smoking","no"), 
                        [osmData.Node(1, 52.12, 4.12, {}), osmData.Node(2, 52.13, 4.12, {}), osmData.Node(3, 52.12, 4.13, {})])
    

  def test_createKML(self):  
    kmlObj = kmlData.KMLObject()
    self.assertIsNotNone(kmlObj)
    self.assertIsNotNone(kmlObj.placemarks)
    
    
  def test_createKMLWithPlacemark(self):
    kmlObj = kmlData.KMLObject(self.testPlacemark)
    self.assertIsNotNone(kmlObj)
    self.assertIsNotNone(kmlObj.placemarks)
    self.assertEqual(len(kmlObj.placemarks), 1)
    self.assertEqual(kmlObj.placemarks[-1], self.testPlacemark)
    
    
  def test_addPlacemark(self):
    kmlObj = kmlData.KMLObject()
    kmlObj.addPlacemark(self.testPlacemark)
    self.assertEqual(len(kmlObj.placemarks), 1)
    self.assertEqual(kmlObj.placemarks[-1], self.testPlacemark)
    
  def test_addPlacemarkList(self):
    testPlacemark2=kmlData.Placemark("0003", ("smoking","no"), 
                        [osmData.Node(1, 52.12, 4.12, {}), osmData.Node(2, 52.13, 4.12, {}), osmData.Node(3, 52.12, 4.13, {})])
    testPlacemark3=kmlData.Placemark("0004", ("smoking","no"), 
                        [osmData.Node(1, 52.12, 4.12, {}), osmData.Node(2, 52.13, 4.12, {}), osmData.Node(3, 52.12, 4.13, {})])
    testPlacemark4=kmlData.Placemark("0005", ("smoking","no"), 
                        [osmData.Node(1, 52.12, 4.12, {}), osmData.Node(2, 52.13, 4.12, {}), osmData.Node(3, 52.12, 4.13, {})])
    kmlObj=kmlData.KMLObject()
    kmlObj.addPlacemarkList([self.testPlacemark, testPlacemark2, testPlacemark3])
    self.assertEqual(len(kmlObj.placemarks),3)
    self.assertTrue(self.testPlacemark in kmlObj.placemarks)
    self.assertTrue(testPlacemark2 in kmlObj.placemarks)
    self.assertTrue(testPlacemark3 in kmlObj.placemarks)
    self.assertFalse(testPlacemark4 in kmlObj.placemarks)
    
    
  def test_parseKML(self):
    filename="../testData/dataOnlyForTests/TestOfKml.kml"
    name1="0001"
    name2="0002"
    style="#Poly1"
    node11=osmData.Node(1,5.33897540,50.93030430,{})
    node12=osmData.Node(2,5.33890610,50.93033890,{})
    node13=osmData.Node(3,5.33892360,50.93035480,{})
    node21=node12
    node22=node13
    node23=osmData.Node(4,5.33897360,50.93040040,{})
    
    testKML = kmlData.KMLObject.parseKML(filename);
    self.assertEqual(len(testKML.placemarks),2)
    self.assertEqual(testKML.placemarks[0].name,name1)
    self.assertEqual(testKML.placemarks[0].style,style)
    self.assertEqual(len(testKML.placemarks[0].polygon),3)
    self.assertEqual(testKML.placemarks[0].polygon[0].lat,node11.lat)
    self.assertEqual(testKML.placemarks[0].polygon[0].lon,node11.lon)
    self.assertEqual(testKML.placemarks[0].polygon[1].lat,node12.lat)
    self.assertEqual(testKML.placemarks[0].polygon[1].lon,node12.lon)
    self.assertEqual(testKML.placemarks[0].polygon[2].lat,node13.lat)
    self.assertEqual(testKML.placemarks[0].polygon[2].lon,node13.lon)
    
    self.assertEqual(testKML.placemarks[1].name,name2)
    self.assertEqual(testKML.placemarks[1].style,style)
    self.assertEqual(len(testKML.placemarks[1].polygon),3)
    self.assertEqual(testKML.placemarks[1].polygon[0].lat,node21.lat)
    self.assertEqual(testKML.placemarks[1].polygon[0].lon,node21.lon)
    self.assertEqual(testKML.placemarks[1].polygon[1].lat,node22.lat)
    self.assertEqual(testKML.placemarks[1].polygon[1].lon,node22.lon)
    self.assertEqual(testKML.placemarks[1].polygon[2].lat,node23.lat)
    self.assertEqual(testKML.placemarks[1].polygon[2].lon,node23.lon)
    
    
  def test_getXML(self):
    self.fail()
      
  #ask me later (mimimi)
  #def test_getAllRequiredStyles(self):
  #  self.fail()  
  

if __name__ == '__main__':
  unittest.main()