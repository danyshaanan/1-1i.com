#!/usr/bin/python
import PIL.Image, random

area = [-1, 0, 1]
neighbours = [(i, j) for i in area for j in area if i or j]

rnd = random.Random(0)
image = PIL.Image.new('1',(200 ,200))
pixel = image.load()

for c in range(image.width):
  for r in range(image.height):
    pixel[c, r] = int(rnd.random() < 0.5)

i = 0
for shot in [0] + [2 ** i for i in range(10, 21)]:
  while i < shot:
    x, y = rnd.randrange(image.width), rnd.randrange(image.height)
    alive = sum(pixel[(x + i) % image.width, (y + j) % image.height] for (i, j) in neighbours)
    if alive > 4: pixel[x, y] = 1
    if alive < 4: pixel[x, y] = 0
    i += 1
  image.save(f'output/cave_1{str(shot).rjust(9, "0")}.png')
image.resize((4 * image.width, 4 * image.height)).save('output/cave_final_big.png')

# the code above generates a set of still images,
# which can be combined to an animated gif using this imagemagick command line:
# convert cave_1*.png -set delay 15 -reverse cave_1*.png -set delay 15 -loop 0 cave.gif
