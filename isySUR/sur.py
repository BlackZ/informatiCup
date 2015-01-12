# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 13:31:51 2014
Basic class to load and store space usage rules.
@author: jpoeppel & adreyer
"""

import surTypeManager as stm

class SUR():
  
  def __init__(self, surID, name, lat, lon, surClassification = "IO"):
    """
      Constructor for the space usage rule object. 
      
      @param surID: Id of the sur
      
      @param name: The name of the rule. Usually a key-value combination.
      @type name: String
      
      @param lat: The latitude that belongs to the SUR.
      @type lat: Float
      
      @param lon: The longitude that belongs to the SUR.
      @type lon: Float
      
      @param surClassification: Optional parameter to determine whether this sur can be applied indoor ("I"),
          Outdoor ("O") or indoor as well as outdoor ("IO"). Default is "IO".
      @type surClassification: String  
          
    """
    self.id = surID
    self.longitude = lon
    self.latitude = lat
    name = name.replace("\"", "").split('=')
    self.ruleName = {name[0]: name[1]}
    if surClassification in ["I","O","IO"]:
      self.classification = surClassification
    else:
      print "Warning: Classification %s invalid. Used IO instead" % surClassification
      self.classification = "IO"
    
  def addRuleName(self, name):
    """
      Function to add further rule names to the SUR.
      
      @param name: The name for the rule that is to be added.
      @type name: String
    """
    name = name.replace("\"", "").split('=')
    self.ruleName[name[0]] = name[1]
    

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
    

  @classmethod
  def fromFile(cls, f, configPath):
    """
      Classmethod that creates a list of SUR objects from the given file.
      
      @param f: The file handler of the already opened file that contains the SUR data.
      @type f: file
      
      @param configPath: Path to the config file that should be used to determine sur classification.
      @type configPath: String
      
      @return: A list of all the created SURs.
      @rtype: [sur.SUR,]
    """
    typeManager = None
    classification = "IO"
    #Get surTypeManager    
    if configPath != '':
      try:
        typeManager = stm.surTypeManager(configPath)
      except IOError, e:
        print e.message
        print "No config file will be used!"
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
      ruleString = line[3].rstrip()
      if typeManager != None:
        classification = typeManager.getSURType(ruleString)
      if line[0] == lastID:
        # only 'new' sur with equal id/lat/long
        surs[-1].addRuleName(ruleString)
        if surs[-1].classification != classification:
          surs[-1].classification = "IO"
      else:
        # completely new sur
        sur = cls(line[0], ruleString, float(line[1]), float(line[2]), classification)
        surs.append(sur)
        lastID = line[0]
      
    return surs
