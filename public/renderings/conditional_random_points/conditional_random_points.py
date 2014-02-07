#!/usr/bin/python
import PIL.Image, random

rnd = random.Random()

size = 100
iterations = 100000
white = 255
black = 0

def valueFor(x, y):
  c = 0
  for i in [-1,0,1]:
    for j in [-1,0,1]:
      if pixel[x+i,y+j] == black:
        c += 1
  return c

def iterate():
  x, y = rnd.randrange(1,size-2), rnd.randrange(1,size-2)
  if valueFor(x, y) in rule:
    pixel[x,y] = black


for i in range(2**7, 2**9): # 10000000 to 111111111
  rnd.seed(0)
  rule = [d for d in range(9) if (i>>(8-d))%2]

  image = PIL.Image.new('L',(size,size), white)
  pixel = image.load()
  pixel[size/2, size/2] = black

  for _ in range(iterations):
    iterate()

  filename = ''.join([d in rule and str(d) or 'x' for d in range(9)]) + '.png'
  image.resize((size*4,size*4)).save(filename)
  print filename
