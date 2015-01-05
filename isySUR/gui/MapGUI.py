#!/usr/bin/env python
#!/usr/bin/kivy

import os
from isySUR import kmlData

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty, NumericProperty,\
                          ListProperty
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line
from mapview import MapView

class Map(FloatLayout):
  
  text = StringProperty()
  
  def __init__(self):
    super(Map, self).__init__()
    
    global map_view
    map_view = self
    self.maps = MapView(app=app, zoom=11, lat=50.6394, lon=3.057)
    self.add_widget(self.maps, 20)
    
    self.menue = Menue()
    
    self.kmlList = KMLList()
  
  def toast(self, text):
    Toast().show(text, False)
      
  def open_menue(self):
    if self.menue.isOpen:
      self.menue.dismiss(self.ids.menueBut)
    else:
      self.menue.open(self.ids.menueBut)
    self.menue.isOpen = not self.menue.isOpen
    
  def open_kmlList(self):
    if len(app.loaded_kmls) == 0:
      self.toast("No KML files loaded!")
      #self.ids.toast.text = "No KML files loaded!"
    elif self.kmlList.is_open:
      self.kmlList.dismiss(self.ids.kml)
    else:
      self.kmlList.open(self.ids.kml)
    self.kmlList.is_open = not self.kmlList.is_open
    
  
  def addPolygon(self, polyList):
    for poly in polyList:
        self.maps.kmls.append(app.getPolygon(poly))
        self.maps.drawPolygon()
    
  def removePolygon(self, polygon):
    print polygon
    self.maps.kmls.remove(polygon)
    self.maps.drawPolygon()
  
class Menue(DropDown):
  loadfile = ObjectProperty(None)
  savefile = ObjectProperty(None)
  text_input = ObjectProperty(None)
  
  def __init__(self):
    super(Menue, self).__init__()
    self.text_input = TextInput()
    self.isOpen = False
    self.auto_dismiss = False
  
  def dismiss_popup(self):
    self._popup.dismiss()
  
  def show_load(self):
    self.isOpen = not self.isOpen
    self.dismiss()
    content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
    self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
    self._popup.open()
  
  def show_save(self):
    self.isOpen = not self.isOpen
    self.dismiss()
    content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
    self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
    self._popup.open()
  
  def load(self, path, filename):
    if filename != []:
      try:
        item_name, polyList = app.addKML(os.path.join(path, filename[0]))
        #add new kml to dropdown menue
        map_view.kmlList.addItem(item_name)
        map_view.addPolygon(polyList)
      except:
        map_view.toast('The loaded file is incomplete!')
        #map_view.ids.toast.text = "The loaded file is incomplete!"
  
    self.dismiss_popup()
  
  def save(self, path, filename):
    if filename != []:
      try:
        with open(os.path.join(path, filename), 'w') as stream:
          for kml in app.loaded_kmls:
            stream.write(app.loaded_kmls[kml]['data'].getXML())
      except Exception as e:
        print e
        map_view.toast('An error occured while saving!')
        #map_view.ids.toast.text = "An error occured while saving!"

    self.dismiss_popup()

class KMLList(DropDown):
  def __init__(self):
    super(KMLList, self).__init__()
    
    self.app = app
    self.is_open = False
    self.createList()
    self.auto_dismiss = False
  
  def createList(self):
    if len(app.loaded_kmls) != 0:
      for kml in self.app.loaded_kmls:
        btn = Button(text=self.app.loaded_kmls['name'], size_hint_y=None, height=44, background_color=(0,0,2,1))
        btn.bind(on_release=self.selectBut)
        self.add_widget(btn)
    
  def selectBut(self, obj):
    selected = app.loaded_kmls[obj.text]['selected']
    placemarks = app.loaded_kmls[obj.text]['data'].placemarks
    print placemarks
    if not selected:
      obj.background_color = (0,0,2,1)
      map_view.addPolygon(placemarks)
    else:
      obj.background_color = (1,1,1,1)
      for poly in placemarks:
        map_view.removePolygon(app.getPolygon(poly))
    app.loaded_kmls[obj.text]['selected'] = not selected

  def addItem(self, name):
    btn = Button(text=name, size_hint_y=None, height=44,background_color=(0,0,2,1))
    btn.bind(on_release=self.selectBut)
    self.add_widget(btn)

class Toast(Label):
  _transparency = NumericProperty(1.0)
  _background = ListProperty((0, 0, 0, 1))
  
  def __init__(self):
    super(Toast, self).__init__()
    self.pos = (map_view.center_x - self.width/2, 0.075)
  
  def show(self, text, length_long):
    duration = 5000 if length_long else 1000
    rampdown = duration * 0.1
    if rampdown > 500:
      rampdown = 500
    if rampdown < 100:
      rampdown = 100
    
    self._rampdown = rampdown
    self._duration = duration - rampdown
    self.text = text
    self.texture_update()
    map_view.add_widget(self)
    with self.canvas.before:
      Color(0,0,0,1)
      Rectangle(pos=(map_view.center_x - self.texture_size[0]/2 - 2.5, 10), size=(self.texture_size[0] + 5, self.texture_size[1]+ 2))
    
    Clock.schedule_interval(self._in_out, 1/60.0)
  
  def _in_out(self, dt):
    self._duration -= dt*1000
    if self._duration <= 0:
      self._transparency = 1.0 + (self._duration / self._rampdown)
    if -(self._duration) > self._rampdown:
      map_view.remove_widget(self)
      return False
  
class LoadDialog(FloatLayout):
  load = ObjectProperty(None)
  cancel = ObjectProperty(None)
  filters = ["*.kml"]

class SaveDialog(FloatLayout):
  save = ObjectProperty(None)
  text_input = ObjectProperty(None)
  cancel = ObjectProperty(None)
  
class MapApp(App):
  
  def __init__(self):
    super(MapApp, self).__init__()
    
    self.loaded_kmls = {}
    global app
    app = self
  
  def build(self):
    return Map()
  
  def addKML(self, kml):
    placemark = kmlData.KMLObject.parseKML(kml)
    name = "KML" + str(len(self.loaded_kmls) + 1)
    self.loaded_kmls.update({name:{'data':placemark, 'selected':True}})
    
    return name, placemark.placemarks
  
  def getPolygon(self, poly):
    polygon = []
    for i in range(len(poly.polygon)):
      coords = poly.polygon[i].split(',')
      if i == 0:
        first = coords
      polygon.append((float(coords[0]),float(coords[1])))
    
    polygon.append((float(first[0]),float(first[1])))
    return polygon
    

if __name__ == '__main__':
  MapApp().run()  


