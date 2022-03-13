import sched, time
class Time:
  _routines = []

  def __init__(self, speed=4):
    self._schedule = sched.scheduler(time.time, time.sleep)
    if speed <= 0: speed = 1
    self._delay = 1 / speed

  def _loop(self):
    for routine in self._routines:
      routine()
    # input('Waiting...')
    self._schedule.enter(self._delay, 1, self._loop)

  def register(self, routine):
    self._routines.append(routine)

  def start(self):
    self._loop()
    self._schedule.run()

# time = Time()

# time.register(lambda:(print('hallo')))
# time.register(lambda:(print('how are you doing?')))
# time.register(lambda:(print('goodbye')))

# time.start()
