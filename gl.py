from math import *
from obj import Obj, Texture
from lib import *


BLACK = color(130, 180, 22)
WHITE = color(255, 255, 255)
contador=0



class Render(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.current_color = WHITE
    self.clear()
    self.light = V3(0,0,1)
    self.active_texture = None
    self.active_vertex_array = []

  def clear(self):
    
    self.pixels = [
      [BLACK for x in range(self.width)]
      for y in range(self.height)
    ]
    self.zbuffer = [
            [-float('inf') for x in range(self.width)]
            for y in range(self.height)
        ]

  def write(self, filename):
    writebmp(filename, self.width, self.height, self.pixels)

  def display(self, filename='out.bmp'):

    self.write(filename)

    try:
      from wand.image import Image
      from wand.display import display

      with Image(filename=filename) as image:
        display(image)
    except ImportError:
      pass
    
  def set_color(self, color):
    self.current_color = color

  def point(self, x, y, color = None):
    try:
      self.pixels[y][x] = color or self.current_color
    except:
      pass

  def shader(self, A, B, C, x, y, v, u, w):
      global contador
      contador+=1
        
      if (contador < 2000):#piel
          return color(226, 197, 161)
      elif(contador < 2100):#cejas
          return color(173, 164, 153)
      elif(contador < 2200):#pintadorojopiel
          return color(156, 51, 64)
      elif(contador < 4500):#pantalonverdesombra
          return color(52, 98, 91)
      elif(contador < 5000):#pantalonazulpitasysombra
          return color(47, 40, 92)
      elif(contador < 5500):#pantaloncinturongris
          return color(22, 11, 5)
      elif(contador < 5600):#pantalonverdeclaro
          return color(152, 187, 150)
      elif(contador < 12500):#caparoja
          return color(255, 31, 39)
      elif(contador < 18000):#pelo
          return color(36, 25, 21)
      elif(contador < 19000):#brazopartegrisclaramano
          return color(212, 206, 206)
      elif(contador < 21000):#brazoparteoscurapierna
          return color(51, 57, 107)
      elif(contador < 24000):#casco
          return color(23, 27, 51)
      elif(contador < 24200):#ojos
          return color(197, 195, 124)
      elif(contador < 24250):#ojos
          return color(255, 255, 255)
      elif(contador < 28000):#casco
          return color(23, 27, 51)
      elif(contador < 29000):#cascovidrio
          return color(0, 204, 203) 
      else:
          return color(200, 202, 52)



  def triangle(self):
    A = next(self.active_vertex_array)
    B = next(self.active_vertex_array)
    C = next(self.active_vertex_array)

    if self.active_texture:
      tA = next(self.active_vertex_array)
      tB = next(self.active_vertex_array)
      tC = next(self.active_vertex_array)

    nA = next(self.active_vertex_array)
    nB = next(self.active_vertex_array)
    nC = next(self.active_vertex_array)

    bbox_min, bbox_max = bbox(A, B, C)

    normal = norm(cross(sub(B, A), sub(C, A)))
    intensity = dot(normal, self.light)
    if intensity < 0:
      return

    for x in range(bbox_min.x, bbox_max.x + 1):
      for y in range(bbox_min.y, bbox_max.y + 1):
        w, v, u = barycentric(A, B, C, V2(x, y))
        if w < 0 or v < 0 or u < 0:  # 0 is actually a valid value! (it is on the edge)
          continue

        if self.active_texture:
          tx = tA.x * w + tB.x * v + tC.x * u
          ty = tA.y * w + tB.y * v + tC.y * u

        color = self.active_shader(
            self,
            triangle=(A, B, C),
            bar=(w, v, u),
            texture_coords=(tx, ty),
            varying_normals=(nA, nB, nC)
        )


        if contador>=4:
          color = self.shader(A, B, C, x, y, v, u, w)


        z = A.z * w + B.z * v + C.z * u

        if x < 0 or y < 0:
          continue

        if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[x][y]:
          self.point(x, y, color)
          self.zbuffer[x][y] = z

  def transform(self, vertex):
    augmented_vertex = [[
      vertex.x],
      [vertex.y],
      [vertex.z],
      [1]
    ]


    result3 = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]

    result4 = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]

    result5 = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]

    tranformed_vertex = [[0], [0], [0], [0]]
    
    #primeras2
    for i in range(len(self.Viewport)):
 
        for j in range(len(self.Projection[0])):
 
            for k in range(len(self.Projection)):
                result3[i][j] += self.Viewport[i][k] * self.Projection[k][j]

    #primeras3
    for i in range(len(result3)):
 
        for j in range(len(self.View[0])):
 
            for k in range(len(self.View)):
                result4[i][j] += result3[i][k] * self.View[k][j]

    #primeras4
    for i in range(len(result4)):
 
        for j in range(len(self.Model[0])):
 
            for k in range(len(self.Model)):
                result5[i][j] += result4[i][k] * self.Model[k][j]
    
    #primeras5
    for i in range(len(result5)):
 
        for j in range(len(augmented_vertex[0])):
 
            for k in range(len(augmented_vertex)):
                tranformed_vertex[i][j] += result5[i][k] * augmented_vertex[k][j]
    lista=[]
    for i in range(0,4):
        lista.append(tranformed_vertex[i][0])
        
    tranformed_vertex = lista

    tranformed_vertex = [
      (tranformed_vertex[0]/tranformed_vertex[3]),
      (tranformed_vertex[1]/tranformed_vertex[3]),
      (tranformed_vertex[2]/tranformed_vertex[3])
    ]
    return V3(*tranformed_vertex)

  def load(self, filename, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
    self.loadModelMatrix(translate, scale, rotate)

    model = Obj(filename)
    vertex_buffer_object = []
    #print(len(model.faces))
    for face in model.faces:
        for facepart in face:
          vertex = self.transform(V3(*model.vertices[facepart[0]]))
          vertex_buffer_object.append(vertex)

        if self.active_texture:
          for facepart in face:
            tvertex = V3(*model.tvertices[facepart[1]])
            vertex_buffer_object.append(tvertex)

          for facepart in face:
            nvertex = V3(*model.normals[facepart[2]])
            vertex_buffer_object.append(nvertex)

    self.active_vertex_array = iter(vertex_buffer_object)

  def loadModelMatrix(self, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
    translate = V3(*translate)
    scale = V3(*scale)
    rotate = V3(*rotate)

    translation_matrix = [
      [1, 0, 0, translate.x],
      [0, 1, 0, translate.y],
      [0, 0, 1, translate.z],
      [0, 0, 0, 1]
    ]



    a = rotate.x
    rotation_matrix_x = [
      [1, 0, 0, 0],
      [0, cos(a), -sin(a), 0],
      [0, sin(a),  cos(a), 0],
      [0, 0, 0, 1]
    ]

    a = rotate.y
    rotation_matrix_y = [
      [cos(a), 0,  sin(a), 0],
      [     0, 1,       0, 0],
      [-sin(a), 0,  cos(a), 0],
      [     0, 0,       0, 1]
    ]

    a = rotate.z
    rotation_matrix_z = [
      [cos(a), -sin(a), 0, 0],
      [sin(a),  cos(a), 0, 0],
      [0, 0, 1, 0],
      [0, 0, 0, 1]
    ]
    
    result = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]

    rotation_matrix = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]
    
    result2 = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]
    
    self.Model = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]
    

    #primeras2
    for i in range(len(rotation_matrix_y)):
 
        for j in range(len(rotation_matrix_x[0])):
 
            for k in range(len(rotation_matrix_x)):
                result[i][j] += rotation_matrix_y[i][k] * rotation_matrix_x[k][j]
 
    #ultimas2
    for i in range(len(result)):
 
        for j in range(len(rotation_matrix_z[0])):
 
            for k in range(len(rotation_matrix_z)):
                rotation_matrix[i][j] += result[i][k] * rotation_matrix_z[k][j]
 


    scale_matrix = [
      [scale.x, 0, 0, 0],
      [0, scale.y, 0, 0],
      [0, 0, scale.z, 0],
      [0, 0, 0, 1]
    ]

    #primeras2
    for i in range(len(translation_matrix)):
 
        for j in range(len(rotation_matrix[0])):
 
            for k in range(len(rotation_matrix)):
                result2[i][j] += translation_matrix[i][k] * rotation_matrix[k][j]

    #ultimas2
    for i in range(len(result2)):
 
        for j in range(len(scale_matrix[0])):
 
            for k in range(len(scale_matrix)):
                self.Model[i][j] += result2[i][k] * scale_matrix[k][j]
 


  def loadViewMatrix(self, x, y, z, center):
    M = [
      [x.x, x.y, x.z,  0],
      [y.x, y.y, y.z, 0],
      [z.x, z.y, z.z, 0],
      [0,     0,   0, 1]
    ]

    O = [
      [1, 0, 0, -center.x],
      [0, 1, 0, -center.y],
      [0, 0, 1, -center.z],
      [0, 0, 0, 1]
    ]

    self.View = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]
    
        #primeras2
    for i in range(len(M)):
 
        for j in range(len(O[0])):
 
            for k in range(len(O)):
                self.View[i][j] += M[i][k] * O[k][j]

  def loadProjectionMatrix(self, coeff):
    self.Projection =  [
      [1, 0, 0, 0],
      [0, 1, 0, 0],
      [0, 0, 1, 0],
      [0, 0, coeff, 1]
    ]

  def loadViewportMatrix(self, x = 0, y = 0):
    self.Viewport =  [
      [self.width/2, 0, 0, x + self.width/2],
      [0, self.height/2, 0, y + self.height/2],
      [0, 0, 128, 128],
      [0, 0, 0, 1]
    ]

  def lookAt(self, eye, center, up):
    z = norm(sub(eye, center))
    x = norm(cross(up, z))
    y = norm(cross(z, x))
    self.loadViewMatrix(x, y, z, center)
    self.loadProjectionMatrix(-1 / length(sub(eye, center)))
    self.loadViewportMatrix()

  def draw_arrays(self, polygon):
    global contador

    if polygon == 'TRIANGLES':
      try:
        while True:
          self.triangle()
      except StopIteration:
        contador+=1
        print('modelo cargado')



