# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 15:17:08 2014

@author: jpoeppel & adreyer
"""


import unittest
import kmlData
import osmData
#import lxml.etree as ET
import xml.etree.cElementTree as ET
import xml.sax.saxutils as xmlUtils

class TestPlacemarkObject(unittest.TestCase):
  
  def setUp(self):
    self.testName = "0002"
    self.ruleType = ("key", "value")
    self.nodeList = [osmData.Node(1, 52.12, 4.12, {}), osmData.Node(2, 52.13, 4.12, {}), osmData.Node(3, 52.12, 4.13, {})]
    self.testStyle = "defaultStyle"

  def test_createPlacemark(self):  
    placemarkObj = kmlData.Placemark(self.testName, self.ruleType)
    self.assertIsNotNone(placemarkObj)
    self.assertEqual(placemarkObj.name, self.testName)
    self.assertEqual(placemarkObj.ruleType, self.ruleType)
    self.assertEqual(placemarkObj.style, self.testStyle)
    self.assertIsNotNone(placemarkObj.polygon)
    self.assertEqual(len(placemarkObj.polygon),0)
    
  def test_createPlacemarkWithPolygon(self):
    placemarkObj = kmlData.Placemark(self.testName, self.ruleType, self.nodeList)
    self.assertIsNotNone(placemarkObj)
    self.assertEqual(placemarkObj.name, self.testName)
    self.assertEqual(placemarkObj.ruleType, self.ruleType)
    self.assertIsNotNone(placemarkObj.polygon)
    self.assertEqual(len(placemarkObj.polygon),len(self.nodeList))
    
  def test_createPlacemarkFailNotList(self):
    with self.assertRaises(TypeError):
      placemarkObj = kmlData.Placemark(self.testName, self.ruleType, 42)
        
  def test_addNode(self):
    placemarkObj = kmlData.Placemark(self.testName, self.ruleType)
    placemarkObj.addNode(self.nodeList[0])
    self.assertEqual(len(placemarkObj.polygon),1)
    self.assertEqual(placemarkObj.polygon[-1], self.nodeList[0])
    
  def test_addNodeFailStringGiven(self):
    placemarkObj = kmlData.Placemark(self.testName, self.ruleType)
    with self.assertRaises(TypeError):
      placemarkObj.addNode(self.testName)
    
  def test_hasPolygonFailNoNodes(self):
    placemarkObj = kmlData.Placemark(self.testName, self.ruleType)
    self.assertFalse(placemarkObj.hasPolygon())

  def test_hasPolygonFailWith2Nodes(self):
    placemarkObj = kmlData.Placemark(self.testName, self.ruleType)
    placemarkObj.addNode(self.nodeList[0])  
    placemarkObj.addNode(self.nodeList[1])
    self.assertFalse(placemarkObj.hasPolygon())    
    
  def test_hasPolygon(self):
    placemarkObj = kmlData.Placemark(self.testName, self.ruleType, self.nodeList)
    self.assertTrue(placemarkObj.hasPolygon())    

  def test_addNodeList(self):
    placemarkObj = kmlData.Placemark(self.testName, self.ruleType)
    placemarkObj.addNodeList(self.nodeList)
    for node in self.nodeList:
      self.assertTrue(node in placemarkObj.polygon)
  
  def test_addNodeListFailNoOtherNodesAffected(self):
    firstNode = osmData.Node(4,123.2,312.5,{})
    placemarkObj = kmlData.Placemark(self.testName, self.ruleType, [firstNode])
    placemarkObj.addNodeList(self.nodeList)
    self.assertEqual(len(placemarkObj.polygon), len(self.nodeList) + 1)
    self.assertTrue(firstNode in placemarkObj.polygon)
    
  def test_getXMLTree(self):
    placemarkObj = kmlData.Placemark(self.testName, self.ruleType, self.nodeList)
    tree = placemarkObj.getXMLTree()
    self.assertEqual(tree.tag, "Placemark")
    nameE = tree.find("name")
    self.assertIsNotNone(nameE)
    self.assertEqual(nameE.text, self.testName)
    trueDescription = "<img src='" + self.testName + ".jpg' width = '400' />"
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
    trueCoords = "\n".join([n.getCoordinateString() for n in self.nodeList])
    trueCoords += "\n"+self.nodeList[0].getCoordinateString()
    self.assertIsNotNone(coordsE)
    self.assertEqual(coordsE.text, trueCoords)
    
    
if __name__ == '__main__':
  unittest.main()
