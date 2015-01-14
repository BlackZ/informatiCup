#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module containing the KMLCalculator, the main class handeling the calculation of kmls based on SUR
files. 
"""
#@author: jpoeppel 


import osmAPI as api
import osmData
import kmlData as kml
import sur
import os
import sys
import isySUR.isyUtils as isyUtils

class KMLCalculator:
  def __init__(self):
    """
      Constructor for the pipeline. Sets up the osmAPI as well as the desired bounding box, 
      that is to be used to request osm data.
    """
    self.osmAPI = api.osmAPI()
    self.osm = None
    self.heightBBox = 60
    self.widthBBox = 60
    self.maxDistance = 6.0
    self.allObjects = {}
    self.certainStyle = {"Style":{"polyColour":"9900ff00"}}
    self.uncertainStyle = {"StyleUncertain":{"polyColour":"99ff0000"}}
    
    
  def computeKMLsAndStore(self, inPath, outPath, configPath=''):
    """
      Function to compute kmls from a given file of SURs. Stores them either in one kml or in 
      individual kmls plus one containing all of them.
      
      @param inPath: Path to the file containing the SURs which areas are to be computed.
      @type inPath: String
      
      @param outPath: Path to the file or directory where the results should be saved. If outPath points
        to a file, all placemarks are stored in one kml. If outPath points to a directory, one kml for
        each SUR will be computed plus one, containing all others.
      @type outPath: String
      
      @param configPath: Optional path to a config file, containing information about the classification of rules
        (indoor, outdoor or both).
      @type configPath: String
            
    """
    isOutputDir = os.path.isdir(outPath)
    surFile = open(inPath,'r')
    try:
      surs = sur.SUR.fromFile(surFile, configPath)
    except ValueError:
      print "Invalid SUR data file: First line is no number."
      surFile.close()
      sys.exit()
    except IndexError:
      print "Not as much lines with SUR information as stated."
      surFile.close()
      sys.exit()
    surFile.close()
    completeKML = kml.KMLObject("complete.kml")
    for s in surs:
      resKML = None
      try:
        resKML = self.calcKML(s)
      except Exception, e:
        print e.message
      if resKML != None:
        if isOutputDir:
          resKML.saveAsXML(outPath + os.path.sep + s.id + '.kml')
      #TODO give kml the option to merge to kmls and change this
        completeKML.placemarks.extend(resKML.placemarks)
        completeKML.addStyles(resKML.styles)
      
    if len(completeKML.placemarks) > 0:
      if isOutputDir:
        completeKML.saveAsXML(outPath + os.path.sep + 'complete.kml')
      else:
        completeKML.saveAsXML(outPath)
    else:
      print "Error: Could not compute placemarks."
  
  def _computeKMLs(self, inPath, kmlList, stopCalc, configPath=''):
    """
    Function to compute kmls from a given file of SURs. Only needed for GUI.
    
    @param inPath: Path to the file containing the SURs which areas are to be computed.
    @type inPath: String
    
    @param kmlList: Queue for computed KMLs
    @type kmlList: Queue.Queue
    
    @param stopCalc: Queue which decides if the kml calculation should be stoped.
    @type stopCalc: Queue.Queue
    
    @param configPath: Optional path to a config file, containing information about the classification of rules
                       (indoor, outdoor or both).
    @type configPath: String
    """
    
    try:
      surFile = open(inPath,'r')
      surs = sur.SUR.fromFile(surFile, configPath)
      surFile.close()
    except:
      kmlList.put(IOError("SUR file incorrect"))
      return
    
    for s in surs:
      if not stopCalc.empty():
        break
      kmlList.put(s.id)
      try:
        kmlObj = self.calcKML(s)
      except Exception, e:
        kmlList.put(e)
        break
      if kmlObj != None:
        kmlList.put(kmlObj)
    kmlList.put('stop')
    return False
  
  def calcKML(self, surObj):
    """
      Function to work on a single sur.SUR object and computes it's kml.
      
      @param surObj: The sur object whose kml is to be calculated.
      @type surObj: sur.SUR
      
      @return: KML object containing the calculated area for the given sur. 
               Returns None if no polygon could be computed.
      @rtype: kmlData.KMLObject
    """

    print "working on sur: ", surObj.id
    coords = (surObj.latitude, surObj.longitude)
    
    #Set relativeNullPoint for lat, lon conversion
    isyUtils._relativeNullPoint = (surObj.latitude, surObj.longitude)
    
    kmlObj = kml.KMLObject(surObj.id+".kml")
    
    self.osm = self._getOSMData(surObj, coords)  

    if surObj.classification in ["I"]:
      nearObjs = self._getNearestObj(coords, {"building":"*"})
    else:
      nearObjs = self._getNearestObj(coords)
    

    print "number nearObjs", len(nearObjs)

    usedStyle = {}
    possibleWays = []
    for obj in nearObjs:
      tmpObj = obj.nearestObj
      tmpWay = None
      if tmpObj[1] == osmData.Relation:
        tmpRel = self.osm.relations[tmpObj[0]]
        for mem in tmpRel.members:
          if mem[2] == "outer":
            tmpWay = self.osm.ways[mem[1]]
            usedStyle[tmpWay.id] = self.certainStyle
      if tmpObj[1] == osmData.Way:
        tmpWay = self.osm.ways[tmpObj[0]]
        
        usedStyle[tmpWay.id] = self.certainStyle
        print "using way", tmpObj[0]
        
      if tmpWay != None and tmpWay.tags.has_key("landuse"):
#        print "is landuse"
        if tmpWay.tags["landuse"] in ["commercial", "industrial"]:
          usedStyle[tmpWay.id] = self.uncertainStyle    
          
        if tmpWay.tags["landuse"] == "residential":
          usedStyle[tmpWay.id] = self.uncertainStyle
          polyString = self._createPolyString(tmpWay)
#          print polyString
          landUseData = osmData.OSM()
          try:
            landUseData = self.osmAPI.getDataFromPoly(polyString)    
          except:
            print "Polygon data could not be loaded."
            
          if surObj.classification in ["I","IO"]:
            buildings = landUseData.getNearestWay(coords, True, {"building":"*"})
          else:
            buildings = landUseData.getNearestWay(coords, True)
          if len(buildings) > 1:
            print "more than one potential building."
          
          for build in buildings:
            tmpBuild = build.nearestObj
            if build.distance < self.maxDistance:
              tmpWay = self.osm.ways[tmpBuild[0]]
              usedStyle[tmpWay.id] = self.certainStyle
              possibleWays.append(tmpWay)
              #Set to None to prevent adding it multiple times
              tmpWay = None    
        
      
      if tmpWay != None and not tmpWay in possibleWays:
        possibleWays.append(tmpWay)


    if len(possibleWays) == 0:
      print "No ways found :-(."
      return None    
      
    buildingsIncluded = False  
    
    for way in possibleWays:
      if way.tags.viewkeys() & {"building","shop"}:
        buildingsIncluded = True
        break
    
    # Prefer buildings if rule is applicable indoor
    if buildingsIncluded and surObj.classification in ["I","IO"]:
#      print "reducing possible ways"
      possibleWays = [x for x in possibleWays if x.tags.viewkeys() & {"building", "shop"}]
      
#    print "number possible ways:", len(possibleWays)
    if len(possibleWays) > 1:
      bestWay = None
      closestDist = sys.float_info.max
      
      for way in possibleWays:
        dist = 0
        for ref in way.refs:
          dist += self.osm.nodes[ref].getDistance(coords).distance
        dist /= len(way.refs)
#        print "dist for", way.id, dist
        if dist < closestDist:
          closestDist = dist
          bestWay = way
    else:
      bestWay = possibleWays[0]
            
#    print "best way:", bestWay.id
    points = []  
    for ref in bestWay.refs[:-1]:
      points.append(self.osm.nodes[ref].getCoordinateString())
      
    if len(points) > 0:
      placemarkName = surObj.id
      for rule in surObj.ruleName:
        placemarkName += "-" + rule + ":" + surObj.ruleName[rule]
        
      placemark = kml.Placemark(placemarkName, surObj.id + ".jpg",
                          rule,
                          pointList=points, 
                          style="#"+usedStyle[bestWay.id].keys()[0],
                          ruleCoords = coords)
      kmlObj.addPlacemark(placemark)
    else:
      print "Error: No polygon found for SUR %s." % surObj.id
      return None
      
    kmlObj.addStyles(usedStyle[bestWay.id])
    
    return kmlObj
    
    
  def _createPolyString(self, way):
    """
    Create a string containing all vertices of the given way.
    
    @param way: Way which vertices will be extracted.
    @type way: osmData.Way
    
    @return: A string containing all the vertices coordinates of the polygon as lat1 lon1 lat2 lon2...
    @rtype: String
    """
    res = ""
    for ref in way.refs[:-1]:
      res += str(self.osm.nodes[ref].lat) + " " + str(self.osm.nodes[ref].lon) + " " 
      
    return res
    
  def _getOSMData(self, surObj, coords):
    """
      Private function to start with a small bounding box and increase it's size
      until data is found.
      
      @param surObj: The surObj for which we want to get the data
      @type surObj: sur.SUR
      
      @param coords: Coordinates of the sur (lat,lon)
      @type coords: Tupel (lat, lon)
      
      @return: The filled osmObject
      @rtype: osmData.OSM
    """
    bBox = self._createBBox(coords)
    storeWidth = self.widthBBox
    storeHeight = self.heightBBox
    buildingRules = [('node',['"building"','"type"!~"^route"','"type"!~"TMC"']),
             ('way',['"building"','"type"!~"^route"','"highway"!~"."','"type"!~"TMC"', '"building:part"!~"."']),
              ('relation',['"building"','"type"!~"^route"', '"type"!~"boundary"', '"boundary"!~"."','"highway"!~"."',
              '"type"!~"associatedStreet"','"type"!~"TMC"', '"building:part"!~"."'])]
    defaultRulesNoRoutes = [('node',['"type"!~"^route"','"type"!~"TMC"']),
                            ('way',['"type"!~"^route"','"highway"!~"."', '"type"!~"associatedStreet"','"type"!~"TMC"', '"building:part"!~"."']),
                ('relation',['"type"!~"^route"','"highway"!~"."','"type"!~"associatedStreet"',
                '"type"!~"TMC"','"type"!~"boundary"', '"boundary"!~"."', '"building:part"!~"."'])]
    osm = None
    if surObj.classification == "I":
      osm = self.osmAPI.performRequest(bBox, buildingRules)
    else:
      osm = self.osmAPI.performRequest(bBox, defaultRulesNoRoutes)
      
    #Increase boundingBox until we actually find SOMETHING
    while len(osm.ways) < 1:
      self.widthBBox *= 2
      self.heightBBox *= 2
      bBox = self._createBBox(coords)
      if surObj.classification == "I":
        osm = self.osmAPI.performRequest(bBox, buildingRules)
      else:
        osm = self.osmAPI.performRequest(bBox, defaultRulesNoRoutes)
        
    self.widthBBox = storeWidth
    self.heightBBox = storeHeight
    return osm
  
  def _getNearestObj(self, coords, tags={}):
    """
      Helper function to return the nearest osmObjects to the given coordinates.
      First tries to find relations, if there is no nearest relation, the nearest way, with closed
      polygon, is used.
      
      @param coords: The coordinates (lat,lon) around which the nearest objects are to be found.
      @type coords: Tuple(float,float)
      
      @param tags: Tags the nearest objects should have
      @type tags: Dict of Key:Value pars
      
      @return: A list of nearstObjects (see osmData.getNearestX for more details)
    """
    nearRelations = self.osm.getNearestRelation(coords, tags=tags)
    nearWays = self.osm.getNearestWay(coords, True, tags=tags)
#    nearestLanduses = self.osm.getNearestWay(coords, True, tags={"landuse":"residential"})
    if len(nearWays) == 0:
      nearWays = self.osm.getNearestWay(coords, True)
    if len(nearWays) == 0:
      nearWays = self.osm.getNearestWay(coords, False)

    nearObjs = nearWays[:]
    
    if len(nearRelations) > 0 and len(nearWays) > 0:
      if nearRelations[0].distance == nearWays[0].distance:
        nearObjs += nearRelations
        
    landuseObjs = []
    for nearWay in nearWays:
      way = self.osm.ways[nearWay.nearestObj[0]]
      if not way.isInside(coords) and nearWay.distance > self.maxDistance*2:
        print "way too far away", way.id, nearWay.distance
        nearLanduses = self.osm.getNearestWay(coords, True, tags={"landuse":"*"})
        for nearLanduse in nearLanduses:
          landuse = self.osm.ways[nearLanduse.nearestObj[0]]
          if landuse.isInside(coords):
            if nearLanduse not in landuseObjs:
              landuseObjs.append(nearLanduse)
    
    if len(landuseObjs) > 0:
      return landuseObjs
    else:      
      return nearObjs
  
  def _createBBox(self, coords):
    """
    The given coords mark the center of a bounding box
    with the given height and width.
    
    @param coords:  Central point coordinates - (lat, long) - of the
                    calculated bounding box
    @type coords:   Tuple(float, float)
    
    @return:        Returns a list of the lower left and upper right coordinates
                    for the bounding box
    """
    #Breitengrad: 0.00001 -> 1.11m
    #Längengrad: 0.00001 -> 0.66 m
    
    midLat = float(coords[0])
    midLon = float(coords[1])
    
    widthOffset = round(0.00001 * self.widthBBox / 2 / 1.11, 8)
    heightOffset = round(0.00001 * self.heightBBox / 2 / 0.66, 8)
    
    llX = round(midLat - widthOffset, 6)
    llY = round(midLon - heightOffset, 6)
    urX = round(midLat + widthOffset, 6)
    urY = round(midLon + heightOffset, 6)
    
    return [llX, llY, urX, urY]
