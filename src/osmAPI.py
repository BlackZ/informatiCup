# -*- coding: utf-8 -*-

import requests
import osmData

#for testing
import os 

from xml.dom.minidom import parse, parseString

class osmAPI():
  
  def __init__(self):
    self.osmurl='http://overpass-api.de/api/interpreter'
      
  def getOsmRequestData(self, minLat,minLon,maxLat,maxLon):
    return {'data': '[out:xml][timeout:25];(node[""=""]({minLat},{minLon},{maxLat},{maxLon});way[""=""]({minLat},{minLon},{maxLat},{maxLon});relation[""=""]({minLat},{minLon},{maxLat},{maxLon}););out body;>;out skel qt;'.format(**locals())}

  def performRequest(self,boundingBox):
    #new code to prevent timeouts
    filename = "map_" + str(boundingBox) + ".xml"
    if (os.path.exists(filename)):
      pass
      #self.parseData(open(filename, "r"))
    else:
      file = open(filename, "w")
      tmp = requests.get(self.osmurl,params=self.getOsmRequestData(boundingBox[0],boundingBox[1],boundingBox[2],boundingBox[3]))
      print tmp.encoding
      print tmp.ok
      
      for block in tmp.iter_content(1024):
       if not block:
           break

       file.write(block)
      
      file.close()
      
      #self.parseData(open(filename, "r"))
      
    #original code
    #return self.parseData(requests.get(self.osmurl,params=self.getOsmRequestData(boundingBox[0],boundingBox[1],boundingBox[2],boundingBox[3])))
  
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