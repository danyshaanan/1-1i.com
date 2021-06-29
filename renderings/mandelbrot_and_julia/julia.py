#!/bin/python
import math, PIL.Image

w, h = 300, 300
x, y = 0, 0
zoom = 80
radius = 2 ** 3
maxIterations = 41

half = 5

def julia(z, x, y):
  return z ** 2 + x + y * 1j

areal = [(a, (a - w / 2) / zoom + x) for a in range(w)]
bimag = [(b, (b - h / 2) / zoom + y) for b in range(h)]

for (yIndex, yVal) in [(v, v / half) for v in range(-half, half + 1)]:
  for (xIndex, xVal) in [(v, v / half) for v in range(-half, half + 1)]:
    image = PIL.Image.new('L', (w, h), 0)
    pixel = image.load()

    for a, real in areal:
      for b, imag in bimag:
        z = real + imag * 1j
        cz = z
        i = 0
        while i < maxIterations and abs(z) < radius:
          z = julia(z, xVal, yVal)
          i += 1
        if i < maxIterations:
          pixel[a, b] = int(128 + 128 * math.sin(i - math.log(abs(z), radius)))

    image.save(f'output/julia_{10000 + (yIndex+half)*100 + (xIndex+half)}.png')

'''
# the code above generates a set of small images,
# which can be combined to one big image using these imagemagick command lines:

mkdir temp
convert julia_100*.png +append temp/line00.png
convert julia_101*.png +append temp/line01.png
convert julia_102*.png +append temp/line02.png
convert julia_103*.png +append temp/line03.png
convert julia_104*.png +append temp/line04.png
convert julia_105*.png +append temp/line05.png
convert julia_106*.png +append temp/line06.png
convert julia_107*.png +append temp/line07.png
convert julia_108*.png +append temp/line08.png
convert julia_109*.png +append temp/line09.png
convert julia_110*.png +append temp/line10.png
convert temp/line*.png -append julia.png
mogrify -resize 900x900 julia.png
rm -rf temp
'''