#!/usr/bin/python
import PIL.Image

for name, w, h in [('whole', 800, 200), ('detail', 800, 750)]:
  image = PIL.Image.new('L', (w, h), 255)
  pixel = image.load()

  for c in range(image.width):
    r = 4 + (c - w) / h
    x = .5
    for i in range(200):
      x = r * x * (1 - x)
      pixel[c, h * (1 - x) - 1] = 200 - i
  image.save(f'output/logistic_map_{name}.png')
