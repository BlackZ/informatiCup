# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 13:39:44 2014

@author: adreyer
"""

import requests

if __name__ == '__main__':
  osmurl='http://overpass-api.de/api/interpreter'
  
  #citec without relation (only ways)  
  f=open("citec_ways.osm","w")
  res=requests.get(osmurl,params={'data':'[out:xml][timeout:25];\
    (\
    way(52.04557979825548,8.492072224617004,52.04605407035063,8.493078052997589);\
    );\
    out body;\
    >;\
    out skel qt;'})
  f.write(res.content)
  
  #citec with relation
  f=open("citec_relation.osm","w")
  res=requests.get(osmurl,params={'data':'[out:xml][timeout:25];\
    (\
    relation["building"](52.04557979825548,8.492072224617004,52.04605407035063,8.493078052997589);\
    );\
    out body;\
    >;\
    out skel qt;'})
  f.write(res.content)
  
  #the whole CERN
  f=open("cern.osm","w")
  osmurl='http://overpass-api.de/api/interpreter'
  res=requests.get(osmurl,params={'data':'[out:xml][timeout:25];\
    (\
    node["type"="site"](46.22886153655168,6.054641604423523,46.22992843710166,6.056653261184692);\
    way["type"="site"](46.22886153655168,6.054641604423523,46.22992843710166,6.056653261184692);\
    relation["type"="site"](46.22886153655168,6.054641604423523,46.22992843710166,6.056653261184692);\
    );\
    out body;\
    >;\
    out skel qt;'})
  f.write(res.content)