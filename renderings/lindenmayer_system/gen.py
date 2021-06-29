import PIL.Image, PIL.ImageDraw, PIL.ImageChops, math

def growingRate(fractal):
  x = y = direction = 0
  for c in list(fractal['rule'].values())[0]:
    if c == 'r':
      direction += fractal['alpha']
    elif c == 'l':
      direction -= fractal['alpha']
    elif c in 'fab ':
      teta = direction * math.tau / 360
      x += math.cos(teta)
      y += math.sin(teta)
  return math.hypot(x, y)

def drawFractal(fractal):
  r = fractal['length'] / growingRate(fractal) ** fractal['iterations']
  rule, string = fractal['rule'], fractal['start']
  for _ in range(fractal['iterations']):
    string = ''.join([rule[c] if c in rule else c for c in string])

  im = PIL.Image.new('1', (2000, 2000), 1)
  draw = PIL.ImageDraw.Draw(im)
  direction = 0
  x, y = im.width / 2, im.height / 2
  for c in string:
    if   c == 'r': direction += fractal['alpha']
    elif c == 'l': direction -= fractal['alpha']
    elif c == 'R': direction += 90
    elif c == 'L': direction -= 90
    elif c in 'fab ':
      teta = direction * math.tau / 360
      nextX = x + r * math.cos(teta)
      nextY = y + r * math.sin(teta)
      if c != ' ': draw.line((x, y, nextX, nextY) , fill=0)
      x, y = nextX, nextY
  return im.crop(PIL.ImageChops.difference(im, PIL.Image.new(im.mode, im.size, 1)).getbbox())

fractals = [
  { 'name': 'snow_flake_0', 'start': 'f',             'rule':{'f':'flfrrflf'},              'alpha':  60, 'length': 800, 'iterations':  0 },
  { 'name': 'snow_flake_1', 'start': 'f',             'rule':{'f':'flfrrflf'},              'alpha':  60, 'length': 800, 'iterations':  1 },
  { 'name': 'snow_flake_2', 'start': 'f',             'rule':{'f':'flfrrflf'},              'alpha':  60, 'length': 800, 'iterations':  2 },
  { 'name': 'snow_flake_3', 'start': 'f',             'rule':{'f':'flfrrflf'},              'alpha':  60, 'length': 800, 'iterations':  3 },
  { 'name': 'snow_flake_4', 'start': 'f',             'rule':{'f':'flfrrflf'},              'alpha':  60, 'length': 800, 'iterations':  4 },
  { 'name': 'snow_flake_5', 'start': 'f',             'rule':{'f':'flfrrflf'},              'alpha':  60, 'length': 800, 'iterations':  5 },
  { 'name': 'penta_flake' , 'start': 'frfrfrfrf',     'rule':{'f':'frfllfrf'},              'alpha':  72, 'length': 400, 'iterations':  5 },
  { 'name': 'cesaro'      , 'start': 'fRfRfRf',       'rule':{'f':'frfllfrf'},              'alpha':  85, 'length': 800, 'iterations':  4 },
  { 'name': 'swirle'      , 'start': 'frfrfrfrfrf',   'rule':{'f':'frfllffrrflf'},          'alpha':  60, 'length': 500, 'iterations':  4 },
  { 'name': 'sierpinski_1', 'start': 'f',             'rule':{'f':'flfrfrflf'},             'alpha': 120, 'length': 800, 'iterations':  7 },
  { 'name': 'sierpinski_2', 'start': 'a',             'rule':{'a':'blalb', 'b':'arbra'},    'alpha':  60, 'length': 800, 'iterations':  7 },
  { 'name': '21112'       , 'start': 'frfrfrf',       'rule':{'f':'ffrflflfrff'},           'alpha':  90, 'length': 800, 'iterations':  5 },
  { 'name': 'shell'       , 'start': 'rrf',           'rule':{'f':'rflfflfr'},              'alpha':  90, 'length': 400, 'iterations':  6 },
  { 'name': 'dragon'      , 'start': 'a',             'rule':{'a':'arb', 'b':'alb'},        'alpha':  90, 'length': 500, 'iterations': 13 },
  { 'name': 'circles'     , 'start': 'flflflf',       'rule':{'f':'ffrfrfrfrfrflf'},        'alpha':  90, 'length': 800, 'iterations':  5 },
  { 'name': 'star'        , 'start': 'arararara',     'rule':{'a':'aararararallllaa'},      'alpha':  72, 'length': 500, 'iterations':  4 }
]

for fractal in fractals:
  image = drawFractal(fractal)
  image.save(f'output/{fractal["name"]}.png')

