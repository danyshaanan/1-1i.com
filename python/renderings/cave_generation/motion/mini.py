#!/usr/bin/python
import PIL.Image, random


size = 7
off = 255
on = 0
colorBalance = 0.5
area = [-1,0,1]


iterations = 4
neighbours = [(i,j) for i in area for j in area if i!=0 or j!=0]
image = PIL.Image.new('L',(size,size), off)
pixel = image.load()
image2 = PIL.Image.new('L',(size,size), off)
pixel2 = image2.load()

for x in range(size):
  for y in range(size):
    onCells = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)] + \
              [(2,3),(3,3),(4,3)] + \
              [(6,6),(6,5),(6,4),(5,6),(5,5),(5,4),(4,6),(4,5),(4,4)]
    if ((x,y) in onCells):
      pixel[x,y] = on
    else:
      pixel[x,y] = off
    pixel2[x,y] = pixel[x,y]

for i in range(iterations):

  for x in range(size):
    for y in range(size):
      count = sum(pixel[(x+i)%size,(y+j)%size] == on for (i,j) in neighbours)

      if (pixel[x,y] == on) and (count in [0,1,2,3]): #die
        pixel2[x,y] = off
      if (pixel[x,y] == off) and (count in [5,6,7,8]): #be born
        pixel2[x,y] = on

  for x in range(size):
    for y in range(size):
      pixel[x,y] = pixel2[x,y]

  filename = 'mini_' + str(1000000000+i) + '.png'
  image.resize((size*4,size*4)).save(filename)
  print filename
