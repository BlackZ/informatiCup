# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 14:10:52 2014

@author: jpoeppel & adreyer
"""

import unittest
from isySUR import kmlData
import xml.etree.cElementTree as ET
import os

class TestKMLObject(unittest.TestCase):
  
  def setUp(self):
    self.testPlacemarks = [kmlData.Placemark("0002", ("smoking","no"), 
                        ["4.12,52.12","4.12,52.13","4.13,52.12"])]
    self.kmlName = "testKml"
    

  def test_createKML(self):  
    kmlObj = kmlData.KMLObject(self.kmlName)
    self.assertIsNotNone(kmlObj)
    self.assertIsNotNone(kmlObj.placemarks)
    self.assertEqual(kmlObj.name, self.kmlName)
    
  def test_createKMLWithPlacemark(self):
    kmlObj = kmlData.KMLObject(self.kmlName, self.testPlacemarks)
    self.assertIsNotNone(kmlObj)
    self.assertIsNotNone(kmlObj.placemarks)
    self.assertEqual(len(kmlObj.placemarks), 1)
    self.assertEqual(kmlObj.placemarks, self.testPlacemarks)
    
    
  def test_addPlacemark(self):
    kmlObj = kmlData.KMLObject(self.kmlName)
    kmlObj.addPlacemark(self.testPlacemarks[0])
    self.assertEqual(len(kmlObj.placemarks), 1)
    self.assertEqual(kmlObj.placemarks[-1], self.testPlacemarks[0])
    
  def test_addPlacemarkList(self):
    testPlacemark2=kmlData.Placemark("0003", ("smoking","no"), 
                        ["4.12,52.12","4.12,52.13","4.13,52.12"])
    testPlacemark3=kmlData.Placemark("0004", ("smoking","no"), 
                        ["4.12,52.12","4.12,52.13","4.13,52.12"])
    testPlacemark4=kmlData.Placemark("0005", ("smoking","no"), 
                        ["4.12,52.12","4.12,52.13","4.13,52.12"])
    kmlObj=kmlData.KMLObject(self.kmlName)
    kmlObj.addPlacemarkList([self.testPlacemarks[0], testPlacemark2, testPlacemark3])
    self.assertEqual(len(kmlObj.placemarks),3)
    self.assertTrue(self.testPlacemarks[0] in kmlObj.placemarks)
    self.assertTrue(testPlacemark2 in kmlObj.placemarks)
    self.assertTrue(testPlacemark3 in kmlObj.placemarks)
    self.assertFalse(testPlacemark4 in kmlObj.placemarks)
    
    
  def test_parseKML2_1(self):
    filename="testData/dataOnlyForTests/TestOfKml.kml"
    kmlName = "TestOfKml.kml"
    name1="0001"
    name2="0002"
    style="#Poly1"
    polyColour ="7f00ff00"
    point11 = "5.33897540,50.93030430"

    point12 = "5.33890610,50.93033890"

    point13 = "5.33892360,50.93035480"

    point21 = point12
    point22 = point13

    point23 = "5.33897360,50.93040040"
    
    testKML = kmlData.KMLObject.parseKML(filename)    
    
    self.assertEqual(len(testKML.placemarks),2)
    self.assertEqual(testKML.placemarks[0].name,name1)
    self.assertEqual(testKML.placemarks[0].style,style)
    self.assertEqual(len(testKML.placemarks[0].polygon),3)
    self.assertEqual(testKML.placemarks[0].polygon[0],point11)
    self.assertEqual(testKML.placemarks[0].polygon[1],point12)
    self.assertEqual(testKML.placemarks[0].polygon[2],point13)
    
    self.assertEqual(testKML.placemarks[1].name,name2)
    self.assertEqual(testKML.placemarks[1].style,style)
    self.assertEqual(len(testKML.placemarks[1].polygon),3)
    self.assertEqual(testKML.placemarks[1].polygon[0],point21)
    self.assertEqual(testKML.placemarks[1].polygon[1],point22)
    self.assertEqual(testKML.placemarks[1].polygon[2],point23)
    self.assertTrue(testKML.styles.has_key("Poly1"))
    self.assertEqual(testKML.styles["Poly1"]["polyColour"], polyColour)
    self.assertEqual(testKML.name, kmlName)    
    
  def test_parseKML2_2(self):
    filename="testData/dataOnlyForTests/TestOfKml2_2.kml"
    kmlName = "TestOfKml2_2.kml"
    name1="0049"
    style="#Poly10"
    point1 = "5.36569825321936,50.93923090709453"

    point2 = "5.366281448276046,50.93917323443537"

    point3 = "5.366351933439293,50.93953260729314"
    point4 = "5.36576126354174,50.9395691930783"

    
    testKML = kmlData.KMLObject.parseKML(filename)
    self.assertEqual(len(testKML.placemarks),1)
    self.assertEqual(testKML.placemarks[0].name,name1)
    self.assertEqual(testKML.placemarks[0].style,style)
    self.assertEqual(len(testKML.placemarks[0].polygon),4)
    self.assertEqual(testKML.placemarks[0].polygon[0],point1)
    self.assertEqual(testKML.placemarks[0].polygon[1],point2)
    self.assertEqual(testKML.placemarks[0].polygon[2],point3)
    self.assertEqual(testKML.placemarks[0].polygon[3],point4)
    self.assertTrue(testKML.styles.has_key("Poly10"))
    self.assertEqual(testKML.name, kmlName)
    
    
  def test_addPolyStyleWithDefaultLine(self):
    testStyle = {"Poly1": {"polyColour":"7fff0000"}, "Poly10":{"polyColour":"ff7f00ff"}}
    kmlObj = kmlData.KMLObject(self.kmlName)
    kmlObj.addStyles(testStyle)
    self.assertTrue(kmlObj.styles.has_key("Poly1"))
    self.assertTrue(kmlObj.styles.has_key("Poly10"))
    self.assertEqual(kmlObj.styles["Poly1"]["polyColour"], testStyle["Poly1"]["polyColour"])
    self.assertEqual(kmlObj.styles["Poly1"]["lineColour"], "9900ff00")
    self.assertEqual(kmlObj.styles["Poly1"]["lineWidth"], "2")
    
  def test_addPolyStyle(self):
    testStyle = {"Poly1": {"polyColour":"7fff0000", "lineColour":"00ff7f00", "lineWidth":"2"}}
    kmlObj = kmlData.KMLObject(self.kmlName)
    kmlObj.addStyles(testStyle)
    self.assertTrue(kmlObj.styles.has_key("Poly1"))
    self.assertEqual(kmlObj.styles["Poly1"]["polyColour"], testStyle["Poly1"]["polyColour"])
    self.assertEqual(kmlObj.styles["Poly1"]["lineColour"], testStyle["Poly1"]["lineColour"])
    self.assertEqual(kmlObj.styles["Poly1"]["lineWidth"], testStyle["Poly1"]["lineWidth"])
    
    
  def test_parseKML21Coords(self):
    testString = "5.5,50.9\n5.3,50.8\n4.2,49.9\n5.5,50.9\n"
    truthPointList= ["5.5,50.9","5.3,50.8","4.2,49.9"]
    self.assertEqual(truthPointList, kmlData.KMLObject._parseKML21Coords(testString))
    
  def test_parseKML21CoordsFailNoPolygon(self):
    testString = "5.5,50.9\n5.3,50.8\n4.2,49.9\n"
    with self.assertRaises(IOError):
      kmlData.KMLObject._parseKML21Coords(testString)
      
  def test_parse22Styles(self):
    filename = "testData/dataOnlyForTests/TestOfKml2_2.kml"
    trueStyles = {"Poly10":{"polyColour":"7f00ff00","lineColour":"7f00ff00","lineWidth":"2"}}
    tree=ET.parse(filename)  
    root=tree.getroot()
    stylesToParse = ["Poly10"]
    namespace = root.tag[:root.tag.find("}")+1]
    styles = kmlData.KMLObject._parse22Styles(root, namespace, stylesToParse)
    self.assertEqual(styles, trueStyles)
    
  def test_parse22StylesStyleInStyleMap(self):
    filename = "testData/dataOnlyForTests/TestOfKml2_2StyleInStyleMap.kml"
    trueStyles = {"Poly10":{"polyColour":"7f00ff00","lineColour":"7f00ff00","lineWidth":"2"}}
    tree=ET.parse(filename)  
    root=tree.getroot()
    stylesToParse = ["Poly10"]
    namespace = root.tag[:root.tag.find("}")+1]
    styles = kmlData.KMLObject._parse22Styles(root, namespace, stylesToParse)
    self.assertEqual(styles, trueStyles)
    
  def test_parse22StylesMultipleStyles(self):
    filename = "testData/dataOnlyForTests/TestOfKml2_2MultipleStyles.kml"
    trueStyles = {"Poly10":{"polyColour":"7f00ff00","lineColour":"7f00ff00","lineWidth":"2"},
                  "Poly20":{"polyColour":"7f00ffff","lineColour":"7f00ff00","lineWidth":"2"}}
    tree=ET.parse(filename)  
    root=tree.getroot()
    stylesToParse = ["Poly10","Poly20"]
    namespace = root.tag[:root.tag.find("}")+1]
    styles = kmlData.KMLObject._parse22Styles(root, namespace, stylesToParse)
    self.assertEqual(styles, trueStyles)
    
  def test_parse22StylesMultipleStylesIgnoreSome(self):
    filename = "testData/dataOnlyForTests/TestOfKml2_2MultipleStyles.kml"
    trueStyles = {"Poly1":{"polyColour":"7f00ff00","lineColour":"7f00ff00","lineWidth":"2"},
                  "Poly2":{"polyColour":"7f00ffff","lineColour":"7f00ff00","lineWidth":"2"}}
    tree=ET.parse(filename)  
    root=tree.getroot()
    stylesToParse = ["Poly1"]
    namespace = root.tag[:root.tag.find("}")+1]
    styles = kmlData.KMLObject._parse22Styles(root, namespace, stylesToParse)
    self.assertNotEqual(styles, trueStyles)
    self.assertTrue(styles.has_key("Poly1"))
    
  def test_parseStyles(self):
    filename = "testData/dataOnlyForTests/TestOfKml.kml"
    trueStyles = {"Poly1":{"polyColour":"7f00ff00","lineColour":"7f00ff00","lineWidth":"2"}}
    tree=ET.parse(filename)  
    root=tree.getroot()
    stylesToParse = ["Poly1"]
    namespace = root.tag[:root.tag.find("}")+1]
    styles = kmlData.KMLObject._parseStyles(root, namespace)
    self.assertEqual(styles, trueStyles)
    
  def test_parseStylesMultipleStyles(self):
    filename = "testData/dataOnlyForTests/TestOfKml2Styles.kml"
    trueStyles = {"Poly1":{"polyColour":"7f00ff00","lineColour":"7f00ff00","lineWidth":"2"},
                  "Poly2":{"polyColour":"7f00ffff","lineColour":"7f00ff00","lineWidth":"2"}}
    tree=ET.parse(filename)  
    root=tree.getroot()
    stylesToParse = ["Poly1","Poly2"]
    namespace = root.tag[:root.tag.find("}")+1]
    styles = kmlData.KMLObject._parseStyles(root, namespace)
    self.assertEqual(styles, trueStyles)
    
  def test_parseStylesMultipleStylesIgnoreSome(self):
    filename = "testData/dataOnlyForTests/TestOfKml2Styles.kml"
    trueStyles = {"Poly1":{"polyColour":"7f00ff00","lineColour":"7f00ff00","lineWidth":"2"},
                  "Poly2":{"polyColour":"7f00ffff","lineColour":"7f00ff00","lineWidth":"2"}}
    tree=ET.parse(filename)  
    root=tree.getroot()
    stylesToParse = ["Poly1"]
    namespace = root.tag[:root.tag.find("}")+1]
    styles = kmlData.KMLObject._parseStyles(root, namespace, stylesToParse)
    self.assertNotEqual(styles, trueStyles)
    self.assertTrue(styles.has_key("Poly1"))
    
  def test_parseKML22Coords(self):
    testString = "5.3,50.9,0 5.4,50.9,0 5.1,50.7,0 5.3,50.9,0 "
    truthPointList= ["5.3,50.9","5.4,50.9","5.1,50.7"]
    self.assertEqual(truthPointList, kmlData.KMLObject._parseKML22Coords(testString))
    
  def test_parseKML22CoordsFailNoPolygon(self):
    testString = "5.3,50.9,0 5.4,50.9,0 5.1,50.7,0 "
    with self.assertRaises(IOError):
      kmlData.KMLObject._parseKML22Coords(testString)
    
  def test_parseKMLTruth40(self):
    filename="testData/dataOnlyForTests/truth40.kml"
    name = "0040"
    testKML = kmlData.KMLObject.parseKML(filename)
    self.assertEqual(len(testKML.placemarks),1)
    self.assertEqual(testKML.placemarks[0].name,name)
    
  def test_parseKMLWithInvalidDataFile(self):
    filename="testData/dataOnlyForTests/TestOfInvalidKml.kml"
    with self.assertRaises(IOError):
      testKML = kmlData.KMLObject.parseKML(filename);
      
  def test_parseKMLWithStartCoordsMultiples(self):
    filename="testData/dataOnlyForTests/TestOfKmlUnformattedMultiple.kml"
    kmlObj = kmlData.KMLObject.parseKML(filename)
    output = "testData/dataOnlyForTests/OutputMultipleKML.kml"
    kmlObj.saveAsXML(output)
    truthFile = open(filename)
    truthString = truthFile.read().replace("\r","").rstrip("\n")
    outputFile = open(output)
    outputString = outputFile.read().replace("\r","").rstrip("\n")
    self.assertEqual(outputString, truthString)
    
      
  def test_saveAsXML(self):
    filename="testData/dataOnlyForTests/TestOfKmlUnformatted.kml"
    kmlObj = kmlData.KMLObject.parseKML(filename)
    output = "testData/dataOnlyForTests/OutputKML.kml"
    kmlObj.saveAsXML(output)
    truthFile = open(filename)
    truthString = truthFile.read().replace("\r","").rstrip("\n")
    try:
      outputFile = open(output)
      outputString = outputFile.read().replace("\r","").rstrip("\n")
      self.assertEqual(outputString, truthString)
    except IOError:
      self.fail("The file was not created.")
    
  def test_saveAsXMLFailIncorrectPath(self):
    filename="testData/dataOnlyForTests/TestOfKmlUnformatted.kml"
    kmlObj = kmlData.KMLObject.parseKML(filename)
    output = "testData/WrongDir/OutputKML.kml"
    with self.assertRaises(IOError):
      kmlObj.saveAsXML(output)
    
  def test_getXML(self):
    filename="testData/dataOnlyForTests/TestOfKmlUnformatted.kml"
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
  os.chdir("../..")
#  suite = unittest.TestSuite()
#  suite.addTest(TestKMLObject("test_parseKML22CoordsFailNoPolygon"))
#  runner = unittest.TextTestRunner()
#  runner.run(suite)
  unittest.main()