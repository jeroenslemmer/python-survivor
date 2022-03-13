import core
import random
from datetime import datetime

class DemoCreature(core.Creature):

  def distance(self, object):
    return abs(self.x - object.x) + abs(self.y - object.y)

  def act(self, nearCreatures, nearItems):
    for creature in nearCreatures:
      if self.attack > 0 and self.health >= 2: #and creature.attack == 0:
        if self.x == creature.x and self.y == creature.y:
          self.clearPlan()
          self.hit(creature)
        else:
          if self.distance(creature) > 1 or random.randint(0,1) == 1:
            self.moveTo(creature)  
          else:
            self.wait()
            
        return

    for item in nearItems:
      if (item.type == core.ItemType.WEAPON and self.attack == 0) or \
        (item.type == core.ItemType.ARMOR and self.defense == 0) or \
        (item.type == core.ItemType.HEALTHPACK and self.health < core.Creature.MAX_HEALTH):
        self.moveTo(item)  
        return

    if not self.hasPlan():
      self.wander()
    
  def move(self, direction):
    if direction == 0:
      self.moveUp()
    elif direction == 1:
      self.moveRight()
    elif direction == 2:
      self.moveDown()
    else:
      self.moveLeft()

  def wander(self):
    steps = random.randint(1,5)
    direction = random.randint(0,3)
    for step in range(steps):
      self.move(direction)
