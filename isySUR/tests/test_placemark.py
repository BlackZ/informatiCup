# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 15:17:08 2014

@author: jpoeppel & adreyer
"""


import unittest
from isySUR import kmlData
from isySUR import osmData
#import lxml.etree as ET


class TestPlacemarkObject(unittest.TestCase):
  
  def setUp(self):
    self.testName = "0002"
    self.imageName = "0002.jpg"
    self.ruleType = ("key", "value")
    self.pointList = ["4.12,52.12","4.12,52.13","4.13,52.12"]
    self.testStyle = "#defaultStyle"
    self.testCoords = (1.2345,9,876)

  def test_createPlacemark(self):  
    placemarkObj = kmlData.Placemark(self.testName, self.imageName, self.ruleType)
    self.assertIsNotNone(placemarkObj)
    self.assertEqual(placemarkObj.name, self.testName)
    self.assertEqual(placemarkObj.ruleType, self.ruleType)
    self.assertEqual(placemarkObj.style, self.testStyle)
    self.assertIsNotNone(placemarkObj.polygon)
    self.assertEqual(len(placemarkObj.polygon),0)
    self.assertIsNone(placemarkObj.ruleCoords)
    
  def test_createPlacemarkWithCoordinates(self):  
    placemarkObj = kmlData.Placemark(self.testName, self.imageName, self.ruleType, ruleCoords = self.testCoords)
    self.assertIsNotNone(placemarkObj)
    self.assertEqual(placemarkObj.name, self.testName)
    self.assertEqual(placemarkObj.ruleType, self.ruleType)
    self.assertEqual(placemarkObj.style, self.testStyle)
    self.assertIsNotNone(placemarkObj.polygon)
    self.assertEqual(len(placemarkObj.polygon),0)
    self.assertEqual(placemarkObj.ruleCoords, self.testCoords)
    
  def test_createPlacemarkWithPolygon(self):
    placemarkObj = kmlData.Placemark(self.testName, self.imageName, self.ruleType, self.pointList)
    self.assertIsNotNone(placemarkObj)
    self.assertEqual(placemarkObj.name, self.testName)
    self.assertEqual(placemarkObj.ruleType, self.ruleType)
    self.assertIsNotNone(placemarkObj.polygon)
    self.assertEqual(len(placemarkObj.polygon),len(self.pointList))
    self.assertEqual(placemarkObj.polygon, self.pointList)
    
  def test_createPlacemarkFailNotList(self):
    with self.assertRaises(TypeError):
      placemarkObj = kmlData.Placemark(self.testName, self.imageName, self.ruleType, 42)
      
  def test_createPlacemarkFailNotTuple(self):
    with self.assertRaises(TypeError):
      placemarkObj = kmlData.Placemark(self.testName, self.imageName, self.ruleType, ruleCoords = "abs")
        
  def test_addPoint(self):
    placemarkObj = kmlData.Placemark(self.testName, self.imageName, self.ruleType)
    placemarkObj.addPoint(self.pointList[0])
    self.assertEqual(len(placemarkObj.polygon),1)
    self.assertEqual(placemarkObj.polygon[-1], self.pointList[0])
    
  def test_addPointFailIntGiven(self):
    placemarkObj = kmlData.Placemark(self.testName, self.imageName, self.ruleType)
    with self.assertRaises(TypeError):
      placemarkObj.addPoint(42)
    
  def test_hasPolygonFailNoPoints(self):
    placemarkObj = kmlData.Placemark(self.testName, self.imageName, self.ruleType)
    self.assertFalse(placemarkObj.hasPolygon())

  def test_hasPolygonFailWith2Points(self):
    placemarkObj = kmlData.Placemark(self.testName, self.imageName, self.ruleType)
    placemarkObj.addPoint(self.pointList[0])  
    placemarkObj.addPoint(self.pointList[1])
    self.assertFalse(placemarkObj.hasPolygon())    
    
  def test_hasPolygon(self):
    placemarkObj = kmlData.Placemark(self.testName, self.imageName, self.ruleType, self.pointList)
    self.assertTrue(placemarkObj.hasPolygon())    

  def test_addPointList(self):
    placemarkObj = kmlData.Placemark(self.testName, self.imageName, self.ruleType)
    placemarkObj.addPointList(self.pointList)
    for point in self.pointList:
      self.assertTrue(point in placemarkObj.polygon)
  
  def test_addPointListFailNoOtherNodesAffected(self):
    firstPoint = "123.2,312.5"
    placemarkObj = kmlData.Placemark(self.testName, self.imageName, self.ruleType, [firstPoint])
    placemarkObj.addPointList(self.pointList)
    self.assertEqual(len(placemarkObj.polygon), len(self.pointList) + 1)
    self.assertTrue(firstPoint in placemarkObj.polygon)
    
  def test_getXMLTree(self):
    placemarkObj = kmlData.Placemark(self.testName, self.imageName, self.ruleType, self.pointList)
    tree = placemarkObj.getXMLTree()
    self.assertEqual(tree.tag, "Placemark")
    nameE = tree.find("name")
    self.assertIsNotNone(nameE)
    self.assertEqual(nameE.text, self.testName)
    trueDescription = "<img src='" + self.imageName + "' width = '400' />"
    descriptionE = tree.find("description")
    self.assertIsNotNone(descriptionE)
    self.assertEqual(descriptionE.text, trueDescription)
    styleE = tree.find("styleUrl")
    trueStyle = "#defaultStyle"
    self.assertIsNotNone(styleE)
    self.assertEqual(styleE.text, trueStyle)
    polygonE = tree.find("Polygon")
    self.assertIsNotNone(polygonE)
    altitudeE = polygonE.find("altitudeMode")
    trueAltitude = "clampToGround"
    self.assertIsNotNone(altitudeE)
    self.assertEqual(altitudeE.text, trueAltitude)
    extrudeE = polygonE.find("extrude")
    self.assertIsNotNone(extrudeE)
    self.assertEqual(extrudeE.text, "1")
    tessellateE = polygonE.find("tessellate")
    self.assertIsNotNone(tessellateE)
    self.assertEqual(tessellateE.text, "1")
    outerBoundE = polygonE.find("outerBoundaryIs")
    self.assertIsNotNone(outerBoundE)
    linRingE = outerBoundE.find("LinearRing")
    self.assertIsNotNone(linRingE)
    coordsE = linRingE.find("coordinates")
    trueCoords = "\n".join(self.pointList)
    trueCoords += "\n"+self.pointList[0]
    self.assertIsNotNone(coordsE)
    self.assertEqual(coordsE.text, trueCoords)
    
    
if __name__ == '__main__':
  unittest.main()
