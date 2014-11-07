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
      return self.parseData(open(filename, "r"))
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
      
      return self.parseData(open(filename, "r"))
      
    #original code
    #return self.parseData(requests.get(self.osmurl,params=self.getOsmRequestData(boundingBox[0],boundingBox[1],boundingBox[2],boundingBox[3])))
  
  def parseData(self, obj):
    osmObj=osmData.OSM()
    f = open("test.txt", "w")
    
    #needed, when working with xml file
    data = dom.parse(obj)
    #needed, when directly working with the request object
    #dom = dom.parseString(obj.content)
    
    for node in data.getElementsByTagName('node'):      
      node_id = node.getAttribute('id').encode('utf-8')
      
      if (osmObj.nodes.has_key(node_id)):
        if len(osmObj.nodes[node_id].tags) == 0:
          osmObj.nodes[node_id].tags = self.getTags(node)
      else:
        node_tags = self.getTags(node)
        
        nodeObj=osmData.Node(node_id, node.getAttribute('lat'), node.getAttribute('lon'), node_tags)
        osmObj.addNode(nodeObj)
      
    for way in data.getElementsByTagName('way'):
      way_id = way.getAttribute('id').encode('utf-8')
      
      if (osmObj.ways.has_key(way_id)):
        if len(osmObj.ways[way_id].refs) == 0:
          osmObj.ways[way_id].refs = self.getRefs(way)
        if len(osmObj.ways[way_id].tags) == 0:
          osmObj.ways[way_id].tags = self.getTags(way)
      
      else:
        if way.hasChildNodes():
          way_refs = self.getRefs(way)
          way_tags = self.getTags(way)
        
          wayObj = osmData.Way(way_id, way_refs, way_tags)  
          osmObj.addWay(wayObj)
    
    for relation in data.getElementsByTagName('relation'):
      rel_id = relation.getAttribute('id').encode('utf-8')
      
      if (osmObj.relations.has_key(rel_id)):
        if len(osmObj.relations[rel_id].members) == 0:
          osmObj.relations[rel_id].refs = self.getMembers(relation)
        if len(osmObj.relations[rel_id].tags) == 0:
          osmObj.relations[rel_id].tags = self.getTags(relation)

      else:
        if relation.hasChildNodes() :
          rel_members = self.getMembers(relation)
          rel_tags = self.getTags(relation) 

          relObj = osmData.Relation(rel_id, rel_members, rel_tags)
          osmObj.addRelation(relObj)

    return osmObj

  def getTags(self, node):
    tags = {}
    for element in node.getElementsByTagName('tag'):
        tags[element.getAttribute('k').encode('utf-8')] = element.getAttribute('v').encode('utf-8')
    
    return tags
  
  def getRefs(self, node):
    refs = []
    for element in node.getElementsByTagName('nd'):
      refs.append(element.getAttribute('ref').encode( "utf-8" ))
      
    return refs

  def getMembers(self, node):
    members = []
    for element in node.getElementsByTagName('member'):
      type = element.getAttribute('type').encode("utf-8")
      ref = element.getAttribute('ref').encode("utf-8")
      role = element.getAttribute('role').encode("utf-8")
      members.append({"type": type, "ref": ref, "role": role})
      
    return members
