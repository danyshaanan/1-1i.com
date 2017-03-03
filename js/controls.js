

const controls = (_ => {


  return {
    keyboard(def, cb) {
      const actions = {
        73: i => def.i += 20,
        79: o => def.i = Math.max(8, def.i - 20),
        83: s => window.localStorage.def = JSON.stringify(def),
        76: l => Object.assign(def, JSON.parse(window.localStorage.def)),
        78: n => def.generator++,
        37: left => def.jA += 0.01,
        39: right => def.jA -= 0.01,
        38: up => def.jB += 0.01,
        40: down => def.jB -= 0.01,
      }

      window.onkeyup = function(e){
        if (actions[e.keyCode]) {
          e.preventDefault()
          actions[e.keyCode]()
          cb()
        }
        console.log(def)
      }
    },
    mouse(def, canvas, cb) {

      const zoomAround = (zoom, mouseEvent) => {
        def.cA += mouseEvent.layerX * def.zoom
        def.cB += mouseEvent.layerY * def.zoom
        def.zoom *= zoom
        def.cA -= mouseEvent.layerX * def.zoom
        def.cB -= mouseEvent.layerY * def.zoom
      }

      let downE
      canvas.canvas.oncontextmenu = e => false
      canvas.canvas.onmousedown = e => downE = e
      canvas.canvas.onmouseup = upE => {
        const diff = { x: downE.layerX - upE.layerX, y: downE.layerY - upE.layerY }
        if (diff.x*diff.x + diff.y*diff.y > 25) {
          def.cA += diff.x * def.zoom
          def.cB += diff.y * def.zoom
        } else {
          zoomAround(upE.which === 1 ? 0.5 : 2, upE)
        }
        cb()
      }

      canvas.canvas.onwheel = function(e) {
        zoomAround(Math.pow(2, -Math.sign(e.wheelDelta)), e)
        cb()
        return false
      }

    }
  }
})()
