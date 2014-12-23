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
    
#TODO this function is not fully tested yet!
#For further information see the test_pipeline test file.
  def computeKMLs(self, inPath, outPath):
    isOutputDir = os.path.isdir(outPath)
    
    surs = sur.SUR.fromFile(open(inPath,'r'))
    
    completeKML = kml.KMLObject()
    
    for s in surs:
      resKML = self.calcKML(s)
      if isOutputDir:
        resKML.saveAsXML(outPath + os.path.sep + s.id + '.kml')
      #TODO give kml the option to merge to kmls and change this -> Jan
      completeKML.placemarks.extend(resKML.placemarks)
      
    if isOutputDir:
      completeKML.saveAsXML(outPath + os.path.sep + 'complete.kml')
    else:
      completeKML.saveAsXML(outPath)
  
  def calcKML(self, SUR):
    coords = (SUR.latitude, SUR.longitude)
    bBox = self._createBBox(coords)
    kmlObj = kml.KMLObject()
    self.osm = self.osmAPI.performRequest(bBox)
    
    #self._createDictionary()
    nearObj = self._getNearestObj(coords)
  
    #==============================================
    #TODO: now the result of getNearestX is a list of distanceResult-Objects. Now a loop is needed
    #TODO: each distanceResult-Object has a List of SubObj. which have the same distance --> loop needed
    #==============================================
    tmpRel = nearObj[0].nearestSubObj[0]  
    
    #print "nearest subobj", tmpRel
    while isinstance(tmpRel[1], osmData.Relation):
      tmpRel = osmData.getNearestRelation(coords, otherRelations = [tmpRel[0]])

    points = []
    if isinstance(tmpRel[1], osmData.Way):
      obj = self.osm.ways[tmpRel[0]]
      for ref in obj.refs:
        points.append(osmData.nodes[ref].getCoordinateString())
    elif isinstance(tmpRel[1], osmData.Node):
      points.append(self.osm.nodes[tmpRel[0]].getCoordinateString())
    
    
    for rule in SUR.ruleName:
      kmlObj.addPlacemark(kml.Placemark(str(rule) + ":" + str(SUR.ruleName[rule]),
                          rule,
                          pointList=points))
    
    return kmlObj
  
  def _getNearestObj(self, coords):
    nearObj = self.osm.getNearestRelation(coords)
    
#    if nearObj.distance == "-1":
#      nearObj = self.osm.getNearestWay(coords)
#      
#    if nearObj.distance == "-1":    
#      nearObj = self.osm.getNearestNode(coords)
#      
    return nearObj
  
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