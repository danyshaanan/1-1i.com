#!/usr/bin/python
import PIL.Image, random

rnd = random.Random()
size = 100
env = [-1,0,1]

d = len(env)
keys = ['0'*(d-len(i)) + i for i in [bin(i)[2:] for i in range(2**d)]]
d = len(keys)
rules = ['0'*(d-len(i)) + i for i in [bin(i)[2:] for i in range(2**d)]]

for rule in rules:
  rnd.seed(0)
  im = PIL.Image.new("L", (size,size))
  pix = im.load()

  for j in [0]:
    for i in range(size):
      pix[i,j] = 255 * rnd.randrange(2)

  for j in range(1,size):
    for i in range(size):
      key = ''.join([str(pix[(i+d)%size,(j-1)%size]/255) for d in env])
      pix[i,j] = 255 * int(rule[int(key, 2)])

  im.resize((size*4,size*4)).save(rule + '.png')
