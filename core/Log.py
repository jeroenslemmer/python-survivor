import core

class Log:
                                                  
  _lines = []

  def __init__(self, width = 40, height = 40):
    self.setSize(width, height)

  def setSize(self,width, height):
    self._width = width
    self._height = height

  def add(self, line : str):
    stdrow = '                                        '
    line = line + stdrow
    self._lines.append(line[:self._width])
    if len(self._lines) > self._height:
      self._lines.pop(0)

  def window(self):
    return self._lines

log = Log()