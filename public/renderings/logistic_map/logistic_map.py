#!/usr/bin/python
import PIL.Image

for (name, w, h) in [('whole', 800, 200), ('detail', 800, 750)]:
  image = PIL.Image.new('L',(w,h),255)
  pixel = image.load()

  for p in range(w):
    r = 1. * p/h + (4-1.*w/h)
    x = 0.5
    for i in range(200):
      x = r * x * (1-x)
      pixel[p,x*h] = 200 - i
  image.transpose(PIL.Image.FLIP_TOP_BOTTOM).save('logistic_map_' + name + '.png')
