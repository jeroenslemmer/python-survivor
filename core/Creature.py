import core
import random

# Creature class ################################################
#
#   An object of this class (a creature)...
#
#   - can act (turn-based) in an arena (Arena class) 
#     . it can walk and pick up items to provide it with attack, defense and health
#     . it can see nearby items and nearby creatures and there position
#     . it can hit other creatures at its position
#   
#   - exposes certain properties as: position (x,y), name, attack, defense and health
#   
#   - can not make good decisions on how to react to nearby items and nearbycreatures. 
#     This intelligence has to be added in an extended class
#
# ######## methods for public use:
#
#   __init__(type: str, name: str, color: str, character: str)
#
#   act(nearCreatures, nearItems) <to be changed in extended class>
#     determines the action the creature takes at its turn: moving, hitting or waiting. 
#     A creature can plan more dan one action in a turn, but one turn can execute just one 
#     action at a time.
#   
#     nearCreatures: the list of creatures in close proximity, sorted on distance
#     nearItems: the list of items in close proximity, sorted on distance
#
#   moveRight()
#     moves the creature to the right in the arena, picking up items
#     
#   moveLeft()
#     moves the creature to the left in the arena, picking up items
#
#   moveUp()
#     moves the creature to the top in the arena, picking up items
# 
#   moveDown()
#     moves the creature to the bottom in the arena, picking up items
#
#   hit(enemy: Creature)
#     lets the creature hit an enemy (opponent) at the same position. Damage depends
#     on the attack of the creature and on the defense of the opponent.
#   
#   wait()
#     do nothing and see what happens
#
#   wander()
#     move in a random direction
#
#   moveTo(object)
#     calculates a direction towards an object and moves accordingly
#
#   moveFrom(object)
#     calculates a direction away from an object and moves accordingly
#
#   hasPlan()
#     returns true if actions are already planned
#
#   clearPlan()
#     removes all planned actions
#
#   show() <to be changed in extended class>
#     returns:
#       - the character of the creature that is displayed at its position in the arena
#       - the color of the creature that is displayed at its position in the arena
#
#   __str__() <to be changed in extended class>
#      returns the string of the object
#
# ######## properties for public use:
#
#   name: str
#   type: str
#   health: int (maximal: MAX_HEALTH; 0 means object has died)
#   attack: int (dealt damage in hit)
#   defense: int (reduces damage when received hit)
#   x: (horizontal position in arena)
#   y: (vertical position in arena)
#
# ###########################################################

class Creature:
  MAX_HEALTH = 10
  BASIC_HEALTH = 3
  _name: str
  _type: str
  _color: str
  _character: str
  _health: int
  _attack: int
  _defense: int
  _x: int
  _y: int
  _restTurns: int
  _commands = []
  
  def __init__(self, type: str = 'Creature', name: str = 'unknown', color: str = 'white', character: str = 'x'):
    self._type = type
    self._name = name
    self._color = color
    self._character = character
    self._health = core.Creature.BASIC_HEALTH
    self._attack = 0
    self._defense = 0
    self._restTurns = 0
    self._x = 0
    self._y = 0

  def __str__(self):
    return f'{self._name}'

  def show(self):
    return self._character, self._color

  def act(self, closeCreatures, closeItems):
    self.wander()

  @property
  def x(self):
    return self._x

  @property
  def y(self):
    return self._y

  @property
  def attack(self):
    return self._attack

  @property
  def defense(self):
    return self._defense

  @property
  def health(self):
    return self._health

  @property
  def name(self):
    return self._name

  def hasPlan(self):
    return len(self._commands) > 0

  def clearPlan(self):
    self._commands = []

  def moveUp(self):
    self._commands.append(core.MoveCommand(self,core.Direction.UP))
  
  def moveDown(self):
    self._commands.append(core.MoveCommand(self,core.Direction.DOWN))

  def moveRight(self):
    self._commands.append(core.MoveCommand(self,core.Direction.RIGHT))

  def moveLeft(self):
    self._commands.append(core.MoveCommand(self,core.Direction.LEFT))

  def moveTo(self,object):
    self.clearPlan()
    distanceX = self._x - object._x
    distanceY = self._y - object._y
    if abs(distanceX) > abs(distanceY) or \
      abs(distanceX) == abs(distanceY) and random.randint(0,1) == 1:
      if distanceX < 0:
        self.moveRight()
      else:
        self.moveLeft()
    else:
      if distanceY < 0:
        self.moveDown()
      else:
        self.moveUp()
  
  def moveFrom(self,object):
    self.clearPlan()
    distanceX = self._x - object._x
    distanceY = self._y - object._y
    if abs(distanceX) < abs(distanceY) or \
      abs(distanceX) == abs(distanceY) and random.randint(0,1) == 1:
      if distanceX < 0:
        self.moveLeft()
      else:
        self.moveRight()
    else:
      if distanceY < 0:
        self.moveUp()
      else:
        self.moveDown()

  def hit(self, enemy: core.Creature):
    self._commands.append(core.AttackCommand(self, enemy))
  
  def wait(self):
    self._commands.append(core.IdleCommand(self))

  def wander(self):
    direction = random.randint(0,3)
    if direction == 0: # UP
      self.moveUp()
    elif direction == 1: # RIGHT
      self.moveRight()
    elif direction == 2: # DOWN
      self.moveDown()
    elif direction == 3: # LEFT
      self.moveLeft()


  def nextCommand(self):
    if len(self._commands) == 0:
      return None
    else:
      command = self._commands.pop(0)
      return command