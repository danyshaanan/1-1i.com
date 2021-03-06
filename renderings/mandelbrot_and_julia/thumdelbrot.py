#!/bin/python
import math, PIL.Image

x, y = -0.7, 0
radius = 2**3
maxIterations = 20

mandelbrot = lambda z, source: z * z + source
createRGBA = lambda v: (lambda v: (v, v, v, 255 - v))(int(v))

for s in [900, 450, 300, 100]:
  zoom = s // 3
  aList = [(p - s / 2) / zoom + x for p in range(s)]
  bList = [(p - s / 2) / zoom + y for p in range(s)]

  image = PIL.Image.new('RGBA', (s, s), createRGBA(0))
  pixel = image.load()

  for pa, a in enumerate(aList):
    for pb, b in enumerate(bList):
      z = source = a + b*1j
      i = 0
      while i < maxIterations and abs(z) < radius:
        z = mandelbrot(z, source)
        i += 1
      if i < maxIterations:
        contI = i - math.log(abs(z), radius)
        pixel[pb, pa] = createRGBA(127 + 128 * math.cos(contI / maxIterations * math.pi))

  image.save(f'output/thumdelbrot_{str(s).rjust(5, "0")}px.png')

