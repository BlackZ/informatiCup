#!/usr/bin/env python
#!/usr/bin/kivy

import os
from threading import Thread,Lock
from Queue import Queue

from isySUR import kmlData, program
from mapview import MapView
from mapview import MapMarker

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty, StringProperty, NumericProperty,\
                          ListProperty, DictProperty

class Map(FloatLayout):
  
  text = StringProperty()
  
  def __init__(self):
    super(Map, self).__init__()
    
    self.lock = Lock()
    
    global map_view
    map_view = self
    self.maps = MapView(zoom=11, lat=50.6394, lon=3.057)
    self.maps.center_on(52.023368, 8.538291)
    self.addMarker(52.023368, 8.538291)
    #self.maps = MapView(app=app, zoom=11, lat=52.023368, lon=8.538291)
    self.add_widget(self.maps, 20)
    
    self.menue = Menue()
    
    self.kmlList = KMLList()
  
  def toast(self, text, duration=False):
    Toast().show(text, duration)
      
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
      self.kmlList.dismiss(self.ids.kmlList)
    else:
      self.kmlList.open(self.ids.kmlList)
    self.kmlList.is_open = not self.kmlList.is_open
    
  def addMarker(self, lat, lon):
    marker = MapMarker()
    marker.lat = lat
    marker.lon = lon
    
    self.maps.add_marker(marker)
    
  def addPolygonsFromKML(self, kml):
    """
    Adds all polygons from a KMLList. Moves map to the
    last added Polygon.
    """
    for placemark in kml.placemarks:
      if kml.placemarks.index(placemark) == len(kml.placemarks) -1:
        move_to = placemark.polygon[0]
      self.maps.addPolygon(app.getPolygonFromPlacemark(placemark))
      self.maps.drawPolygon()
    return move_to  
      
  
  def addPolygon(self, placemarks):
    """
    Adds all polygons from one KML. Moves map to the
    added Polygon.
    """
    for placemark in placemarks:
        self.maps.kmls.append(app.getPolygonFromPlacemark(placemark))
        self.maps.drawPolygon()
    move_to = placemarks[0].polygon[0]
    move_to = move_to.split(',')
    self.maps.center_on(float(move_to[1]), float(move_to[0]))
    self.maps.drawPolygon()
    
  def removePolygon(self, polygon):
    self.maps.kmls.remove(polygon)
    self.maps.drawPolygon()
  
  def computeAndShowKmls(self, path, queue):
    self.toast('Calculating ...', True)
    kmlList = Queue()
    thread = Thread(target=app.pipe._computeKMLs, args=(path, kmlList))
    thread.start()
    
    while not kmlList.empty() or thread.isAlive():
      self.toast('Calculating ...', True)
      item = kmlList.get()
      queue.put(item)
      name = app.addKML(str(item[0]), item[1])
      self.lock.acquire()
      self.kmlList.addItem(name)
      self.toast('Calculating ...', True)

      self.lock.release()
      move_to = self.addPolygonsFromKML(item[1])
    
    move_to = move_to.split(',')
    self.maps.center_on(float(move_to[1]), float(move_to[0]))
    
    
class Menue(DropDown):
  loadfile = ObjectProperty(None)
  savefile = ObjectProperty(None)
  text_input = ObjectProperty(None)
  
  def __init__(self):
    super(Menue, self).__init__()
    self.text_input = TextInput()
    self.isOpen = False
    self.auto_dismiss = False
    
    self.queue = Queue()
  
  def dismiss_load(self):
    self._popup_load.dismiss()
  
  def dismiss_save(self):
   self._popup_save.dismiss()
  
  def dismiss_config(self):
   self._popup_config.dismiss()
  
  
  def show_load(self, obj):
    self.isOpen = not self.isOpen
    self.dismiss()
    content = LoadDialog(load=self.load, cancel=self.dismiss_load)
    if 'KML' in obj.text:
      content.ids.filechooser.filters = ['*.kml']
    elif 'SUR' in obj.text:
      content.ids.filechooser.filters = ['*.txt']
    self._popup_load = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
    self._popup_load.open()
  
  def show_save(self):
    self.isOpen = not self.isOpen
    self.dismiss()
    content = SaveDialog(save=self.save, cancel=self.dismiss_save)
    self._popup_save = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
    self._popup_save.open()
    
      
  def show_config(self):
    self.isOpen = not self.isOpen
    self.dismiss()
    
    content = ConfigDialog(save=self.show_save, load=self.show_load, cancel=self.dismiss_config)
    self._popup_config = Popup(title="Configurate SUR-Rules", content=content, size_hint=(0.9, 0.9))
    self._popup_config.open()
  
  def load(self, filename):    
    if filename != []:
      #path = os.path.join(path, filename[0])
      path = filename[0]
      name, ext = os.path.splitext(filename[0])
      name = (name.replace('\\','/').split('/'))[-1]
      if ext == '.kml':
        try:
          item_name, polyList = app.addKMLFromPath(path, name)
          #add new kml to dropdown menue
          map_view.kmlList.addItem(item_name)
          map_view.addPolygon(polyList)
        except Exception as e:
          print e
          map_view.toast('The loaded KML file is incomplete!')
      
      self.dismiss_load()
      
      if ext == '.txt':
        Thread(target=map_view.computeAndShowKmls, args=(path, self.queue, )).start()
  
  def save(self, path, filename):
    isDir = os.path.isdir(os.path.join(path, filename))
    completeKML = kmlData.KMLObject()
    selection = app.getSelectedPolygons()
    for elem in selection:
      if isDir:  
        try:
          selection[elem].saveAsXML(path + os.path.sep + elem + '.kml')
        except:
          map_view.toast(elem + " could not be saved!")
      completeKML.placemarks.extend(selection[elem].placemarks)
    if len(completeKML.placemarks) > 0:
      try:
        if isDir:
          completeKML.saveAsXML(path + os.path.sep + 'complete.kml')
        else:
          with open(os.path.join(path, filename), 'w') as stream:
            stream.write(completeKML.getXML())
      except Exception as e:
        print e
        map_view.toast('An error occured while saving!')
        #map_view.ids.toast.text = "An error occured while saving!"

    self.dismiss_save()

class KMLList(DropDown):
  def __init__(self):
    super(KMLList, self).__init__()
    
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
    if not selected:
      obj.background_color = (0,0,2,1)
      map_view.addPolygon(placemarks)
    else:
      obj.background_color = (1,1,1,1)
      for placemark in placemarks:
        map_view.removePolygon(app.getPolygonFromPlacemark(placemark))
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
  
class ConfigDialog(FloatLayout):
  
  def __init__(self, save, load, cancel):
    super(ConfigDialog, self).__init__()
    
    self.load = load
    self.save = save
    self.cancel = cancel
    
    self.counter = 0
    
    if len(app.configContent) > 0:
      self.addConfigContent()
  
  def addConfigContent(self):  
    layout = GridLayout(cols=4)
    
    self.addContentHeader(layout)
    for ruleArea in app.configContent:
      for rule in app.configContent[ruleArea]:
        self.addConfigEntry(layout, ruleArea, rule)
    
    self.ids.view.add_widget(layout)
    #    self.addConfigEntry(content,item[0],optionSelected=item[1])
  
  def addContentHeader(self, layout):
    label1 = Label(text='', size_hint=(.4,.1))
    label2 = Label(text='Inside', size_hint=(.1,.1))
    label3 = Label(text='Outside', size_hint=(.1,.1))
    label4 = Label(text='Both', size_hint=(.1,.1))
    
    layout.add_widget(label1)
    layout.add_widget(label2)
    layout.add_widget(label3)
    layout.add_widget(label4)
  
  def addConfigEntry(self, layout, ruleArea, rule):
    active={"[Indoor]":False,"[Outdoor]":False,"[Both]":False}
    active[ruleArea] = True
    

    label = Label(text=rule, size_hint=(.4,.1))
    btn1 = CheckBox(group=('g' + str(self.counter)), active=active['[Indoor]'], size_hint=(.1,.1))
    btn2 = CheckBox(group=('g' + str(self.counter)), active=active['[Outdoor]'], size_hint=(.1,.1))
    btn3 = CheckBox(group=('g' + str(self.counter)), active=active['[Both]'], size_hint=(.1,.1))
    
    layout.add_widget(label)
    layout.add_widget(btn1)
    layout.add_widget(btn2)
    layout.add_widget(btn3)
    
    self.counter += 1
    
    
  def addConfigEntry_old(self,content,text,optionSelected=""):
    selected={"inner":"normal","outer":"normal","both":"normal"}
    if not optionSelected=="":
        selected[optionSelected]="down"
      
    label=Label(text=text,size_hint=(.4,.1))
    tglBtn1=ToggleButton(text='inner',group='g1', state=selected["inner"], size_hint=(.2,.1))
    tglBtn2=ToggleButton(text='outer',group='g1', state=selected["outer"],size_hint=(.2,.1))
    tglBtn3=ToggleButton(text='both',group='g1', state=selected["both"],size_hint=(.2,.1))
    content.add_widget(label)
    content.add_widget(tglBtn1)
    content.add_widget(tglBtn2)
    content.add_widget(tglBtn3)
  
  
class MapApp(App):
  
  def __init__(self, configPath):
    super(MapApp, self).__init__()
    
    self.configContent = {}
    self.loadConfig(configPath)
    
    print self.config
    
    self.pipe = program.Pipeline()
    self.loaded_kmls = {}
    global app
    app = self
  
  def build(self):
    return Map()
  
  def loadConfig(self, configPath):
    if configPath != '':
      with open(configPath, 'r') as stream:
        for line in stream:
          line = line.replace('\n','')
          if line.startswith('['):
            key = line
            self.configContent.update({key:[]})
          else:
            self.configContent[key].append(line)
          
  def addKML(self, name, kmlObj):
    newName = name
    i = 1
    while self.loaded_kmls.has_key(newName):
      newName = name + '(' + str(i) + ')'
      i += 1
    self.loaded_kmls.update({newName:{'data':kmlObj, 'selected':True}})
    
    return newName
  
  def addKMLFromPath(self, path, filename):
    kmlObj = kmlData.KMLObject.parseKML(path)
    name = filename
    i = 1
    while self.loaded_kmls.has_key(name):
      name = filename + '(' + str(i) + ')'
      i += 1
    self.loaded_kmls.update({name:{'data':kmlObj, 'selected':True}})
    
    return name, kmlObj.placemarks
  
  def getPolygonFromPlacemark(self, placemark):
    polygon = []
    for i in range(len(placemark.polygon)):
      coords = placemark.polygon[i].split(',')
      if i == 0:
        first = coords
      polygon.append((float(coords[0]),float(coords[1])))
    
    polygon.append((float(first[0]),float(first[1])))
    return polygon
  
  def getSelectedPolygons(self):
    selection = {}
    for kml in self.loaded_kmls:
      if self.loaded_kmls[kml]['selected']:
        selection.update({kml:self.loaded_kmls[kml]['data']})
    
    return selection
    

if __name__ == '__main__':
  MapApp().run()  


