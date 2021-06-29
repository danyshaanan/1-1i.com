#!/usr/bin/python

import PIL.Image, random

for rule in range(2 ** 2 ** 3):
  im = PIL.Image.new('1', (100, 100))
  px = im.load()
  rr = random.Random(0).randrange

  for r in range(im.height):
    for c in range(im.width):
      px[c, r] = rule & 2 ** (sum([px[(c + 1 - d) % im.width, (r - 1) % im.height] * 2 ** d for d in range(3)])) and 1 if r else rr(2)

  im.resize((4 * p for p in im.size)).save('output/' + format(rule, '08b') + '.png')
