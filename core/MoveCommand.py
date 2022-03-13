import core

class MoveCommand(core.Command):

  def __init__(self, creature: core.Creature, direction: core.Direction):
    super().__init__(creature)
    self._direction = direction

  def do(self, arena: core.Arena):
    x = self._creature._x
    y = self._creature._y

    if self._direction == core.Direction.RIGHT:
      x += 1
    if self._direction == core.Direction.DOWN:
      y += 1
    if self._direction == core.Direction.LEFT:
      x -= 1
    if self._direction == core.Direction.UP:
      y -= 1

    if x >=0 and y >= 0 and x < arena._width and y < arena._height:
      self._creature._x = x
      self._creature._y = y
      self._pickupItem(arena)

  def _pickupItem(self, arena: core.Arena):
    item = arena.findItem(self._creature._x, self._creature._y)
    if item is not None:
        pickedUp = item.pickUp(self.creature) 
        if pickedUp:
          arena.removeItem(item)


