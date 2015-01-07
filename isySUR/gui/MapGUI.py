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
from kivy.uix.filechooser import FileChooserListView
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
  
  def __init__(self, app):
    super(Map, self).__init__()
    
    self.lock = Lock()
    self.app = app
    self.maps = MapView(zoom=11, lat=50.6394, lon=3.057)
    self.maps.center_on(52.023368, 8.538291)
    self.addMarker(52.023368, 8.538291)
    #self.maps = MapView(app=app, zoom=11, lat=52.023368, lon=8.538291)
    self.add_widget(self.maps, 20)
    
    self.menue = Menue(self, app)
    
    self.kmlList = KMLList(self, app)
  
  def toast(self, text, duration=False):
    Toast(self).show(text, duration)
      
  def open_menue(self):
    if self.menue.isOpen:
      self.menue.dismiss(self.ids.menueBut)
    else:
      self.menue.open(self.ids.menueBut)
    self.menue.isOpen = not self.menue.isOpen
    
  def open_kmlList(self):
    if len(self.app.loaded_kmls) == 0:
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
      self.maps.addPolygon(self.app.getPolygonFromPlacemark(placemark))
      self.maps.drawPolygon()
    return move_to  
      
  
  def addPolygon(self, placemarks):
    """
    Adds all polygons from one KML. Moves map to the
    added Polygon.
    """
    print placemarks
    for placemark in placemarks:
      try:  
        self.maps.addPolygon(self.app.getPolygonFromPlacemark(placemark))
      except:
        print 'getPolygonFromPlacemark'
    move_to = placemarks[0].polygon[0]
    move_to = move_to.split(',')
#    self.maps.center_on(float(move_to[1]), float(move_to[0]))
    self.maps.zoom_to(move_to[1], move_to[0], 15)
    self.maps.drawPolygon()
    
  def removePolygon(self, polygon):
    self.maps.kmls.remove(polygon)
    self.maps.drawPolygon()
  
  def computeAndShowKmls(self, path, queue):
    self.toast('Calculating ...', True)
    kmlList = Queue()
    thread = Thread(target=self.app.pipe._computeKMLs, args=(path, kmlList))
    thread.start()
    
    while not kmlList.empty() or thread.isAlive():
      self.toast('Calculating ...', True)
      item = kmlList.get()
      queue.put(item)
      if not item[1].placemarks == []:
        self.lock.acquire()
        name = self.app.addKML(str(item[0]), item[1])
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
  
  def __init__(self, mapview, app):
    super(Menue, self).__init__()
    self.text_input = TextInput()
    self.isOpen = False
    self.auto_dismiss = False

    self.map_view =mapview
    self.app = app

    self.config = None
    
    self.queue = Queue()
  
  def dismiss_load(self):
    self._popup_load.dismiss()
  
  def dismiss_save(self):
   self._popup_save.dismiss()
  
  def dismiss_config(self):
   self._popup_config.dismiss()
   self.config = None
  
  
  def show_load(self, obj, config=None):
    self.isOpen = False
    self.dismiss()
    content = LoadDialog(load=self.load, cancel=self.dismiss_load)
    if 'KML' in obj.text:
      content.ids.filechooser.filters = ['*.kml']
    elif 'SUR' in obj.text:
      content.ids.filechooser.filters = ['*.txt']
    else:
      content.ids.filechooser.filters = ['*.cfg']
    self._popup_load = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
    self._popup_load.open()
  
  def show_save(self, isConfig=False):
    self.isOpen = False
    self.dismiss()
    if isConfig:
      content = SaveDialog(save=self.saveConfig, cancel=self.dismiss_save)
    else:
      content = SaveDialog(save=self.saveKML, cancel=self.dismiss_save)
    self._popup_save = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
    self._popup_save.open()
    
      
  def show_config(self):
    self.isOpen = False
    self.dismiss()
    
    self.config = ConfigDialog(self.app, save=self.show_save, load=self.show_load, cancel=self.dismiss_config)
    self._popup_config = Popup(title="Configurate SUR-Rules", content=self.config, size_hint=(0.9, 0.9))

    self._popup_config.open()
#    
  #def test(self, a,b):
  #  print "test a:",a.path
  #  print "test b:", b
    
#  def test(self, entry, touch):
#    '''(internal) This method must be called by the template when an entry
#    is touched by the user.
#    '''
#    if ('button' in touch.profile and touch.button in ('scrollup', 'scrolldown', 'scrollleft', 'scrollright')):
#      return False
#    _dir = self.file_system.is_dir(entry.path)
#    dirselect = self.dirselect
#    if _dir and dirselect and touch.is_double_tap:
#      self.open_entry(entry)
#      return
#    if self.multiselect:
#      if entry.path in self.selection:
#        self.selection.remove(entry.path)
#      else:
#        if _dir and not self.dirselect:
#          self.open_entry(entry)
#          return
#        self.selection.append(entry.path)
#    else:
#      if _dir and not self.dirselect:
#        self.open_entry
#        return
#      self.selection = [entry.path, ]
  
  def load(self, path, filename, config=None):    
    if filename != []:
      #path = os.path.join(path, filename[0])
      path = filename[0]
      name, ext = os.path.splitext(filename[0])
      name = (name.replace('\\','/').split('/'))[-1]
      if ext == '.kml':
        try:
          item_name, placemarks = self.app.addKMLFromPath(path, name)
          if not placemarks==[]:
            self.map_view.kmlList.addItem(item_name)
            self.map_view.addPolygon(placemarks)
          else:
            self.map_view.toast('The loaded KML has no polygon!')
        except Exception as e:
          print e
          self.map_view.toast('The loaded KML file is incomplete!')
          #add new kml to dropdown menue
      
      if ext == '.cfg':
        self.app.loadConfig(path)
        
        if len(self.app.configContent) > 0:
          self.config.addConfigContent()
          
      self.dismiss_load()
      
      if ext == '.txt':
        Thread(target=self.map_view.computeAndShowKmls, args=(path, self.queue, )).start()
  
  def saveConfig(self, path, filename):
    if filename != "":
    
      config = {'[Indoor]':[], '[Outdoor]':[], '[Both]':[]}
    
      for layout in self.config.ids.view.children:
        if isinstance(layout, GridLayout):
          i = 0
          while i < (len(layout.children) - 4)/4:
    
            child = layout.children[(4*i):(4*(i+1))]
            rule = ""
            key = ""
            for elem in child:
              print elem
              if isinstance(elem, Label):
                rule = elem.text
              if isinstance(elem, CheckBox):
                if elem.active:
                  key = elem.id
                  
            config[key].append(rule)
            i += 1
      
      with open(os.path.join(path, filename), 'w') as stream:
        for ruleArea in config:
          stream.write(ruleArea + '\n')
          for rule in config[ruleArea]:
            stream.write(rule + '\n')
      
      self.dismiss_save()
  
  def saveKML(self, path, filename):
    isDir = os.path.isdir(os.path.join(path, filename))
    completeKML = kmlData.KMLObject()
    selection = self.app.getSelectedPolygons()
    if len(selection) > 0:
      for elem in selection:
        if isDir:  
          try:
            selection[elem].saveAsXML(path + os.path.sep + elem + '.kml')
          except:
            self.map_view.toast(elem + " could not be saved!")
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
          self.map_view.toast('An error occured while saving!')
          #map_view.ids.toast.text = "An error occured while saving!"
    else:
      self.map_view.toast("No KML files selected or loaded!")

    self.dismiss_save()

class CustomFileChooser(FileChooserListView):
  """
    Implemented this and override the following method to fix path bug.
  """
  
  def open_entry(self, entry):
        #print "custom open"
        #try:
        #    # Just check if we can list the directory. This is also what
        #    # _add_file does, so if it fails here, it would also fail later
        #    # on. Do the check here to prevent setting path to an invalid
        #    # directory that we cannot list.
        #    self.file_system.listdir(entry.path)
        #except OSError:
        #    entry.locked = True
        #else:
        #    self.path = entry.path
        #    self.selection = []
        newPath = ''
        entry_path = entry.path.replace('\\', '/')
        if entry_path == '../':
          newPath = os.path.join(self.path, entry_path[:-1])
        else:
          tmp = entry_path.split('/')
          newPath = os.path.join(self.path, tmp[-1])
        
        if os.path.isdir(newPath):
          self.path = newPath 
          self.selection = []


class KMLList(DropDown):
  def __init__(self, mapview, app):
    super(KMLList, self).__init__()
    self.map_view = mapview
    self.app = app
    self.is_open = False
    self.createList()
    self.auto_dismiss = False
  
  def createList(self):
    if len(self.app.loaded_kmls) != 0:
      for kml in self.app.loaded_kmls:
        btn = Button(text=self.app.loaded_kmls['name'], size_hint_y=None, height=44, background_color=(0,0,2,1))
        btn.bind(on_release=self.selectBut)
        self.add_widget(btn)
    
  def selectBut(self, obj):
    selected = self.app.loaded_kmls[obj.text]['selected']
    placemarks = self.app.loaded_kmls[obj.text]['data'].placemarks
    if not selected:
      obj.background_color = (0,0,2,1)
      self.map_view.addPolygon(placemarks)
    else:
      obj.background_color = (1,1,1,1)
      for placemark in placemarks:
        self.map_view.removePolygon(self.app.getPolygonFromPlacemark(placemark))
    self.app.loaded_kmls[obj.text]['selected'] = not selected

  def addItem(self, name):
    btn = Button(text=name, size_hint_y=None, height=44,background_color=(0,0,2,1))
    btn.bind(on_release=self.selectBut)
    self.add_widget(btn)

class Toast(Label):
  _transparency = NumericProperty(1.0)
  _background = ListProperty((0, 0, 0, 1))
  
  def __init__(self, mapview):
    super(Toast, self).__init__()
    self.map_view =mapview
    self.pos = (self.map_view.center_x - self.width/2, 0.075)
    
  
  def show(self, text, length_long):
    duration = 7000 if length_long else 2000
    rampdown = duration * 0.1
    if rampdown > 500:
      rampdown = 500
    if rampdown < 150:
      rampdown = 150
    
    self._rampdown = rampdown
    self._duration = duration - rampdown
    self.text = text
    self.texture_update()
    self.map_view.add_widget(self)
    with self.canvas.before:
      Color(0,0,0,1)
      Rectangle(pos=(self.map_view.center_x - self.texture_size[0]/2 - 2.5, 10), 
                size=(self.texture_size[0] + 5, self.texture_size[1]+ 2))
    
    Clock.schedule_interval(self._in_out, 1/60.0)
  
  def _in_out(self, dt):
    self._duration -= dt*1000
    if self._duration <= 0:
      self._transparency = 1.0 + (self._duration / self._rampdown)
    if -(self._duration) > self._rampdown:
      self.map_view.remove_widget(self)
      return False
  
class LoadDialog(FloatLayout):
  load = ObjectProperty(None)
  cancel = ObjectProperty(None)
  test = ObjectProperty(None)

class SaveDialog(FloatLayout):
  save = ObjectProperty(None)
  text_input = ObjectProperty(None)
  cancel = ObjectProperty(None)
  
class ConfigDialog(FloatLayout):
  
  def __init__(self, app, save, load, cancel):
    super(ConfigDialog, self).__init__()

    self.app = app    
    
    self.load = load
    self.save = save
    self.cancel = cancel
    
    self.info = Label(text="No configuration file loaded!")
    self.counter = 0
    self.layout = GridLayout(cols=4, size_hint_y=1.1)
    
    self.ruleInput = TextInput(focus=True, size_hint=(.4,.15))
    
    if len(self.app.configContent) > 0:
      self.addConfigContent()
    else:
      self.layout.add_widget(self.info)
    self.ids.view.add_widget(self.layout)
    
    print self.ids.view.children

  def addConfigContent(self):
    print 'add Content'
    if self.info.parent != None:
      self.layout.remove_widget(self.info)
    if len(self.layout.children) > 1:
      self.layout.clear_widgets()
    self.addContentHeader()
    for ruleArea in self.app.configContent:
      for rule in self.app.configContent[ruleArea]:
        self.addConfigEntry(ruleArea, rule)
  
  def addContentHeader(self):
    label1 = Label(text='', size_hint=(.4,.1))      
    label2 = Label(text='Indoor', size_hint=(.1,.1))
    label3 = Label(text='Outdoor', size_hint=(.1,.1))
    label4 = Label(text='Both', size_hint=(.1,.1))
    
    self.layout.add_widget(label1)
    self.layout.add_widget(label2)
    self.layout.add_widget(label3)
    self.layout.add_widget(label4)
  
  def addConfigEntry(self, ruleArea, rule):
    active={"[Indoor]":False,"[Outdoor]":False,"[Both]":False}
    active[ruleArea] = True
    
    group = ('g' + str(self.counter))
    label = Label(text=rule, size_hint=(.4,.1), id=group)
    btn1 = CheckBox(group=group, active=active['[Indoor]'], size_hint=(.1,.1), id='[Indoor]')
    btn2 = CheckBox(group=group, active=active['[Outdoor]'], size_hint=(.1,.1), id='[Outdoor]')
    btn3 = CheckBox(group=group, active=active['[Both]'], size_hint=(.1,.1), id='[Both]')
    
    self.layout.add_widget(label)
    self.layout.add_widget(btn1)
    self.layout.add_widget(btn2)
    self.layout.add_widget(btn3)
    
    self.counter += 1
  
    
  def addRule(self, obj):
    if "New" in obj.text:
      obj.text = "Add Rule"
      self.ruleInput.text = ""
      self.layout.add_widget(self.ruleInput)
      self.ids.view.scroll_y = 0 
    elif "Add" in obj.text:
      obj.text = "New Rule"
      self.layout.remove_widget(self.ruleInput)
      if self.ruleInput.text != "":
        group = 'g' + str(self.counter)
        self.app.configContent['[Both]'].append(self.ruleInput.text)
        print self.app.configContent
        self.layout.add_widget(Label(text=self.ruleInput.text, size_hint=(.4,.1), id=group))
        self.layout.add_widget(CheckBox(group=group, size_hint=(.1,.1), id='[Indoor]'))
        self.layout.add_widget(CheckBox(group=group, size_hint=(.1,.1), id='[Outdoor]'))
        self.layout.add_widget(CheckBox(group=group, active=True, size_hint=(.1,.1), id='[Both]'))
        self.ids.view.scroll_y = 0 
      
  
class MapApp(App):
  
  def __init__(self, configPath=""):
    super(MapApp, self).__init__()
    
    self.configContent = {}
    self.loadConfig(configPath)
    
    print self.config
    
    self.pipe = program.Pipeline()
    self.loaded_kmls = {}

  
  def build(self):
    return Map(self)
  
  def loadConfig(self, configPath):
    if configPath != '':
      self.configContent = {}
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
    print len(placemark.polygon)
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


