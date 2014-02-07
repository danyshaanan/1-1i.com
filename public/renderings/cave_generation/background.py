#!/usr/bin/python
import PIL.Image, random


size = 200
light = 255
dark = 230
colorBalance = 0.508
area = [-2,-1,0,1,2]
iterations = 500000

neighbours = [(i,j) for i in area for j in area if i!=0 or j!=0]
neighboursCount = len(neighbours)
rnd = random.Random()
rnd.seed(0)
image = PIL.Image.new('L',(size,size), light)
pixel = image.load()

for x in range(size):
  for y in range(size):
    pixel[x,y] = rnd.random() < colorBalance and light or dark

for i in range(iterations):
  x = rnd.randrange(size)
  y = rnd.randrange(size)
  currentColor = pixel[x,y]
  darkNeighbours = sum(pixel[(x+i)%size,(y+j)%size] == dark for (i,j) in neighbours)
  lightNeighbours = neighboursCount - darkNeighbours
  if darkNeighbours > lightNeighbours:
    pixel[x,y] = dark
  elif lightNeighbours > darkNeighbours:
    pixel[x,y] = light

image.save('cave_background.png')
