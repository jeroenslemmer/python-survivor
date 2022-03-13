import os
# import unicurses as curses

class Display:
  _lines = []

  def __init__(self):
    pass

  def _clearConsole(self):
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)
 
  def render(self):
    self._clearConsole()
    for line in self._lines:
      print(line)

  def addWindow(self, x: int, y: int, window):
    if isinstance(window, str):
      window = window.splitlines()
    while len(self._lines) < y + len(window):
      self._lines.append('')
    l = 0
    while  l < len(window):
      if len(self._lines[y+l]) < x:
        self._lines[y+l] += ' '*x
      self._lines[y+l] = self._lines[y+l][:x] + window[l] + self._lines[y+l][x+len(window[l]):]
      l += 1

# display = Display()

# w1 = '''\
# *********
# *       *
# *       *
# *********
# '''
# display.addWindow(15,2,w1)
# display.addWindow(10,7,w1)
# display.addWindow(3,3,w1)
# display.render()
