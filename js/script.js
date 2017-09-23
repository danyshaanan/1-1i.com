'use strict'

const {
  eca, mr4, lor
}=(_=>{

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
  const dot = (x, y) => image.data[4 * ((x|0) + size * (y|0)) + 3] = 255
  return { dot, url }
}

const Canvas = size => {
  const { canvas, ctx } = Element(size)
  const rect = ctx.fillRect.bind(ctx)
  const url = canvas.toDataURL.bind(canvas)
  return { rect, url }
}

////////////////////////////////////////////////////////////////////////////////

const eca_pattern = i => (2**8 + i).toString(2).slice(1).split('').map(v => +v)
const eca_init_row = [...Array(2**8).keys()].map(n => (''+Math.sin(n+1))[7]%2)

const eca = (id, size = defaultSize) => {
  const pattern = eca_pattern(id)
  const { dot, url } = Matrix(size)

  for (let r = 0, row = eca_init_row; r < size; r++) {
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

const mr4 = (id, size = defaultSize, block = 2**2) => {
  const pattern = mr4_pattern(id)
  const { rect, url } = Canvas(size)

  const square = (x, y, s, color) => {
    if (s > block)
      for (const i of [0,1])
        for (const j of [0,1])
          square(x + i * s/2, y + j * s/2, s/2, pattern[color][i + 2 * j])
    else if (color) rect(x, y, s, s)
  }
  square(0, 0, size, 0)

  return { src: url(), title: id + ': ' + JSON.stringify(pattern) }
}

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
return {
  eca, mr4, lor
}})()
