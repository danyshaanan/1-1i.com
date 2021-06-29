#!/bin/python
import math, PIL.Image

w, h = 900, 900
x, y = -0.7, 0
zoom = 300
radius = 2 ** 3
maxIterations = 41



def mandelbrot(z, cz):
  return z ** 2 + cz

areal = [(a, (a - w / 2) / zoom + x) for a in range(w)]
bimag = [(b, (b - h / 2) / zoom + y) for b in range(h)]

if True:
  if True:
    image = PIL.Image.new('L', (w, h), 0)
    pixel = image.load()

    for a, real in areal:
      for b, imag in bimag:
        z = real + imag * 1j
        cz = z
        i = 0
        while i < maxIterations and abs(z) < radius:
          z = mandelbrot(z, cz)
          i += 1
        if i < maxIterations:
          pixel[a, b] = int(128 + 128 * math.sin(i - math.log(abs(z), radius)))

    image.save('output/mandelbrot.png')

