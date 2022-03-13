import random
import core
import sys

# Arena class ################################################
#
#   An object of this class (an arena)...
#
#   - is a closed playing field for creatures, sources and items
#   
#   - can register and position:
#     . creatures (Creature class)
#     . sources (Source class) of items (Item Class) of certain types (ItemType class)
#   
#   - lets all creatures act turn based
#
#   - lets all sources act turn based to spawn new items
#  
#   - lets display:
#       . the playing field with creatures and items
#       . a log of the latest events
#       . a overview of the status of the creatures
#
# ######## methods for public use:
#
#   __init__(width: int, height: int) 
#     determines the dimensions at creation
#
#   registerCreature(creature: Creature):
#     registers and positions a given creature
#     
#   registerSource(itemClass, chance: float)
#     creates, registers and positions a source of given itemclass, with a given 
#     chance of spawning a new item.
#
#   start()
#     starts the play and display
# 
# ######## properties for public use:
#
#   width: int (width, horizontally of playing field of arena)
#   height: int (height, vertically of playing field of arena)
#   pause: Bool (should there be paused every turn of not)
#
# ###########################################################

class Arena:
  CLOSE_DISTANCE = 10
  _creatures = []
  _items = []
  _sources = []
  _width = 40
  _height = 40
  pause = False
  
  @property
  def width(self):
    return self._width

  @property
  def height(self):
    return self._height

  def __init__(self, width: int = 80, height: int = 80):
    self._width = width
    self._height = height

  def _findSafeNewCreaturePosition(self, newCreature: core.Creature):
    while True:
      x = random.randint(0,self._width-1)
      y = random.randint(0,self._height-1)
      safe = True
      for creature in self._creatures:
        if creature is not newCreature:
          if self._calcDistance(x,y,creature._x,creature._y) <= self.CLOSE_DISTANCE:
            safe = False
      if safe:
        return x, y
  
  def _findSafeNewSourcePosition(self):
    while True:
      x = random.randint(0,self._width-1)
      y = random.randint(0,self._height-1)
      safe = True
      for source in self._sources:
        if self._calcDistance(x,y,source._x,source._y) <= self.CLOSE_DISTANCE:
          safe = False
      if safe:
        return x, y
  
  def registerCreature(self, creature: core.Creature):
    self._creatures.append(creature)
    creature._x, creature._y = self._findSafeNewCreaturePosition(creature)
    self._totalCreatures = len(self._creatures)

  def registerSource(self, ItemClass, chance):
    x, y = self._findSafeNewSourcePosition()
    source = core.Source(ItemClass, chance, self, x, y)
    self._sources.append(source)
    self.addItem(source.itemClass(source.x, source.y))

  def _calcDistance(self,x1,y1,x2,y2):
    return abs(x1 - x2) + abs(y1 - y2)

  def _calcCreatureDistance(self,creature : core.Creature, object):
    return self._calcDistance(creature._x,creature._y, object._x, object._y)

  def _getNearCreatures(self, toCreature : core.Creature):
    nearCreatures = []
    for creature in self._creatures:
      if creature != toCreature:
        if self._calcCreatureDistance(toCreature, creature) <= self.CLOSE_DISTANCE:
          nearCreatures.append(creature)
    nearCreatures.sort(key=lambda creature: self._calcCreatureDistance(toCreature, creature))
    return nearCreatures
  
  def _getNearItems(self, toCreature : core.Creature):
    nearItems = []
    for item in self._items:
      if self._calcCreatureDistance(toCreature, item) <= self.CLOSE_DISTANCE:
        nearItems.append(item)
    nearItems.sort(key=lambda item:self._calcCreatureDistance(toCreature, item))
    return nearItems

  def findItem(self,x,y):
    for item in self._items:
      if item._x == x and item._y == y:
        return item
    return None

  def addItem(self, item: core.Item):
    self._items.append(item)

  def removeItem(self, item: core.Item):
    self._items.pop(self._items.index(item))

  def _buryCreature(self, creature):
    self._items.append(core.Armor(creature.x, creature.y))
    self._creatures.pop(self._creatures.index(creature))

  def _update(self):
    if self._totalCreatures > 1 and len(self._creatures) == 1:
      sys.exit()

    for creature in self._creatures:
      if creature._restTurns > 0:
        creature._restTurns -= 1
      else:
        nearCreatures = self._getNearCreatures(creature)
        nearItems = self._getNearItems(creature)
        creature.act(nearCreatures,nearItems)

    random.shuffle(self._creatures) # let fate decide who's first 

    for creature in self._creatures:
        command = creature.nextCommand()
        if command is not None:
         command.do(self)

    for creature in self._creatures:
      if creature.health <= 0:
        core.log.add(creature.name + ' dies ')
        self._buryCreature(creature)
    if len(self._creatures) == 1 and self._totalCreatures > 1:
      core.log.add(self._creatures[0].name + ' WINS!! ')
    
    for source in self._sources:
      source.spawnTime()
    
    if self.pause:
      input('continue...')

    self._displayArena()
    self._displayCreatures()
    self._display.addWindow(self._width+1,0,core.log.window())
    self._display.render()

  def _setCharacter(self,character, string, position):
    return string[:position] + character + string[position+1:] 

  def _displayCreatures(self):
    stdrow = ('.'*50)
    window = []
    self._creatures.sort(key = lambda creature: creature.name)
    for c in range(self._totalCreatures):
      if c < len(self._creatures):
        creature = self._creatures[c]
        row = f'{creature} health: {creature.health} attack: {creature.attack} defense: {creature.defense}'
        window.append((row+stdrow)[:50])
      else:
        window.append(stdrow[:50])
    self._display.addWindow(0,self.height+1, window)

  def _displayArena(self):
    stdrow = ('.'*40)[:self._width]
    visibles = {}
    for visible in self._creatures + self._items:
      y = visible._y
      if y not in visibles:
        visibles[y] = []
      visibles[y].append(visible)
    window = []
    for y in range(self._height):
      row = stdrow
      if y in visibles:
        for visible in visibles[y]:
          row = self._setCharacter(visible._character,row, visible._x)
      window.append(row)
    self._display.addWindow(0,0,window)

  def start(self):
    self._time = core.Time(2)
    self._display = core.Display()
    core.log.setSize(30,self.height)
    self._time.register(self._update)
    self._time.start()