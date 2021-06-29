#!/bin/python
import PIL.Image, math

p = 28
o = 10
b = 8/3.

def iterate(x,y,z, step):
  xChange = o * (y - x)
  yChange = x * (p - z) - y
  zChange = x * y - b * z
  x += xChange * step
  y += yChange * step
  z += zChange * step
  return (x,y,z)

def project(x,y,z, teta):
  horizontal = x*math.sin(teta) + z*math.cos(teta)
  vertical = y
  draw(horizontal, vertical)

width = 800
height = 400

def draw(x,y):
  size = 6
  w = int(size*x+width/2) % width
  h = int(size*y+height/2) % height
  pixel[w,h] = 255


frames = 66

for i in range(frames):
  image = PIL.Image.new("L",(width, height), 0)
  pixel = image.load()
  teta = 2.*math.pi*i/frames

  x = y = z = 1
  for _ in range(10000):
    (x,y,z) = iterate(x,y,z, 0.004)
    project(x,y,z, teta)

  filename = "lorenz" + str(10000 + i) + ".png"
  image.save(filename)
  print filename

# the code above generates a set of still images,
# which can be combined to an animated gif using this imagemagick command line:
# convert -delay 1 -loop 0 lorenz*png lorenz.gif