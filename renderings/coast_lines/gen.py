from PIL import Image, ImageDraw
import random, math

rnd = random.Random()
iterations = 12
x, y = 450, 450
r = min(x, y) / 2 * 0.82 # initial shape radius is 82% of image radius

for gon in [2, 3, 4]:
  angles = [math.tau * i / gon for i in range(gon)]
  points = [(x / 2 + r * math.cos(a), y / 2 + r * math.sin(a)) for a in angles]

  for seed in range(3):
    rnd.seed(seed)
    lines = [(points[i], points[(i + 1) % gon]) for i in range(gon)]
    im = Image.new('L', (x, y), 255)
    draw = ImageDraw.Draw(im)

    for i in range(iterations):
      for l in lines: draw.line((l[0], l[1]), fill=175)

      newLines = []
      for s, e in lines:
        d = 0.32 * math.hypot(s[0] - e[0], s[1] - e[1])
        alpha = rnd.random() * math.tau
        m = ((s[0] + e[0]) / 2 + d * math.cos(alpha), (s[1] + e[1]) / 2 + d * math.sin(alpha))
        newLines += [(s, m), (m, e)]
      lines = newLines

    for l in lines: draw.line((l[0], l[1]), fill=0)
    im.save(f'output/coast_line_{gon}_{seed}_0.png')

    im = Image.new('L', (x,y), 255)
    ImageDraw.Draw(im).polygon([l[0] for l in lines], fill=0)
    im.save(f'output/coast_line_{gon}_{seed}_1.png')

