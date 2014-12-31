#!/usr/bin/env python
# -*- coding: utf-8 -*-

import osmAPI as api
import osmData
import kmlData as kml
import sur
import os


class Pipeline:
  def __init__(self):
    self.osmAPI = api.osmAPI()
    self.osm = None
    self.heightBBox = 100
    self.widthBBox = 100
    self.allObjects = {}
    
  def computeKMLs(self, inPath, outPath, configPath):
    isOutputDir = os.path.isdir(outPath)
    
    surs = sur.SUR.fromFile(open(inPath,'r'))
    
    completeKML = kml.KMLObject()
    
    for s in surs:
      
      resKML = self.calcKML(s)
      if resKML != None:
        if isOutputDir:
          resKML.saveAsXML(outPath + os.path.sep + s.id + '.kml')
      #TODO give kml the option to merge to kmls and change this -> Jan
        completeKML.placemarks.extend(resKML.placemarks)
      
    if len(completeKML.placemarks) > 0:
      if isOutputDir:
        completeKML.saveAsXML(outPath + os.path.sep + 'complete.kml')
      else:
        completeKML.saveAsXML(outPath)
    else:
      print "Error: Could not compute placemarks."
  
  def calcKML(self, surObj):
    print "working on sur: ", surObj.id
    coords = (surObj.latitude, surObj.longitude)
    bBox = self._createBBox(coords)
    kmlObj = kml.KMLObject()
    #TODO Determine filter depending on rules
    self.osm = self.osmAPI.performRequest(bBox, [(["node","way","relation"],"building","")])
    nearObjs = self._getNearestObj(coords)
    if len(nearObjs) == 0:
      #Searching for buildings did not help.
      self.osm = self.osmAPI.performRequest(bBox)
      nearObjs = self._getNearestObj(coords)
    

    points = []
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
      if tmpWay != None:
        for ref in tmpWay.refs:
          points.append(self.osm.nodes[ref].getCoordinateString())
      
    if len(points) > 0:
      for rule in surObj.ruleName:
        kmlObj.addPlacemark(kml.Placemark(str(rule) + ":" + str(surObj.ruleName[rule]),
                          rule,
                          pointList=points))
    else:
      print "Error: No polygon found for SUR %s." % surObj.id
      return None
    
    return kmlObj
  
  def _getNearestObj(self, coords):
    nearObjs = self.osm.getNearestRelation(coords)
    
    if len(nearObjs) == 0:
      nearObjs = self.osm.getNearestWay(coords, True)
      
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
    with around 100m height and width.
    
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
    
    widthOffset = round(0.00001 * self.widthBBox / 2 / 1.11, 6)
    heightOffset = round(0.00001 * self.heightBBox / 2 / 0.66, 6)
    
    llX = round(midLat - widthOffset, 6)
    llY = round(midLon - heightOffset, 6)
    urX = round(midLat + widthOffset, 6)
    urY = round(midLon + heightOffset, 6)
    
    return [llX, llY, urX, urY]