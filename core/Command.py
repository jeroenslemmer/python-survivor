import core
class Command:

  def __init__(self, creature: core.Creature):
    self._creature = creature

  @property
  def creature(self):
    return self._creature

  def do(self, arena: core.Arena):
    pass



