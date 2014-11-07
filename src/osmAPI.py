# -*- coding: utf-8 -*-

import requests
import osmData

#for testing
import os 

import xml.dom.minidom as dom

class osmAPI():
  
  def __init__(self):
    self.osmurl='http://overpass-api.de/api/interpreter'
      
  def getOsmRequestData(self, minLat,minLon,maxLat,maxLon):
    return {'data': '[out:xml][timeout:25];(node[""=""]({minLat},{minLon},{maxLat},{maxLon});way[""=""]({minLat},{minLon},{maxLat},{maxLon});relation[""=""]({minLat},{minLon},{maxLat},{maxLon}););out body;>;out skel qt;'.format(**locals())}

  def performRequest(self,boundingBox):
    #new code to prevent timeouts
    filename = "map_" + str(boundingBox) + ".xml"
    if (os.path.exists(filename)):
      self.parseData(open(filename, "r"))
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
      
      self.parseData(open(filename, "r"))
      
    #original code
    #return self.parseData(requests.get(self.osmurl,params=self.getOsmRequestData(boundingBox[0],boundingBox[1],boundingBox[2],boundingBox[3])))
  
  def parseData(self, obj):
    osmObj=osmData.OSM()
    
    #needed, when working with xml file
    data = dom.parse(obj)
    #needed, when directly working with the request object
    #dom = dom.parseString(obj.content)
    
    for node in data.getElementsByTagName('node'):      
      node_tags = {}
      if node.hasChildNodes():
        for element in node.childNodes:
          if (element.nodeType == dom.Node.TEXT_NODE):
            pass
          elif (element.tagName == "tag"):
            node_tags[element.getAttribute('k').encode('utf-8')] = element.getAttribute('v').encode('utf-8')
      print node.getAttribute('id'),node.getAttribute('lat'),node.getAttribute('lon')
      print node_tags
      print ":::::::::::::::::::::::::::::::"
      nodeObj=osmData.Node(node.getAttribute('id'), node.getAttribute('lat'), node.getAttribute('lon'), node_tags)
      
      osmObj.addNode(nodeObj)
      
    for way in data.getElementsByTagName('way'):
      way_id = way.getAttribute('id')
      print "ID" + str(way_id)
      way_refs = []
      way_tags = {}
      if way.hasChildNodes():
        for node in way.childNodes:
          if (node.nodeType == dom.Node.TEXT_NODE):
            pass
          elif (node.tagName == 'nd'):
            way_refs.append(node.getAttribute('ref').encode( "utf-8" ))
          elif (node.tagName == 'tag'):
            way_tags[node.getAttribute('k').encode( "utf-8" )] = node.getAttribute('v').encode( "utf-8" )
      print way_refs
      print way_tags
      print "-------------------------------------------"
      wayObj = osmData.Way(way_id, way_refs, way_tags)
      
      osmObj.addWay(wayObj)
    
    for relation in data.getElementsByTagName('relation'):
      rel_id = relation.getAttribute('id')
      rel_members = []
      rel_tags = {}
      if relation.hasChildNodes():
        for node in relation.childNodes:
          if (node.nodeType == dom.Node.TEXT_NODE):
            pass
          elif (node.tagName == "member"):
            type = node.getAttribute('type').encode("utf-8")
            ref = node.getAttribute('ref').encode("utf-8")
            role = node.getAttribute('role').encode("utf-8")
            rel_members.append({"type": type, "ref": ref, "role": role})
          elif (node.tagName == "tag"):
            rel_tags[node.getAttribute('k').encode( "utf-8" )] = node.getAttribute('v').encode( "utf-8" )
            
      print "ID" + rel_id
      print rel_members
      print rel_tags
      print ";;;;;;;;;;;;;;;;;;;"
      relObj = osmData.Relation(rel_id, rel_members, rel_tags)
      
      osmObj.addRelation(relObj)
      
    print len(osmObj.nodes)
    print len(osmObj.ways)
    print len(osmObj.relations)

if __name__ == '__main__':
  obj=osmAPI()
  boundingBox=[52.032736,8.486593,52.042113,8.501194]
  obj.performRequest(boundingBox)