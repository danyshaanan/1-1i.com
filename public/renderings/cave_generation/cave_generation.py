#!/usr/bin/python
import PIL.Image, random


size = 200
light = 255
dark = 0
colorBalance = 0.5
area = [-1,0,1]


screenShotsAtIterations = [0] + [2**i for i in range(10,21)]
iterations = screenShotsAtIterations[-1]
neighbours = [(i,j) for i in area for j in area if i!=0 or j!=0]
neighboursCount = len(neighbours)
rnd = random.Random()
rnd.seed(0)
image = PIL.Image.new('L',(size,size), light)
pixel = image.load()

for x in range(size):
  for y in range(size):
    pixel[x,y] = rnd.random() < colorBalance and light or dark

for i in range(iterations+1):
  if (i in screenShotsAtIterations):
    filename = 'cave_' + str(1000000000+i) + '.png'
    image.save(filename)
    print filename
    if i == screenShotsAtIterations[-1]:
      image.resize((size*4,size*4)).save('cave_final_big.png')

  x = rnd.randrange(size)
  y = rnd.randrange(size)
  currentColor = pixel[x,y]
  darkNeighbours = sum(pixel[(x+i)%size,(y+j)%size] == dark for (i,j) in neighbours)
  lightNeighbours = neighboursCount - darkNeighbours
  if darkNeighbours > lightNeighbours:
    pixel[x,y] = dark
  elif lightNeighbours > darkNeighbours:
    pixel[x,y] = light

# the code above generates a set of still images,
# which can be combined to an animated gif using this imagemagick command line:
# convert cave_1*.png -set delay 15 -reverse cave_1*.png -set delay 25 -loop 0 cave.gif
