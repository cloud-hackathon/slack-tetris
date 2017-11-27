import random


# game field params
HEIGHT = 21
WIDTH = 12


class Tetris:

  def __init__(self):
    self.player = None
    self.playing = False

    self.blocks = [
      [0, 1, -WIDTH, -WIDTH, -1], # 1: green Z block
      [0, 1, -WIDTH, -WIDTH*2],   # 2: orange L block
      [0, 1, -WIDTH, WIDTH+1],    # 3: pink S block
      [0, 1, -WIDTH, 2],          # 4: purple J block
      [0, 1, -WIDTH, -WIDTH+1],   # 5: yellow O block
      [-1, 0, 1, 2],              # 6: blue I block
      [-1, 0, 1, -WIDTH]          # 7: red T block
    ]

    # fixed blocks(1-7) or background(0), lane is -1
    self.fixed = []
    for y in range(HEIGHT):
      for x in range(WIDTH):
        if y == HEIGHT - 1:
          self.fixed.append(-1)
        elif x == 0 or x == WIDTH - 1:
          self.fixed.append(-1)
        else:
          self.fixed.append(0)

    # floating block info
    self.id = random.randint(1, len(self.blocks))
    self.floating = self.blocks[self.id - 1]
    self.pos = WIDTH + WIDTH / 2 - 1

  def clear(self):
    for y in range(HEIGHT - 1):
      for x in range(1, WIDTH - 1):
        self.fixed[y * WIDTH + x] = 0

  def move(self, delta):
    movable = True
    for b in self.floating:
      pos = self.pos + b + delta
      if pos >= 0 and self.fixed[int(pos)] != 0:
        movable = False
        break
    if movable:
      self.pos = self.pos + delta
    return movable

  def turn(self):
    movable = True
    rot = []
    for b in self.floating:
      v = int(round(float(b) / float(WIDTH)))
      w = b - v * WIDTH
      p = w * WIDTH - v
      rot.append(p)
      pos = self.pos + p
      if pos >= 0 and self.fixed[int(pos)] != 0:
        movable = False
        break
    if movable:
      self.floating = rot
    return movable

  def down(self):
    movable = True
    if not self.fall():
      self.fix()
      for line in range(HEIGHT - 1):
        if self.full(line):
          self.remove(line)
      if not self.next():
        movable = False
    return movable

  def bottom(self):
    movable = True
    while self.fall():
      pass
    self.fix()
    for line in range(HEIGHT - 1):
      if self.full(line):
        self.remove(line)
    if not self.next():
      movable = False
    return movable

  def fall(self):
    movable = True
    for b in self.floating:
      pos = self.pos + b + WIDTH
      if pos >= 0 and self.fixed[int(pos)] != 0:
        movable = False
        break
    if movable:
      self.pos = self.pos + WIDTH
    return movable

  def fix(self):
    for b in self.floating:
      self.fixed[int(self.pos + b)] = self.id

  def next(self):
    nextId = random.randint(1, len(self.blocks))
    nextFloating = self.blocks[nextId - 1]
    nextPos = WIDTH + WIDTH / 2 - 1
    starting = True
    for b in nextFloating:
      pos = nextPos + b
      if pos >= 0 and self.fixed[int(pos)] != 0:
        starting = False
        break
    if starting:
      self.id = nextId
      self.floating = nextFloating
      self.pos = nextPos
    return starting

  def full(self, line):
    for b in self.fixed[line * WIDTH: (line + 1) * WIDTH]:
      if b == 0:
        return False
    return True

  def remove(self, line):
    del self.fixed[line * WIDTH: (line + 1) * WIDTH]
    top = []
    for x in range(WIDTH):
      if x == 0 or x == WIDTH - 1:
        top.append(-1)
      else:
        top.append(0)
    self.fixed[0: 0] = top

  def block(self, x, y):
    pos = y * WIDTH + x
    for block in self.floating:
      if self.pos + block == pos:
        return self.id
    return self.fixed[int(pos)]
