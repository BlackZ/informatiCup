# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 19:56:04 2014

@author: adreyer
"""

import requests

boundingBox=[8.486593,52.032736,8.501194,52.042113]

minLon=boundingBox[0];
minLat=boundingBox[1];

maxLon=boundingBox[2];
maxLat=boundingBox[3];

osmrequest = {'data': '[out:xml][timeout:25];(node["amenity"="university"](%s,%s,%s,%s);way["amenity"="university"](%s,%s,%s,%s);relation["amenity"="university"](%s,%s,%s,%s););out body;>;out skel qt;'%(minLat, minLon, maxLat, maxLon, minLat, minLon, maxLat, maxLon, minLat, minLon, maxLat, maxLon)}
#osmrequest = {'data': '[out:xml][timeout:25];(node[""=""]({minLat},{minLon},{maxLat},{maxLon});way[""=""]({minLat},{minLon},{maxLat},{maxLon});relation[""=""]({minLat},{minLon},{maxLat},{maxLon}););out body;>;out skel qt;'.format(**locals())}

osmurl='http://overpass-api.de/api/interpreter'
osm=requests.get(osmurl,params=osmrequest)

osmdata=osm.content
#print(osmdata)