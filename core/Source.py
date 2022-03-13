import random
import core

class Source:
  _x = 0
  _y = 0
  _arena = None
  _itemClass = None

  @property
  def x(self):
    return self._x

  @property
  def y(self):
    return self._y
  
  @property
  def arena(self):
    return self._arena

  @property
  def itemClass(self):
    return self._itemClass

  def __init__(self, itemClass, chance, arena, x, y):
    self._itemClass = itemClass
    self._lotery = int(round(1 / chance, 0))
    self._x = x
    self._y = y
    self._arena = arena

  def mustSpawn(self):
    return random.randint(1,self._lotery) == 1

  def spawnTime(self):
    if self.arena.findItem(self.x, self.y) is None:
      if self.mustSpawn():
        self.arena.addItem(self.itemClass(self.x,self.y))
  