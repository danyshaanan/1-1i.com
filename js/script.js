'use strict'

{

////////////////////////////////////////////////////////////////////////////////

const defaultSize = 256

const Element = size => {
  const canvas = document.createElement('canvas')
  canvas.width = canvas.height = size
  return { canvas, ctx: canvas.getContext('2d') }
}

const Matrix = size => {
  const { canvas, ctx } = Element(size)
  const image = ctx.getImageData(0, 0, size, size)
  const url = _ => (ctx.putImageData(image, 0, 0), canvas.toDataURL())
  const dot = (x, y, l = 0) => {
    let i = 4 * ((x|0) + size * (y|0)) + 4
    image.data[--i] = 255
    if (l) while (i % 4) image.data[--i] = l
  }
  return { dot, url }
}

const Canvas = size => {
  const { canvas, ctx } = Element(size)
  const rect = ctx.fillRect.bind(ctx)
  const url = canvas.toDataURL.bind(canvas)
  const transform = ctx.transform.bind(ctx)
  const polygon = (points, width, close, fill) => {
    ctx.lineWidth = width
    if (close) ctx.moveTo(...points[points.length - 1])
    points.forEach(p => ctx.lineTo(...p))
    fill ? ctx.fill() : ctx.stroke()
  }
  return { transform, rect, polygon, url }
}

const Random = seed => _ => (seed = seed * 48271 % 2147483647)
const RandomBool = seed => (r => _ => r() % 2)(Random(seed))
const RandomFloat = seed => (r => _ => r() / 2147483647)(Random(seed))

////////////////////////////////////////////////////////////////////////////////

const eca_pattern = i => (2**8 + i).toString(2).slice(1).split('').map(v => +v)

const eca = (id, size = defaultSize) => {
  const pattern = eca_pattern(id)
  const { dot, url } = Matrix(size)
  const init_row = [...Array(size).keys()].map(RandomBool(1))

  for (let r = 0, row = init_row; r < size; r++) {
    const nextRow = []
    for (let i = 0; i < size; i++) {
      if (!row[i]) dot(i, r)
      nextRow[i] = pattern[4 * row[(i - 1 + size) % size] + 2 * row[i] + row[(i + 1) % size]]
    }
    row = nextRow
  }

  return { src: url(), title: id + ': ' + JSON.stringify(pattern) }
}

eca.range = [0, 2**8]

////////////////////////////////////////////////////////////////////////////////

const mr4_pattern = i => [i & 0xf, i >> 4].map(n => [1,2,4,8].map(d => +!!(d & n)))

const mrx = (S, pattern, size = defaultSize, block = 2**2) => {
  const { rect, url } = Canvas(size)

  if (typeof pattern === 'number') pattern = mr4_pattern(pattern)

  const square = (x, y, s, color) => {
    if (s > block)
      for (const i of [...Array(S).keys()])
        for (const j of [...Array(S).keys()])
          square(x + i * s/S, y + j * s/S, s/S, pattern[color][i + S * j])
    else if (color) rect(x, y, s, s)
  }
  square(0, 0, size, 0)

  return { src: url(), title: JSON.stringify(pattern) }
}

const mr9 = mrx.bind(null, 3)
const mr4 = mrx.bind(null, 2)

mr4.range = [0, 2**8]

////////////////////////////////////////////////////////////////////////////////

const Lorentz = (m = 0) => {
  const [p, o, b] = [28, 10, 8 / 3]
  let [x, y, z] = [1, 1, 1]
  return s => {
    ;[x, y, z] = [x + (o * (y - x)) * s, y + (x * (p - z) - y) * s, z + (x * y - b * z) * s]
    return { x, y, z }
  }
}

const lor = (id, size = defaultSize, block = 2**2) => {
  const { dot, url } = Matrix(size)
  const iterate = Lorentz(id / 1000)
  const trans = v => size * (v / 66 + 0.5)
  const xya = (x, y, a) => x * Math.sin(a) + y * Math.cos(a)

  for (let i=0; i < 20000; i++) {
    const {x, y, z} = iterate(0.0012)
    dot(trans(xya(x, y, id / 5 * Math.PI / 2)), trans(z - 25))
  }

  return { src: url(), title: `alpha = ${id / 10} * PI` }
}

lor.range = [0, 6]

////////////////////////////////////////////////////////////////////////////////

const cvg = (id, s = defaultSize) => {
  const random = RandomBool(id)
  const a = []
  for (let x = 0; x < s; x++) for (let y = (a[x] = [], 0); y < s; y++) a[x][y] = random()

  for (let _ = 0; _ < 5; _++) {
    for (let x = 0; x < s; x++) {
      for (let y = 0; y < s; y++) {
        const sum = a[(x+s-1)%s][(y+s-1)%s] +
                    a[   x     ][(y+s-1)%s] +
                    a[(  x+1)%s][(y+s-1)%s] +
                    a[(  x+1)%s][   y     ] +
                    a[(  x+1)%s][(  y+1)%s] +
                    a[   x     ][(  y+1)%s] +
                    a[(x+s-1)%s][(  y+1)%s] +
                    a[(x+s-1)%s][   y     ] // This ugly thing is highly performant :[
        if (sum > 4) a[x][y] = 1
        if (sum < 4) a[x][y] = 0
      }
    }
  }

  const { dot, url } = Matrix(s)
  for (let x = 0; x < s; x++) {
    for (let y = 0; y < s; y++) {
      if (a[x][y]) dot(x, y)
    }
  }

  return { src: url(), title: `Cave id #${id}` }
}

cvg.range = [1, 5]

////////////////////////////////////////////////////////////////////////////////

const cst = (o, size = defaultSize, block = 2**2) => {
  const { transform, polygon, url } = Canvas(size)
  const p = 4
  const zoom = .4 * size
  const random = RandomFloat(o.seed)
  const cis = (r, a) => [r * Math.cos(a), r * Math.sin(a)]

  let points = [...Array(p).keys()].map(n => n/p*2*Math.PI).map(a => ([Math.sin(a), Math.cos(a)]))

  for (let _ = 0; _ < o.iterations; _++) {
    let temp = []
    for (let i = 0; i < points.length; i++) {
      const a = points[i]
      const b = points[(i + 1) % points.length]
      temp.push(a)
      const dist = Math.hypot(a[0] - b[0], a[1] - b[1])
      if (dist < 3 / zoom) continue
      const vector = cis(.6 * dist * random(), 2 * Math.PI * random())
      temp.push([0, 1].map(i => (a[i] + b[i]) / 2 + vector[i]))
    }
    points = temp
  }

  transform(zoom, 0, 0, zoom, size / 2, size / 2)
  polygon(points, 1/zoom, 1, o.fill)

  return { src: url(), title: JSON.stringify(o) }
}

cst.range = [0, 40]

////////////////////////////////////////////////////////////////////////////////

const fractals = [
  ['Sierpinski', 6, 'a',      { a: '-b+a+b-', b: '+a-b-a+' }],
  ['Koch',       6, 'ftftft', { f: 'f-f++f-f' }],
  ['Hilbert',    4, 'A',      { A: '-Bf+AfA+fB-', B: '+Af-BfB-fA+'}],
  ['Dragon 1',   4, 'x',      { x: 'x+yf', y: 'fx-y' }],
  ['Dragon 2',   8, '+a',     { a: 'a+f+b', b: 'a-f-b'}],
  ['Shell',      4, 'f',      { f: '-f+ff+f-'}]
].map(([name, a, start, dict]) => {
  let path = start
  while (path.length < 2000) path = path.replace(/./g, c => dict[c] || c)
  return { name, path: path.replace(/[AB]/g, ''), angle: Math.PI * 2 / a, tAngle: Math.PI * 4 / start.length }
})

const generatePoints = ({ path, angle, tAngle }) => {
  let [dir, p] = [0, { x: 0, y: 0 }]
  const actions = {
    '+': _ => { dir += angle },
    '-': _ => { dir -= angle },
    't': _ => { dir += tAngle },
    'f': _ => p = { x: p.x + Math.cos(dir), y: p.y + Math.sin(dir) }
  }
  return [...path].map(c => (actions[c] || actions.f)()).filter(Boolean)
}

const getBoundingBox = points => {
  const x = { max: -0/1, min: +0/1 }
  const y = { max: -0/1, min: +0/1 }

  for (const p of points) {
    x.max = Math.max(x.max, p.x)
    x.min = Math.min(x.min, p.x)
    y.max = Math.max(y.max, p.y)
    y.min = Math.min(y.min, p.y)
  }
  return { x, y }
}

const lss = (id, size = defaultSize) => {
  let points = generatePoints(fractals[id])
  const { x, y } = getBoundingBox(points)
  const zoom = size / Math.max(x.max - x.min, y.max - y.min) * 0.95

  const { transform, polygon, url } = Canvas(size)
  transform(zoom, 0, 0, zoom, (size - zoom * (x.max + x.min)) / 2, (size - zoom * (y.max + y.min)) / 2)
  polygon(points.map(({x, y}) => [x, y]), 1/zoom)

  return { src: url(), title: JSON.stringify({}) }
}

////////////////////////////////////////////////////////////////////////////////

const getJulia = c => (z, max) => {
  let [i, [a, b], r2, t] = [0, z, Math.pow(2, 6)]
  while (true) {
    if (++i > max) return Infinity
    if ((t = a * a + b * b) > r2) return Math.max(0, i - Math.log(t) / Math.log(r2))
    ;[a, b] = [a * a - b * b + c[0], 2 * a * b + c[1]]
  }
}
const mandelbrot = (z, max) => getJulia(z)(z, max)

const getDef = (id, size) => {
  const zs = [!1,[0.287,-0.01],[0.159,0.571],[-0.66,0.334],[-0.82,0.176],[0.329,0.470]]
  return { a: id ? 0 : -0.66, b: 0, zoom: 3.3 / size, i: 50, gen: id ? getJulia(zs[id]) : mandelbrot }
}

const mnd = (def, size = defaultSize) => {
  if (typeof def === 'number') def = getDef(def, size)

  const { dot, url } = Matrix(size)

  const getColor = i => isFinite(i) ? 128 + 128 * Math.sin(i) : 0
  const pixelLocation = (x, y) => [(x - size/2) * def.zoom + def.a, (y - size/2) * def.zoom + def.b]

  for (let y = 0; y < size; ++y) {
    for (let x = 0; x < size; ++x) {
      dot(x, y, getColor(def.gen(pixelLocation(x, y), def.i)))
    }
  }

  return { src: url(), title: `?` }
}

////////////////////////////////////////////////////////////////////////////////

const externalize = { eca, mr4, lor, cvg, cst, mr9, lss, mnd }

const wrap = f => (...a) => {
  const [t0, r, t1] = [Date.now(), f(...a), Date.now()]
  return Object.assign(r, { title: r.title + ` (${t1 - t0}ms)`})
}

Object.keys(externalize).forEach(k => window[k] = wrap(externalize[k]))

}
