# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 13:31:51 2014
Basic class to load and store space usage rules.
@author: jpoeppel & adreyer
"""

class SUR():
  
  def __init__(self, surID, name, lat, lon):
    self.id = surID
    self.longitude = lon
    self.latitude = lat
    name = name.replace("\"", "").split('=')
    self.ruleName = {name[0]: name[1]}
    
  ##
  # addRuleName adds another rule name to the dictionary
  def addRuleName(self, name):
    name = name.replace("\"", "").split('=')
    self.ruleName[name[0]] = name[1]
    
  ##
  # fromString builds an instance of SUR given a string containing the
  # relevant data.
  @classmethod
  def fromString(cls, s):
    data = s.replace(" ", "").split(',')
    return cls(data[0], data[3], float(data[1]), float(data[2]))
    
  ##
  # fromFile builds multiple instances of SUR given a file containing the
  # relevant data.
  @classmethod
  def fromFile(cls, f):
    # open file and read first line (num of SURs)
    num = f.readline()
    try:
      num=int(num)
    except ValueError:
      print "Invalid data file: First line is no number."
    
    # build SURs
    surs = []
    lastID = 0
    for i in range(int(num)):
      line = f.readline().replace(" ","").split(',')
      if line[0] == lastID:
        # only 'new' sur with equal id/lat/long
        surs[-1].addRuleName(line[3].rstrip())
      else:
        # completely new sur
        sur = cls(line[0], line[3].rstrip(), float(line[1]), float(line[2]))
        surs.append(sur)
        lastID = line[0]
      
    #return SURs
    return surs
