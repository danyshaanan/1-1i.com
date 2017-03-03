'use strict'

function Canvas() {
  const canvas = document.createElement('canvas')
  let ctx, imageData

  const set = function(x, y, c) {
    const index = (canvas.width * y + x) << 2
    imageData.data[index+0] = 255 * c.r % 256
    imageData.data[index+1] = 255 * c.g % 256
    imageData.data[index+2] = 255 * c.b % 256
    imageData.data[index+3] = 255
  }

  document.body.appendChild(canvas)

  return {
    canvas,
    init() {
      canvas.width = document.documentElement.clientWidth
      canvas.height = document.documentElement.clientHeight
      ctx = canvas.getContext('2d')
      imageData = ctx.getImageData(0, 0, canvas.width, canvas.height)
    },
    drawPixels(cb) {
      const t = Date.now()
      for (let y = 0; y < canvas.height; ++y) {
        for (let x = 0; x < canvas.width; ++x) {
          set(x, y, cb(x, y))
        }
      }
      ctx.putImageData(imageData, 0, 0)
      document.title = Date.now() - t
    }
  }
}
