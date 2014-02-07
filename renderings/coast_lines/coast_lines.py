from PIL import Image, ImageDraw
import random, math

rnd = random.Random()
iterations = 12
x, y = 450, 450
r = min(x,y)/2 * 0.82 # initial shape radius is 82% of image radius

for gon in [2,3,4]:

  points = [(x/2+r*math.cos(2.*math.pi*i/gon),y/2+r*math.sin(2.*math.pi*i/gon)) for i in range(gon)]

  for seed in range(3):
    rnd.seed(seed)
    lines = [(points[i],points[(i+1)%gon]) for i in range(gon)]
    im = Image.new("L", (x,y), 255)
    draw = ImageDraw.Draw(im)

    for i in range(iterations):

      for l in lines:
        draw.line((l[0], l[1]), fill=175)

      newLines = []
      for l in lines:
        s = l[0]
        e = l[1]
        d = 0.32 * ((s[0]-e[0])**2 + (s[1]-e[1])**2)**0.5
        alpha = rnd.random() * 2 * math.pi
        mx = (s[0]+e[0])/2 + d * math.cos(alpha)
        my = (s[1]+e[1])/2 + d * math.sin(alpha)
        m = (mx, my)
        newLines += [(s,m),(m,e)]
      lines = newLines

    for l in lines:
      draw.line((l[0], l[1]), fill=0)
    im.save('coast_line_' + str(gon) + '_' + str(seed) + '_0.png')

    im = Image.new("L", (x,y), 255)
    draw = ImageDraw.Draw(im)
    draw.polygon([l[0] for l in lines], fill=0)
    im.save('coast_line_' + str(gon) + '_' +str(seed) + '_1.png')

