# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 13:31:51 2014
Basic class to load and store space usage rules.
@author: jpoeppel & adreyer
"""

class SUR():
  
  def __init__(self, surID, name, lat, lon):
    """
      Constructor for the space usage rule object. 
      
      @param surID: Id of the sur
      
      @param name: The name of the rule. Usually a key-value combination.
      @type name: String
      
      @param lat: The latitude that belongs to the SUR.
      @type: Float
      
      @param lon: The longitude that belongs to the SUR.
      @type: Float
    """
    self.id = surID
    self.longitude = lon
    self.latitude = lat
    name = name.replace("\"", "").split('=')
    self.ruleName = {name[0]: name[1]}
    
  ##
  # addRuleName adds another rule name to the dictionary
  def addRuleName(self, name):
    """
      Function to add further rule names to the SUR.
      
      @param name: The name for the rule that is to be added.
      @type name: String
    """
    name = name.replace("\"", "").split('=')
    self.ruleName[name[0]] = name[1]
    
  ##
  # fromString builds an instance of SUR given a string containing the
  # relevant data.
  @classmethod
  def fromString(cls, s):
    """
      Classmethod that creates a SUR object from the given string.
      
      @param s: The string that contains the relevant data. The data should be seperated 
              by ','
      @type s: String
      
      @return: The created SUR object.
      @rtype: sur.SUR
    """
    data = s.replace(" ", "").split(',')
    return cls(data[0], data[3], float(data[1]), float(data[2]))
    
  ##
  # fromFile builds multiple instances of SUR given a file containing the
  # relevant data.
  @classmethod
  def fromFile(cls, f):
    """
      Classmethod that creates a list of SUR objects from the given file.
      
      @param f: The file handler of the already opened file that contains the SUR data.
      @type f: file
      
      @return: A list of all the created SURs.
      @rtype: [sur.SUR,]
    """
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
