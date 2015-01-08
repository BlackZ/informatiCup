#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Last modified on Thu Jan 01 13:05:00 2015
Main pipeline to compute kml from a given SUR(file).
@author: jpoeppel 
"""
import osmAPI as api
import osmData
import kmlData as kml
import sur
import os
import sys


class Pipeline:
  def __init__(self):
    """
      Constructor for the pipeline. Sets up the osmAPI as well as the desired bounding box, 
      that is to be used to request osm data.
    """
    self.osmAPI = api.osmAPI()
    self.osm = None
    self.heightBBox = 20
    self.widthBBox = 20
    self.allObjects = {}
    self.certainStyle = {"Style":{"polyColour":"9900ff00"}}
    self.uncertainStyle = {"StyleUncertain":{"polyColour":"99ff0000"}}
    
    
  def computeKMLsAndStore(self, inPath, outPath, configPath=''):
    """
      Function to compute kmls from a given file of SURs. Stores them either in one kml or in 
      individual kmls plus one containing all of them. W
      
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
    surs = sur.SUR.fromFile(surFile, configPath)
    surFile.close()
    
    completeKML = kml.KMLObject("complete.kml")
    
    
    for s in surs:
      
      resKML = self.calcKML(s)
      if resKML != None:
        if isOutputDir:
          resKML.saveAsXML(outPath + os.path.sep + s.id + '.kml')
      #TODO give kml the option to merge to kmls and change this -> Jan
        completeKML.placemarks.extend(resKML.placemarks)
        completeKML.addStyles(resKML.styles)
      
    if len(completeKML.placemarks) > 0:
      if isOutputDir:
        completeKML.saveAsXML(outPath + os.path.sep + 'complete.kml')
      else:
        completeKML.saveAsXML(outPath)
    else:
      print "Error: Could not compute placemarks."
  
  def _computeKMLs(self, inPath, kmlList, configPath=''):
    """
    Function to compute kmls from a given file of SURs. Only needed for GUI.
    
    @param inPath: Path to the file containing the SURs which areas are to be computed.
    @type inPath: String
    
    @param configPath: Optional path to a config file, containing information about the classification of rules
      (indoor, outdoor or both).
    @type configPath: String
    """
    
    surFile = open(inPath,'r')
    surs = sur.SUR.fromFile(surFile, configPath)
    surFile.close()
    
    #kmlList = []
    
    for s in surs:
      kmlList.put(s.id)
      kmlObj = self.calcKML(s)
      if kmlObj != None:
        kmlList.put(kmlObj)
    
    #return kmlList
  
  def calcKML(self, surObj):
    """
      Function to work on a single sur.SUR object and computes it's kml.
      
      @param surObj: The sur object whose kml is to be calculated.
      @type surObj: sur.SUR
      
      @return: KML object containing the calculated area for the given sur. 
               Returns None if no polygon could be computed.
      @rtype: kmlData.KMLObject
    """

    #print "working on sur: ", surObj.id
    coords = (surObj.latitude, surObj.longitude)
    
#    print bBox
    
    kmlObj = kml.KMLObject(surObj.id+".kml")
    
    self.osm = self._getOSMData(surObj, coords)  

#    print "nodes:", len(self.osm.nodes)
#    print "ways:", len(self.osm.ways)
#    print "relations:", len(self.osm.relations)
#      
    if surObj.classification in ["I","IO"]:
      nearObjs = self._getNearestObj(coords, {"building":"*"})
    else:
      nearObjs = self._getNearestObj(coords)
    

    usedStyle = self.certainStyle
    possibleWays = []
    for obj in nearObjs:
      tmpObj = obj.nearestObj
      tmpWay = None
      if tmpObj[1] == osmData.Relation:
        tmpRel = self.osm.relations[tmpObj[0]]
        for mem in tmpRel.members:
          if mem[2] == "outer":
            tmpWay = self.osm.ways[mem[1]]
      if tmpObj[1] == osmData.Way:
        tmpWay = self.osm.ways[tmpObj[0]]
        
      if tmpWay.tags.has_key("landuse"):
        print "is landuse"
        if tmpWay.tags["landuse"] == "residential":
          otherWayIds = self.osm.ways.keys()
          otherWayIds.remove(tmpWay.id)
          buildings = self.osm.getNearestWay(coords, True, {"building":"*"}, otherWayIds)

          if len(buildings) > 1:
            print "more than one potential building."
          usedStyle = self.uncertainStyle
          for build in buildings:
            tmpBuild = build.nearestObj
            tmpWay = self.osm.ways[tmpBuild[0]]
            usedStyle = self.certainStyle
#            possibleWays.append(tmpWay)
#            #Set to None to prevent adding it multiple times
#            tmpWay = None              
            
      
      if tmpWay != None:
        possibleWays.append(tmpWay)
        
    if len(possibleWays) == 0:
      print "No ways found :-(."
      return None
          
    bestWay = None
    closestDist = sys.float_info.max
    for way in possibleWays:
      dist = 0
      for ref in way.refs:
        dist += self.osm.nodes[ref].getDistance(coords).distance
      dist /= len(way.refs)
      if dist < closestDist:
        closestDist = dist
        bestWay = way
            
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
                          style="#"+usedStyle.keys()[0],
                          ruleCoords = coords)
      kmlObj.addPlacemark(placemark)
    else:
      print "Error: No polygon found for SUR %s." % surObj.id
      return None
      
    kmlObj.addStyles(usedStyle)
    
    return kmlObj
    
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
    osm = None
    if surObj.classification == "I":
      osm = self.osmAPI.performRequest(bBox, [(["node","way","relation"],"building","")])
    else:
      osm = self.osmAPI.performRequest(bBox)
      
    #Increase boundingBox until we actually find SOMETHING
    while len(osm.nodes) < 3:
      self.widthBBox *= 2
      self.heightBBox *= 2
      bBox = self._createBBox(coords)
      if surObj.classification == "I":
        osm = self.osmAPI.performRequest(bBox, [(["node","way","relation"],"building","")])
      else:
        osm = self.osmAPI.performRequest(bBox)
        
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
    nearObjs = self.osm.getNearestRelation(coords, tags=tags)
    
    if len(nearObjs) == 0:
      nearObjs = self.osm.getNearestWay(coords, True)
    if len(nearObjs) == 0:
      nearObjs = self.osm.getNearestWay(coords, False)  
#    if nearObj.distance == "-1":    
#      nearObj = self.osm.getNearestNode(coords)
#      
    return nearObjs
  
  def _createDictionary(self):
    self.allObjects.update({self.osm.relations.__class__:self.osm.relations})
    self.allObjects.update({self.osm.ways[0].__class__:self.osm.ways})
    self.allObjects.update({self.osm.nodes[0].__class__:self.osm.nodes})
    
    print self.allObjects
  
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
