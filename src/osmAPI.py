# -*- coding: utf-8 -*-

import requests
import osmData
from xml.dom.minidom import parse, parseString

class osmAPI():
  def __init__(self):
    self.osmurl='http://overpass-api.de/api/interpreter'
      
  def getOsmRequestData(self, minLat,minLon,maxLat,maxLon):
    return {'data': '[out:xml][timeout:25];(node[""=""]({minLat},{minLon},{maxLat},{maxLon});way[""=""]({minLat},{minLon},{maxLat},{maxLon});relation[""=""]({minLat},{minLon},{maxLat},{maxLon}););out body;>;out skel qt;'.format(**locals())}

  def performRequest(self,boundingBox):
    return self.parseData(requests.get(self.osmurl,params=self.getOsmRequestData(boundingBox[0],boundingBox[1],boundingBox[2],boundingBox[3])))
  
  def parseData(self, obj):
    osmObj=osmData.OSM()
    dom = parseString(obj.content)
    for node in dom.getElementsByTagName('node'):
      #müssen noch irgendwo weggesucht werden.
      tags={}
      nodeObj=osmData.Node(node.attributes['id'],node.attributes['lat'],node.attributes['long'],tags)
    for way in dom.getElementsByTagName('way'):
      pass
    for relation in dom.getElementsByTagName('relation'):
      pass
    
if __name__ == '__main__':
  obj=osmAPI()
  boundingBox=[52.032736,8.486593,52.042113,8.501194]
  obj.performRequest(boundingBox)