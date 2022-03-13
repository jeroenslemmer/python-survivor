import core
class Armor(core.Item):

  def __init__(self,x,y):
    super().__init__(core.ItemType.ARMOR,'A',x,y)
    self._defense = 1

  def pickUp(self, creature):
    creature._defense = self._defense
    creature._restTurns += 2
    core.log.add(creature.name + ' picks up an armor')
    return True

