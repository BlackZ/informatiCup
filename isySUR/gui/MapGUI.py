#!/usr/bin/env python
#!/usr/bin/kivy

import os
from isySUR import kmlData

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from mapview import MapView

class Map(FloatLayout):
  
  def __init__(self):
    super(Map, self).__init__()
    
    global map_view
    map_view = self
    self.maps = MapView(app=app, zoom=11, lat=50.6394, lon=3.057)
    self.add_widget(self.maps, 20)
    
    self.menue = Menue()
    
    self.kmlList = KMLList()
      
  def open_menue(self):
    if self.menue.isOpen:
      self.menue.dismiss(self.ids.menueBut)
    else:
      self.menue.open(self.ids.menueBut)
    self.menue.isOpen = not self.menue.isOpen
    
  def open_kmlList(self):
    if len(app.loaded_kmls) == 0:
      self.ids.toast.text = "No KML files loaded!"
    elif self.kmlList.is_open:
      self.kmlList.dismiss(self.ids.kml)
    else:
      self.kmlList.open(self.ids.kml)
    self.kmlList.is_open = not self.kmlList.is_open
  
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
      except:
        map_view.ids.toast.text = "The loaded file is incomplete!"
      #add new kml to dropdown menue
      map_view.kmlList.addItem(item_name)
      
      for poly in polyList:
        polygone = []
        for i in range(len(poly.polygon)):
          coords = poly.polygon[i].split(',')
          if i == 0:
            first = coords
          polygone.append((float(coords[0]),float(coords[1])))
        
        polygone.append((float(first[0]),float(first[1])))
        map_view.maps.addPolygone(polygone)
  
    self.dismiss_popup()
  
  def save(self, path, filename):
    if filename != []:
      try:
        with open(os.path.join(path, filename), 'w') as stream:
          for kml in app.loaded_kmls:
            stream.write(app.loaded_kmls[kml]['data'].getXML())
      except Exception as e:
        print e
        map_view.ids.toast.text = "An error occured while saving!"

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
    if selected:
      obj.background_color = (1,1,1,1)
    else:
      obj.background_color = (0,0,2,1)
    app.loaded_kmls[obj.text]['selected'] = not selected

  def addItem(self, name):
    print name
    btn = Button(text=name, size_hint_y=None, height=44,background_color=(0,0,2,1))
    btn.bind(on_release=self.selectBut)
    self.add_widget(btn)
    
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
    

if __name__ == '__main__':
  MapApp().run()  


