#!/usr/bin/env python
# -*- coding: utf-8 -*-

import osmAPI as api
import osmData
import kmlData as kml

class Pipeline:
  def __init__(self):
    self.osmAPI = api.osmAPI()
    self.osm = None
    self.heightBBox = 100
    self.widthBBox = 100
    self.allObjects = {}
    self.kmlObj = kml.KMLObject()
  
  def calcKML(self, SUR):
    coords = (SUR.latitude, SUR.longitude)
    bBox = self._createBBox(coords)
    
    self.osm = self.osmAPI.performRequest(bBox)
    
    #self._createDictionary()
    
    nearObj = self._getNearestObj(coords)
  
    tmpRel = nearObj.nearestSubObj  
    while isinstance(tmpRel[1], osmData.Relation):
      tmpRel = osmData.getNearestRelation(coords, otherRelations = [tmpRel[0]])

    nodes = []
    if isinstance(tmpRel[1], osmData.Way):
      obj = self.osm.ways[tmpRel[0]]
      for ref in obj.refs:
        nodes.append(osmData.nodes[ref])
    elif isinstance(tmpRel[1], osmData.Node):
      nodes.append(self.osm.nodes[tmpRel[0]])
    
    for rule in SUR.ruleName:
      self.kmlObj.addPlacemark(kml.Placemark(str(rule) + ":" + str(SUR.ruleName[rule]),
                          rule,
                          nodeList=nodes))
    
    return self.kmlObj
  
  def _getNearestObj(self, coords):
    nearObj = self.osm.getNearestRelation(coords)
    
    if nearObj.distance == "-1":
      nearObj = self.osm.getNearestWay(coords)
      
    if nearObj.distance == "-1":    
      nearObj = self.osm.getNearestNode(coords)
      
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