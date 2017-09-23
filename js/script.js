'use strict'

const {
  eca, mr4, lor
}=(_=>{

////////////////////////////////////////////////////////////////////////////////

const defaultSize = 128

const dot = (data, x, y, r = 0, g = 0, b = 0, a = 255) => {
  const i = 4 * ((x|0) + (y|0) * data.width)
  data.data[i + 0] = r
  data.data[i + 1] = g
  data.data[i + 2] = b
  data.data[i + 3] = a
}

////////////////////////////////////////////////////////////////////////////////

const eca_pattern = i => (2**8 + i).toString(2).slice(1).split('').map(v => +v)

const eca_init_row = [...Array(2**8).keys()].map(n => (''+Math.sin(n+1))[7]%2)

function eca(id, size = defaultSize) {
  const pattern = eca_pattern(id)

  const canvas = document.createElement('canvas')
  canvas.width = canvas.height = size
  const ctx = canvas.getContext('2d')
  const image = ctx.getImageData(0, 0, size, size)

  let row = eca_init_row

  for (let r = 0; r < size; r++) {
    const nextRow = []
    for (let i = 0; i < size; i++) {
      if (!row[i]) dot(image, i, r)
      nextRow[i] = pattern[4 * row[(i - 1 + size) % size] + 2 * row[i] + row[(i + 1) % size]]
    }
    row = nextRow
  }
  ctx.putImageData(image, 0, 0)

  return {
    id,
    size,
    title: id + ': ' + JSON.stringify(pattern),
    src: canvas.toDataURL()
  }
}

eca.range = [0, 2**8]

////////////////////////////////////////////////////////////////////////////////

const mr4_pattern = i => [i & 0xf, i >> 4].map(n => [1,2,4,8].map(d => +!!(d & n)))

function mr4(id, size = defaultSize, block = 2**2) {
  const pattern = mr4_pattern(id)

  const canvas = document.createElement('canvas')
  canvas.width = canvas.height = size
  const ctx = canvas.getContext('2d')

  const square = (x, y, s, color) => {
    if (s > block)
      for (const i of [0,1])
        for (const j of [0,1])
          square(x + i * s/2, y + j * s/2, s/2, pattern[color][i + 2 * j])
    else if (color) ctx.fillRect(x, y, s, s)
  }
  square(0, 0, size, 0)

  return {
    id,
    size,
    title: id + ': ' + JSON.stringify(pattern),
    src: canvas.toDataURL()
  }
}

mr4.range = [0, 2**8]

////////////////////////////////////////////////////////////////////////////////

function Lorentz() {
  const [p, o, b] = [28, 10, 8 / 3]
  let [x, y, z] = [1, 1, 1]

  return s => {
    ;[x, y, z] = [x + (o * (y - x)) * s, y + (x * (p - z) - y) * s, z + (x * y - b * z) * s]
    return { x, y, z }
  }
}

function lor(id, size = defaultSize, block = 2**2) {
  const canvas = document.createElement('canvas')
  canvas.width = canvas.height = size
  const ctx = canvas.getContext('2d')
  const image = ctx.getImageData(0, 0, size, size)

  const iterate = Lorentz()

  const trans = v => size * (v / 60 + 0.5)

  for (let i=0; i<30000; i++) {
    const {x, y, z} = iterate(0.0012)
    dot(image, trans(y), trans(z - 25))
  }

  ctx.putImageData(image, 0, 0)

  return {
    id,
    size,
    title: '',
    src: canvas.toDataURL()
  }
}


////////////////////////////////////////////////////////////////////////////////
return {
  eca, mr4, lor
}})()
