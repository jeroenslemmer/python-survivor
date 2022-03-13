import core

class HealthPack(core.Item):

  def __init__(self,x,y):
    super().__init__(core.ItemType.HEALTHPACK,'H', x, y)
    self._healthPoints = 1

  def pickUp(self, creature: core.Creature):
    core.log.add(creature.name + ' picks up a health pack')
    if creature._health < core.Creature.MAX_HEALTH:
      creature._health += self._healthPoints
      creature._restTurns += 3
    return True