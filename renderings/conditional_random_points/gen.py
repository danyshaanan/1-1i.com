#!/usr/bin/python
import PIL.Image, random

area = [-1, 0, 1]
neighbours = [(i, j) for i in area for j in area if i or j]

for i in range(2 ** 7, 2 ** 9):
  rr = random.Random(0).randrange
  rule = [str(i) if int(c) else 'x' for i, c in enumerate(format(i, '09b'))]
  image = PIL.Image.new('1',(100, 100), 1)
  pixel = image.load()
  pixel[image.width // 2, image.height // 2] = 0

  for _ in range(100_000):
    x, y = rr(1, image.width - 2), rr(1, image.height - 2)
    if rule[[pixel[x + i, y + j] for i, j in neighbours].count(0)] != 'x':
      pixel[x, y] = 0

  image.resize((4 * image.width, 4 * image.height)).save('output/' + ''.join(rule) + '.png')
