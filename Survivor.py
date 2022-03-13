import core
from MyCreature import MyCreature
from WeakCreature import WeakCreature

arena = core.Arena(25,25)

arena.registerCreature(MyCreature(name='Biden', character='B'))
arena.registerCreature(WeakCreature(name='Putin', character='P'))
arena.registerCreature(WeakCreature(name='Xi', character='X'))

arena.registerSource(core.HealthPack, 0.004)
arena.registerSource(core.HealthPack, 0.004)
arena.registerSource(core.Weapon, 0.04)
arena.registerSource(core.Armor, 0.02) 
# arena.pause = True
arena.start()

