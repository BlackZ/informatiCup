# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 15:09:52 2014

@author: jpoeppel & adreyer
"""

import xml.etree.cElementTree as ET
import xml.sax.saxutils as xmlUtils

class KMLObject():
  """ Class representing a kml file. Holds a list of contained placemarks.
  """
  
  def __init__(self, placemarks=None):
    """
      Constructor for the KMLObject.
      
      @param placemarks: Optional paramter to initialise this KMLObject with a list of placemarks.
    """
    self.placemarks = []
    if placemarks != None:
      if not isinstance(placemarks, list):
        raise TypeError("placemarks must be a list of placemarks.")
      for p in placemarks:
        self.addPlacemark(p)
      
  def addPlacemark(self, placemark):
    """
      Function to add a placemark to this SURObject.
      
      @param placemark: The placemark object that is to be added.
      
      @raise TypeError: If the given placemark is not a Placemark object.
    """
    if not isinstance(placemark, Placemark):
      raise TypeError("addPlacemark only accepts Placemarks.")
    self.placemarks.append(placemark)
    
  def addPlacemarkList(self,placemarkList):
    """
      Function to add a list of placemarks to this SURObject.
      
      @param placemarkList: The list of placemark objects that are to be added.
      
      @raise TypeError: If the plcemarkList is not actually a list.
    """
    if not isinstance(placemarkList, list):
      raise TypeError("addPlacemarkList only accepts a list of placemarks.")
    for placemark in placemarkList:
      self.addPlacemark(placemark)
      
  @classmethod
  def parseKML(cls, filename):
    """
      Classmethod to create a KMLObject from a file.
      
      @param filename: The name (including the path) of the file.
      @type filename: String
      
      @return: The parsed KMLObject.
    """
    tree=ET.parse(filename)
    root=tree.getroot()
    nid=1
    res=cls()
    for pm in root.iter("{http://earth.google.com/kml/2.1}Placemark"):
      pmName = pm[0].text
      imageName = pmName + ".jpg"
      for img in pm.iter("{http://earth.google.com/kml/2.1}img"):
        imageName = img.attrib["src"]
      newPlacemark=Placemark(pmName, imageName ,None,None,pm[2].text)
      startlat=None
      startlon=None
      for coord in pm.iter("{http://earth.google.com/kml/2.1}coordinates"):
        coordstring = coord.text.replace(" ", "")
        nodes = filter(None, coordstring.split('\n'))
        numberOfNodes=len(nodes)
        nodeNr=0
        for node in nodes:
          nodeNr+=1
          if node.lstrip()!='':#leaves out the first and last entry because
                               #they don't hold coordinates
            pos = node.split(',')
            lon=pos[0]
            lat=pos[1]
            if startlat==None:
              startlat=lat
              startlon=lon
              newPlacemark.addPoint(node)
              nid+=1
            elif startlat!=lat or startlon!=lon:
              newPlacemark.addPoint(node)
              nid+=1
              if nodeNr==numberOfNodes:
                raise IOError("Invalid kml-file: Placemark does not start and end with the same coordinates.")
            else:
              startlat=None
              startlon=None
      res.addPlacemark(newPlacemark)
    return res
    

  def saveAsXML(self, filename):
    """
      Function to save the kml in it's xml representation in a file with the given
      filename.
      
      @param filename: The name of the file this kml should be written to.
      @type filename: String
    """    
    if not isinstance(filename, str):
      raise TypeError("filename must be a string.")
    try:
      f = open(filename, 'w')
      xmlString = self.getXML()
      f.write(xmlString)
      f.close()
    except IOError:
      raise IOError("File %s could not be found." % filename)
    
    
  def getXML(self):
    """
      Function to return the XML representation for this kml as string.
      
      @return: The String-XML representation of this kml object.
    """
    root = ET.Element("kml")
    root.attrib = {"xmlns":"http://earth.google.com/kml/2.1"}
    documentE = ET.SubElement(root, "Document")
    styleE = ET.SubElement(documentE, "Style")  
    styleE.attrib = {"id":"defaultStyle"}
    lineStyleE = ET.SubElement(styleE, "LineStyle")
    linColourE = ET.SubElement(lineStyleE, "color")
    linColourE.text = "7f0000ff"
    widthE = ET.SubElement(lineStyleE, "width")
    widthE.text = "2"
    polyStyleE = ET.SubElement(styleE, "PolyStyle")
    polyColourE = ET.SubElement(polyStyleE, "color")
    polyColourE.text = "7fff0000"
    
    for p in self.placemarks:
      documentE.append(p.getXMLTree())
    return '<?xml version="1.0" encoding="UTF-8"?>' + xmlUtils.unescape(ET.tostring(root, encoding='utf-8'))
    
  
class Placemark():
  
  def __init__(self, name, imageName, ruleType=None, pointList=None, style="#defaultStyle"):
    """
      Constructor for the Placemark class.
      
      Contains a list of nodes that make up the polygon for this placemark.
      
      @param name: The name of the placemark.
      @type name: String
      
      @param imageName: The name/src of the image in the placemark description.
      @type imageName: String
      
      @param ruleType: The rule type of the placemark. (Currently not used)
      @type ruleType: Tupel(key, value)
      
      @param pointList: Optional pointList that contains the points coordinates that make 
                          up the polygon this placemark describes.
      
      @param style: Optional style for the placemark. Relevant for displaying the placemark in googleEarth. 
                (Currently not used)
      @type style: String.
    """
    self.name = name
    self.ruleType = ruleType
    self.style = style
    self.polygon = []
    self.imageName = imageName
    if pointList != None:
      if not isinstance(pointList, list):
        raise TypeError("nodeList must be a list of nodes")
      self.addPointList(pointList)
    
    
  def addPoint(self, point):
    """
      Function to add a node to the polygon for the placemark.
      
      @param node: The point coordinate that is to be added to the placemark.
      
      @raise TypeError: If point is not a string.
    """
    if not isinstance(point, str):
      raise TypeError("addPoint only accepts strings for the point coordinates.")
    self.polygon.append(point)
  
  def addPointList(self, pointList):
    """
      Function to add a list of nodes to the polygon of the placemark.
      
      @param pointList: The list of point coordinates that are to be added.
      
      @raise TypeError: If pointList is not a list.
    """
    if not isinstance(pointList, list):
      raise TypeError("addNodeList only accepts a list of nodes.")
    for point in pointList:
      self.addPoint(point)
  
  def hasPolygon(self):
    """
      Function to check if a placemark contains a valid polygon.
      
      A polygon is considered as valid as soon as it contains at least 3 nodes.
      
      @return: True if the polygon consists of at least 3 nodes, else False.
    """
    if len(self.polygon) > 2:
      return True
    else:
      return False
      
  def getXMLTree(self):
    """
      Function to get the xmlTree representation of the placemark.
      
      @return: A xmlTree (xml.etree) representation of the placemark.
    """
    root = ET.Element("Placemark")
    
    name = ET.SubElement(root, "name")
    name.text = self.name
    
    description = ET.SubElement(root, "description")
    #Add this line by hand in order to be able to compare with truth string better.
    #Results in having to unescape the <> in the kmlObject though
    description.text ="<img src='"+ self.imageName + "' width = '400' />"
#    image = ET.SubElement(description, "img")
#    image.attrib["src"] = self.name
#    image.attrib["width"] = '400'
    style = ET.SubElement(root, "styleUrl")
    style.text = self.style
    
    polygon = ET.SubElement(root, "Polygon")
    altitudeMode = ET.SubElement(polygon, "altitudeMode")
    altitudeMode.text = "clampToGround"
    extrude = ET.SubElement(polygon, "extrude")
    extrude.text = str(1)
    tessellate = ET.SubElement(polygon, "tessellate")
    tessellate.text = str(1)
    outerBoundary = ET.SubElement(polygon, "outerBoundaryIs")
    linearRing = ET.SubElement(outerBoundary, "LinearRing")
    
    coordinates = ET.SubElement(linearRing, "coordinates")
    coordinates.text = "\n".join(self.polygon)
    #Placemark polygons are supposed to close with the starting coordinates again.
    coordinates.text += "\n" + self.polygon[0]
    
    return root
    
  
