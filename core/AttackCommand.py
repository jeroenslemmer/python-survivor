import core

class AttackCommand(core.Command):

  _enemy = None

  def __init__(self, creature: core.Creature, enemy: core.Creature):
    super().__init__(creature)
    self._enemy = enemy

  @property
  def enemy(self):
    return self._enemy

  def do(self, arena):
    core.log.add(self.creature.name + ' attacks ' + self.enemy.name)
    if self.creature.attack <= 0:
      core.log.add('no weapon used, nothing happens')
    elif self.creature.x == self.enemy.x and self.creature.y == self.enemy.y:
      damage = max(0,self.creature.attack - self.enemy.defense)
      self.enemy._health -= damage
      self.enemy._defense = 0
      core.log.add('damage dealt: '+str(damage))
      self._creature._attack = 0
    else:
      core.log.add('but misses, no damage dealt')
      self._creature._attack -= 1

   


