# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 15:09:52 2014

@author: jpoeppel & adreyer
"""

import xml.etree.cElementTree as ET
import xml.sax.saxutils as xmlUtils
import os

class KMLObject():
  """ Class representing a kml file. Holds a list of contained placemarks.
  """
  
  def __init__(self, name, placemarks=None):
    """
      Constructor for the KMLObject.
      
      @param name: Name of the kml.
      @type name: String
      
      @param placemarks: Optional paramter to initialise this KMLObject with a list of placemarks.
      @type placemarks: [kmlData.Placemark,]
    """
    self.name = name
    self.placemarks = []
    self.styles = {}
    if placemarks != None:
      if not isinstance(placemarks, list):
        raise TypeError("placemarks must be a list of placemarks.")
      for p in placemarks:
        self.addPlacemark(p)
        
  def addStyles(self, styles):
    """
      Function that allows to add styles to the kml. If styles does not include lineColour, or
      lineWidth, standard values are used.
      
      @param styles: The styles that are to be added.
      @type styles: {styleID: {"polyColour":value, "lineColour":value, "lineWidth":value},}
    """
    for key, value in styles.items():
      self.styles[key] = value
      if not value.has_key("lineColour"):
        self.styles[key]["lineColour"] = "7f00ff00"
      if not value.has_key("lineWidth"):
        self.styles[key]["lineWidth"] = "2"
      
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
    stylesToParse = []
    
#    fileNameIndex = filename.rfind(os.sep)
#    
#    #Mabe remove file ending
#    if fileNameIndex > 0:
#      kmlName = filename[fileNameIndex+1:]
#    else:
#      kmlName = filename
    kmlName = os.path.basename(filename)

    tree=ET.parse(filename)  
    root=tree.getroot()
    res=cls(kmlName)
    namespace = root.tag[:root.tag.find("}")+1]
    for pm in root.iter(namespace + "Placemark"):
      pmName = pm.find(namespace+"name").text
      imageName = pmName + ".jpg"
      if "2.2" in namespace:
        for desc in pm.iter(namespace + "description"):
          imageRoot = ET.fromstring(desc.text)
          imageName = imageRoot.attrib["src"]
      elif "2.1" in namespace:
        for img in pm.iter(namespace + "img"):
          imageName = img.attrib["src"]
      pmStyle = pm.find(namespace+"styleUrl")
      stylesToParse.append(pmStyle.text[1:])
      newPlacemark=Placemark(pmName, imageName, None, None, pmStyle.text)
      for coord in pm.iter(namespace + "coordinates"):
        points = []
        if "2.1" in namespace:
          points = cls._parseKML21Coords(coord.text)
        elif "2.2" in namespace:
          points = cls._parseKML22Coords(coord.text)
        else:
          raise IOError("Can only parse KML2.1 and KML2.2 files.")
        
        if len(points) > 0:
          newPlacemark.addPointList(points)
      res.addPlacemark(newPlacemark)

      styles = {}
      if "2.2" in namespace:
        styles = cls._parse22Styles(root, namespace, stylesToParse)
      elif "2.1" in namespace:
        styles = cls._parseStyles(root, namespace, stylesToParse)
      
      res.addStyles(styles)
    return res
    
  @classmethod
  def _parse22Styles(cls, root, ns, stylesToParse = []):
    """
      Helper function to parse the styles in kml2.2.
      Only "normal" styleMaps will be parsed.
      
      @param root: Root element from where to start parsing
      @type root: ET.Element
      
      @param ns: Namespace of the tags
      @type ns: String
      
      @param stylesToParse: Optional list of styleIds that are to be parsed. All are parsed if list is empty
      @type stylesToParse: [String,]
      
      @return: The parsed styles.
      @rtype: {styleID: {"polyColour":value, "lineColour":value, "lineWidth":value},}
    """
    res = {}

    tmpStyles = cls._parseStyles(root, ns)    
    for styleId in tmpStyles.keys():
      if len(stylesToParse) == 0 or styleId in stylesToParse:
        res[styleId] = tmpStyles[styleId]
    
    for styleMap in root.iter(ns +"StyleMap"):
      styleMapId = styleMap.attrib["id"]
      if len(stylesToParse) == 0 or styleMapId in stylesToParse:
        for pair in styleMap.iter(ns +"Pair"):
          if pair.find(ns+"key").text == "normal":
            styleId = ""
            style = pair.find(ns+"Style")
            if style != None:
              styleId = style.attrib["id"]
            styleUrl = pair.find(ns+"styleUrl")
            if styleUrl != None:
              styleId = styleUrl.text[1:]
            if tmpStyles.has_key(styleId):
              res[styleMapId] = tmpStyles[styleId]
              
    
    return res
    
    
    
  @classmethod
  def _parseStyles(cls, root, ns, stylesToParse=[]):
    """
      Helper function to parse the styles in kml files.
      Finds the style tags and returns them in a dictionary.
      
      @param root: Root element from where to start parsing
      @type root: ET.Element
      
      @param ns: Namespace of the tags
      @type ns: String
      
      @param stylesToParse: Optional list of styleIds that are to be parsed. All are parsed if list is empty
      @type stylesToParse: [String,]
      
      @return: The parsed styles.
      @rtype: {styleID: {"polyColour":value, "lineColour":value, "lineWidth":value},}
    """
    res = {}
    for style in root.iter(ns +"Style"):
      styleId = style.attrib["id"]
      if len(stylesToParse) == 0 or styleId in stylesToParse:
        for lineStyle in style.iter(ns +"LineStyle"):
          res[styleId] = {"lineColour": lineStyle[0].text, "lineWidth":lineStyle[1].text}
        for polyStyle in style.iter(ns +"PolyStyle"):
          res[styleId]["polyColour"] = polyStyle[0].text
    return res
    
  @classmethod
  def _parseKML22Coords(cls, coordstring):
    """
      Private classmethod to parse kml2.2 coordinates to a list of points.
      
      @param coordstring: String including the coordinates in a placemark xml.
      @type coordstring: String
      
      @return: List of points (lon,lat). Points are still strings.
      @rtype: [str,]
    """
    pointList = []
    coords = coordstring.lstrip().rstrip().split(" ")
    if coords[0] != coords[-1]:
      raise IOError("Invalid kml-file: Placemark does not start and end with the same coordinates.")
      
    pointList = [coord[:coord.rfind(',')] for coord in coords[:-1] ]
    
    return pointList
    
    
  @classmethod
  def _parseKML21Coords(cls, coordstring):
    """
      Private classmethod to parse kml2.1 coordinates to a list of points.
      
      @param coordstring: String including the coordinates in a placemark xml.
      @type coordstring: String
      
      @return: List of points (lon,lat). Points are still strings.
      @rtype: [str,]
    """
    pointList = []
    startlat=None
    startlon=None
    lastlat=None
    lastlon=None
    coordstring = coordstring.replace(" ", "")
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
          #store first lat/lon
          startlat=lat
          startlon=lon
        else:
          #store last lat/lon
          lastlat=lat
          lastlon=lon
        if nodeNr!=numberOfNodes:
          #if it's not the last node - save it
          pointList.append(node)
        elif startlat!=lastlat or startlon!=lastlon:
          #if it's the last node: check equality of first and last node
          raise IOError("Invalid kml-file: Placemark does not start and end with the same coordinates.")
          
    return pointList

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
    for styleId, style in self.styles.items():        
      styleE = ET.SubElement(documentE, "Style")  
      styleE.attrib = {"id":styleId}
      lineStyleE = ET.SubElement(styleE, "LineStyle")
      linColourE = ET.SubElement(lineStyleE, "color")
      linColourE.text = style["lineColour"]
      widthE = ET.SubElement(lineStyleE, "width")
      widthE.text = style["lineWidth"]
      polyStyleE = ET.SubElement(styleE, "PolyStyle")
      polyColourE = ET.SubElement(polyStyleE, "color")
      polyColourE.text = style["polyColour"]
    
    for p in self.placemarks:
      documentE.append(p.getXMLTree())
    return '<?xml version="1.0" encoding="UTF-8"?>' + xmlUtils.unescape(ET.tostring(root, encoding='utf-8'))
    
  
class Placemark():
  
  def __init__(self, name, imageName, ruleType=None, pointList=None, style="#defaultStyle", ruleCoords = None):
    """
      Constructor for the Placemark class.
      
      Contains a list of nodes that make up the polygon for this placemark.
      
      @param name: The name of the placemark.
      @type name: String
      
      @param imageName: The name/src of the image in the placemark description.
      @type imageName: String
      
      @param ruleType: The rule type of the placemark. (Currently not used)
      @type ruleType: Tupel(key, value)
      
      @param pointList: Optional pointList that contains the points coordinates (lon,lat) that make 
                          up the polygon this placemark describes.
      
      @param style: Optional style for the placemark. Relevant for displaying the placemark in googleEarth. 
                (Currently not used)
      @type style: String.
      
      @param ruleCoords: Optional rule coordinates (lat,lon).
      @type ruleCoords: (Float,Float)
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
    if ruleCoords != None:
      if not isinstance(ruleCoords, tuple):
        raise TypeError("ruleCoords must be a tuple of lat, lon coordinates.")
    self.ruleCoords = ruleCoords
    
  def addPoint(self, point):
    """
      Function to add a node to the polygon for the placemark.
      
      @param node: The point coordinate (lon,lat) that is to be added to the placemark. 
      
      @raise TypeError: If point is not a string.
    """
    if not isinstance(point, str):
      raise TypeError("addPoint only accepts strings for the point coordinates.")
    self.polygon.append(point)
  
  def addPointList(self, pointList):
    """
      Function to add a list of nodes to the polygon of the placemark.
      
      @param pointList: The list of point coordinates(lon,lat) that are to be added.
      
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
    
  
