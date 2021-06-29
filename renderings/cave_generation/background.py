#!/usr/bin/python
import PIL.Image, random

area = [-1, 0, 1]
neighbours = [(i, j) for i in area for j in area if i or j]

rnd = random.Random(0)
image = PIL.Image.new('L',(200 ,200))
pixel = image.load()

for c in range(image.width):
  for r in range(image.height):
    pixel[c, r] = int(rnd.random() < 0.5)

for _ in range(500_000):
  x, y = rnd.randrange(image.width), rnd.randrange(image.height)
  alive = sum(pixel[(x + i) % image.width, (y + j) % image.height] for (i, j) in neighbours)
  if alive > 4: pixel[x, y] = 1
  if alive < 4: pixel[x, y] = 0

for c in range(image.width):
  for r in range(image.height):
    pixel[c, r] = 240 if pixel[c, r] else 255

image.save('cave_background.png')