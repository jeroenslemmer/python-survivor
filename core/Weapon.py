import core

class Weapon(core.Item):

  def __init__(self,x,y):
    super().__init__(core.ItemType.WEAPON,'W',x,y)
    self._attack = 3

  def pickUp(self, creature):
    creature._attack = self._attack
    creature._restTurns += 1
    core.log.add(creature.name + ' picks up a weapon')
    return True