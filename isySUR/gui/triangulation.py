# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 00:15:11 2015
Simple triangulation class. It tries to triangulate a given polygon using the
ear clipping algorithm.
Roughly based on Rawlyn's implementation (http://chipmunk-physics.net/forum/viewtopic.php?f=1&t=813&p=3985)
but not using pymunk and more flexible to the polygon orientation.
@author: jpoeppel
"""

class Triangulator():
  
  def __init__(self):
    self.clockwise = False

  def _is_corner(self,a,b,c):
     # returns if point b is an outer corner
    if self.clockwise:
      return self.is_clockwise([a,b,c])
    else:
      return not self.is_clockwise([a,b,c])
   

                 
  def calc_area(self, tri):
    if len(tri) == 3:
      edge1 = (tri[1][0] -tri[0][0], tri[1][1]-tri[0][1])
      edge2 = (tri[2][0] -tri[0][0], tri[2][1]-tri[0][1])
      return 0.5 * (edge1[0]*edge2[1] - edge2[0]*edge1[1])
    else:
      print "not a triangle!!"
  
  
  def is_clockwise(self, points):
    edgeSum = 0
    size = len(points)
    for i in range(size):
      j = i + 1 if i < size-1 else 0
      p1 = points[i]
      p2 = points[j]
      edgeSum += (p2[0]-p1[0])*(p2[1]+p1[1])
    return (edgeSum > 0)


  def _point_in_triangle(self, p,a,b,c):
    # measure area of whole triangle
    whole = abs(self.calc_area([a,b,c]))
    # measure areas of inner triangles formed by p
    parta = abs(self.calc_area([a,b,p]))
    partb = abs(self.calc_area([b,c,p]))
    partc = abs(self.calc_area([c,a,p]))

    # allow for potential rounding error in area calcs
    # (not that i've encountered one yet, but just in case...)
    thresh = 0.0000001
    # return if the sum of the inner areas = the whole area
    return ((parta+partb+partc) < (whole+thresh))
      
  def _get_ear(self, poly):
    count = len(poly)
    # not even a poly
    if count < 3:
      return [], []
    # only a triangle anyway
    if count == 3:
      return poly, []

    # start checking points
    for i in range(count):
      ia = (i-1) % count
      ib = i
      ic = (i+1) % count
      a = poly[ia]
      b = poly[ib]
      c = poly[ic]
      # is point b an outer corner?
      if self._is_corner(a,b,c):
        # are there any other points inside triangle abc?
        valid = True
        for j in range(count):
          if not(j in (ia,ib,ic)):
            p = poly[j]
            if self._point_in_triangle(p,a,b,c):
              valid = False
        # if no such point found, abc must be an "ear"
        if valid:
          remaining = []
          for j in range(count):
            if j != ib:
              remaining.append(poly[j])
          # return the ear, and what's left of the polygon after the ear is clipped
          return [a,b,c], remaining
    # no ear was found, so something is wrong with the given poly (not anticlockwise? self-intersects?)
    return [], []

  ### major functions
   
  def triangulate(self,poly):
    """
    triangulates poly and returns a list of triangles
    poly: list of points that form an anticlockwise polygon (self-intersecting polygons won't work, results are... undefined)
    """
    triangles = []
    remaining = poly[:]
    if self.is_clockwise(poly):
      self.clockwise = True
    else:
      self.clockwise = False
    # while the poly still needs clipping
    while len(remaining) > 2:
      # rotate the list:
      # this stops the starting point from getting stale which sometimes a "fan" of polys, which often leads to poor convexisation
      remaining = remaining[1:]+remaining[:1]
      # clip the ear, store it
      ear, remaining = self._get_ear(remaining)
      if ear != []:
        triangles.append(ear)
    # return stored triangles
    return triangles
