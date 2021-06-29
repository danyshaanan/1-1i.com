#!/bin/python
import PIL.Image, math

step = 0.004
p, o, b = 28, 10, 8/3
zoom = 6
frames = 66

for i in range(frames):
  image = PIL.Image.new('1', (800, 400), 0)
  pixel = image.load()
  teta = math.tau * i / frames

  x = y = z = 1
  for _ in range(10_000):
    x, y, z = x + (o * (y - x)) * step, y + (x * (p - z) - y) * step, z + (x * y - b * z) * step
    px, py = x * math.sin(teta) + z * math.cos(teta), y
    pixel[zoom * px + image.width / 2, zoom * py + image.height / 2] = 1

  image.save(f'output/lorenz{10000 + i}.png')

# the code above generates a set of still images,
# which can be combined to an animated gif using this imagemagick command line:
# convert -delay 1 -loop 0 lorenz*png lorenz.gif