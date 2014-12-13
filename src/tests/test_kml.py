# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 14:10:52 2014

@author: jpoeppel & adreyer
"""

import unittest
import kmlData
import osmData
import os

class TestKMLObject(unittest.TestCase):
  
  def setUp(self):
    self.testPlacemarks = [(kmlData.Placemark("0002", ("smoking","no"), 
                        [osmData.Node(1, 52.12, 4.12, {}), osmData.Node(2, 52.13, 4.12, {}), osmData.Node(3, 52.12, 4.13, {})]))]
    

  def test_createKML(self):  
    kmlObj = kmlData.KMLObject()
    self.assertIsNotNone(kmlObj)
    self.assertIsNotNone(kmlObj.placemarks)
    
    
  def test_createKMLWithPlacemark(self):
    kmlObj = kmlData.KMLObject(self.testPlacemarks)
    self.assertIsNotNone(kmlObj)
    self.assertIsNotNone(kmlObj.placemarks)
    self.assertEqual(len(kmlObj.placemarks), 1)
    self.assertEqual(kmlObj.placemarks, self.testPlacemarks)
    
    
  def test_addPlacemark(self):
    kmlObj = kmlData.KMLObject()
    kmlObj.addPlacemark(self.testPlacemarks[0])
    self.assertEqual(len(kmlObj.placemarks), 1)
    self.assertEqual(kmlObj.placemarks[-1], self.testPlacemarks[0])
    
  def test_addPlacemarkList(self):
    testPlacemark2=kmlData.Placemark("0003", ("smoking","no"), 
                        [osmData.Node(1, 52.12, 4.12, {}), osmData.Node(2, 52.13, 4.12, {}), osmData.Node(3, 52.12, 4.13, {})])
    testPlacemark3=kmlData.Placemark("0004", ("smoking","no"), 
                        [osmData.Node(1, 52.12, 4.12, {}), osmData.Node(2, 52.13, 4.12, {}), osmData.Node(3, 52.12, 4.13, {})])
    testPlacemark4=kmlData.Placemark("0005", ("smoking","no"), 
                        [osmData.Node(1, 52.12, 4.12, {}), osmData.Node(2, 52.13, 4.12, {}), osmData.Node(3, 52.12, 4.13, {})])
    kmlObj=kmlData.KMLObject()
    kmlObj.addPlacemarkList([self.testPlacemarks[0], testPlacemark2, testPlacemark3])
    self.assertEqual(len(kmlObj.placemarks),3)
    self.assertTrue(self.testPlacemarks[0] in kmlObj.placemarks)
    self.assertTrue(testPlacemark2 in kmlObj.placemarks)
    self.assertTrue(testPlacemark3 in kmlObj.placemarks)
    self.assertFalse(testPlacemark4 in kmlObj.placemarks)
    
    
  def test_parseKML(self):
    filename="../testData/dataOnlyForTests/TestOfKml.kml"
    name1="0001"
    name2="0002"
    style="#Poly1"
    node11=osmData.Node(1,50.93030430,5.33897540,{})
    node12=osmData.Node(2,50.93033890,5.33890610,{})
    node13=osmData.Node(3,50.93035480,5.33892360,{})
    node21=node12
    node22=node13
    node23=osmData.Node(4,50.93040040,5.33897360,{})
    
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
    
  def test_parseKMLWithInvalidDataFile(self):
    filename="../testData/dataOnlyForTests/TestOfInvalidKml.kml"
    with self.assertRaises(IOError):
      testKML = kmlData.KMLObject.parseKML(filename);
    
    
  def test_getXML(self):
    filename="../testData/dataOnlyForTests/TestOfKmlUnformatted.kml"
    truthFile = open(filename)
    #Read string from file and remove potential windows return char \r. Also remove
    #last \n that is added from the read function.
    truthString = truthFile.read().replace("\r","").rstrip("\n")
    kmlObj = kmlData.KMLObject.parseKML(filename);
    self.assertEqual(kmlObj.getXML(), truthString)
      
  #ask me later (mimimi)
  #def test_getAllRequiredStyles(self):
  #  self.fail()  
  

if __name__ == '__main__':
  os.chdir("..")
  unittest.main()