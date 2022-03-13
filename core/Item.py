import core
class Item:

  def __init__(self, itemType, character, x, y):
    self._x = x
    self._y = y
    self._type = itemType
    self._character = character

  def __str__(self):
    return f'Item: {self.type} at x: {self.x} and y: {self.y}'

  @property
  def type(self):
    return self._type

  @property
  def x(self):
    return self._x

  @property
  def y(self):
    return self._y

  def pickUp(self):
    return True

  pass
