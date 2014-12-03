#!/usr/bin/env python
# -*- coding: utf-8 -*-

import osmAPI as osm

class Pipeline:
  def __init__(self):
    self.osmAPI = osm.osmAPI()
    self._heightBBox = 100
    self._widthBBox = 100
  
  @property
  def heightBBox(self, height):
    self._heightBBox = height
  
  @property
  def widthBBox(self, width):
    self._widthBBox = width
  
  def calcKML(self, SUR):
    bBox = self._createBBox((SUR.latitude, SUR.longitude))
    
    osmData = self.osmAPI.performRequest(bBox)
    
    return None
  
  
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
    
    widthOffset = round(0.00001 * self._widthBBox / 2 / 1.11, 6)
    heightOffset = round(0.00001 * self._heightBBox / 2 / 0.66, 6)
    
    llX = round(midLat - widthOffset, 6)
    llY = round(midLon - heightOffset, 6)
    urX = round(midLat + widthOffset, 6)
    urY = round(midLon + heightOffset, 6)
    
    return [llX, llY, urX, urY]