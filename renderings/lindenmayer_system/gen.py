import PIL.Image, PIL.ImageDraw, PIL.ImageChops, math

size = 2000

def generateString(s, rule, iterations):
  for i in range(iterations):
    s = ''.join([c in rule and rule[c] or c for c in s])
  return s

def drawString(string, alpha, x, y, r):
  im = PIL.Image.new("L", (size,size), 255)
  draw = PIL.ImageDraw.Draw(im)
  direction = 0
  for i in range(len(string)):
    c = string[i]
    if c == "r":
      direction += alpha
    elif c == "l":
      direction -= alpha
    elif c == "R":
      direction += 90
    elif c == "L":
      direction -= 90
    elif c in "fab ":
      teta = direction * math.pi / 180.0
      nextX = x + r * math.cos(teta)
      nextY = y + r * math.sin(teta)
      if c != " ":
        draw.line((x, y, nextX, nextY) , fill=0)
      x, y = nextX, nextY
  return trim(im)

def calcFractalGrowingRate(rule, alpha):
  x = y = direction = 0
  for c in rule[rule.keys()[0]]:
    if c == "r":
      direction += alpha
    elif c == "l":
      direction -= alpha
    elif c in "fab ":
      teta = direction * math.pi / 180.0
      x += math.cos(teta)
      y += math.sin(teta)
  return math.sqrt(x**2+y**2)

def trim(im):
    bg = PIL.Image.new(im.mode, im.size, 255)
    diff = PIL.ImageChops.difference(im, bg)
    diff = PIL.ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

fractals = {
  "snow_flake_0" : {"start": "f",             "rule":{"f":"flfrrflf"},              "alpha":  60, "length": 800, "iterations":  0},
  "snow_flake_1" : {"start": "f",             "rule":{"f":"flfrrflf"},              "alpha":  60, "length": 800, "iterations":  1},
  "snow_flake_2" : {"start": "f",             "rule":{"f":"flfrrflf"},              "alpha":  60, "length": 800, "iterations":  2},
  "snow_flake_3" : {"start": "f",             "rule":{"f":"flfrrflf"},              "alpha":  60, "length": 800, "iterations":  3},
  "snow_flake_4" : {"start": "f",             "rule":{"f":"flfrrflf"},              "alpha":  60, "length": 800, "iterations":  4},
  "snow_flake_5" : {"start": "f",             "rule":{"f":"flfrrflf"},              "alpha":  60, "length": 800, "iterations":  5},
  "penta_flake"  : {"start": "frfrfrfrf",     "rule":{"f":"frfllfrf"},              "alpha":  72, "length": 400, "iterations":  5},
  "cesaro"       : {"start": "fRfRfRf",       "rule":{"f":"frfllfrf"},              "alpha":  85, "length": 800, "iterations":  4},
  "swirle"       : {"start": "frfrfrfrfrf",   "rule":{"f":"frfllffrrflf"},          "alpha":  60, "length": 500, "iterations":  4},
  "sierpinski_1" : {"start": "f",             "rule":{"f":"flfrfrflf"},             "alpha": 120, "length": 800, "iterations":  7},
  "sierpinski_2" : {"start": "a",             "rule":{"a":"blalb", "b":"arbra"},    "alpha":  60, "length": 800, "iterations":  7},
  "21112"        : {"start": "frfrfrf",       "rule":{"f":"ffrflflfrff"},           "alpha":  90, "length": 800, "iterations":  5},
  "shell"        : {"start": "rrf",           "rule":{"f":"rflfflfr"},              "alpha":  90, "length": 400, "iterations":  6},
  "dragon"       : {"start": "a",             "rule":{"a":"arb", "b":"alb"},        "alpha":  90, "length": 500, "iterations": 13},
  "circles"      : {"start": "flflflf",       "rule":{"f":"ffrfrfrfrfrflf"},        "alpha":  90, "length": 800, "iterations":  5},
  "star"         : {"start": "arararara",     "rule":{"a":"aararararallllaa"},      "alpha":  72, "length": 500, "iterations":  4}
}

for name in fractals.keys():
  fractal = fractals[name]
  string = generateString(fractal["start"], fractal["rule"], fractal["iterations"])
  r = 1. * fractal['length'] / calcFractalGrowingRate(fractal['rule'], fractal['alpha']) ** fractal['iterations']
  image = drawString(string, fractal['alpha'], size/2, size/2, r)
  image.save(name + '.png')

