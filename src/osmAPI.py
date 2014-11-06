# -*- coding: utf-8 -*-

import requests

class osmAPI():
  def __init__(self):
    self.osmurl='http://overpass-api.de/api/interpreter'
      
  def getOsmRequestData(self, minLat,minLon,maxLat,maxLon):
    return {'data': '[out:xml][timeout:25];(node[""=""]({minLat},{minLon},{maxLat},{maxLon});way[""=""]({minLat},{minLon},{maxLat},{maxLon});relation[""=""]({minLat},{minLon},{maxLat},{maxLon}););out body;>;out skel qt;'.format(**locals())}

  def performRequest(self,boundingBox):
    return requests.get(self.osmurl,params=self.getOsmRequestData(boundingBox[0],boundingBox[1],boundingBox[2],boundingBox[3]))
  
  def name(self, ):
    pass
    
    