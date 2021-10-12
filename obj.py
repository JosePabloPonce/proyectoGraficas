import struct

def color(r, g, b):
  return bytes([b, g, r])




def try_int_minus1(s, base=10, val=None):
  try:
    return int(s, base) - 1
  except ValueError:
    return val


class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()
        self.vertices = []
        self.tvertices = []
        self.normals = []
        self.faces = []
        self.read()

    def read(self):
        for line in self.lines:
            if line:
                try:
                    prefix, value = line.split(' ', 1)
                except:
                    prefix = ''
                if prefix == 'v':
                    self.vertices.append(list(map(float, value.split(' '))))
                elif prefix == 'vt':
                    self.tvertices.append(list(map(float, value.split(' '))))
                elif prefix == 'vn':
                    self.normals.append(list(map(float, value.split(' '))))
                elif prefix == 'f':
                    self.faces.append([list(map(try_int_minus1, face.split('/'))) for face in value.split(' ')])



class Texture(object):
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        img = open(self.path, "rb")
        img.seek(10)
        headerSize = struct.unpack('=l', img.read(4))[0]

        img.seek(14 + 4)
        self.width = struct.unpack('=l', img.read(4))[0]
        self.height = struct.unpack('=l', img.read(4))[0]

        img.seek(headerSize)
        self.pixels = []
        for y in range(self.height):
            for x in range(self.width):
                b = ord(img.read(1)) 
                g = ord(img.read(1)) 
                r = ord(img.read(1)) 

                self.pixels.append(b)
                self.pixels.append(g)
                self.pixels.append(r)

        img.close()

    def get_color(self, tx, ty, intensity = 1):
        x = int(tx * self.width)
        y = int(ty * self.height)
        index = (y * self.width + x) * 3
        processed = self.pixels[index:index+3] * intensity
        return processed