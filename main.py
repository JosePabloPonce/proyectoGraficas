from gl import *

def gourad(render, **kwargs):
  w, v, u = kwargs['bar']
  tx, ty = kwargs['texture_coords']
  tcolor = render.active_texture.get_color(tx, ty)
  nA, nB, nC = kwargs['varying_normals']
  iA, iB, iC = [ dot(n, render.light) for n in (nA, nB, nC) ]
  intensity = w*iA + v*iB + u*iC
  return color(
      int(tcolor[2] * intensity) if tcolor[0] * intensity > 0 else 0,
      int(tcolor[1] * intensity) if tcolor[1] * intensity > 0 else 0,
      int(tcolor[0] * intensity) if tcolor[2] * intensity > 0 else 0
    )

r = Render(700, 700)

for x in range(0, 700):
    for y in range(350,700):
        r.point(x,y,color(82, 168, 243))


t = Texture('./models/nanachi.bmp')
r.light = V3(0, 0, 1)
r.active_texture = t
r.active_shader = gourad
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load('./models/nanachi.obj', translate=(-0.45, -0.25, 0), scale=(0.13, 0.13, 0.13), rotate=(0, 0.85, 0))
r.draw_arrays('TRIANGLES')


t = Texture('./models/reg.bmp')
r.light = V3(0, 0, 1)
r.active_texture = t
r.active_shader = gourad
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load('./models/reg.obj', translate=(-0.68, -0.28, 0), scale=(0.14, 0.14, 0.14), rotate=(0, 1.4, 0))
r.draw_arrays('TRIANGLES')

t = Texture('./models/beastars.bmp')
r.light = V3(0, 0, 1)
r.active_texture = t
r.active_shader = gourad
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load('./models/beastars.obj', translate=(-0.21, 0.05, 0), scale=(0.26, 0.26, 0.26), rotate=(0, 0.6, 0))
r.draw_arrays('TRIANGLES')

t = Texture('./models/mitty.bmp')
r.light = V3(0, 0, 1)
r.active_texture = t
r.active_shader = gourad
r.lookAt(V3(1, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
r.load('./models/mitty.obj', translate=(-0.3, -0.68, 0), scale=(0.08, 0.08, 0.08), rotate=(0, 1.6, 0))
r.draw_arrays('TRIANGLES')

r.light = V3(0, 0, 1)
r.lookAt(V3(1, 0, 0), V3(0, 0, 0), V3(1, 1.6, 0))
r.load('./models/reg1.obj', translate=(-0.2, -0.6, -0.4), scale=(0.2,0.2,0.2), rotate=(0.2, 0.89, 0))
r.draw_arrays('TRIANGLES')

r.display('out.bmp')

