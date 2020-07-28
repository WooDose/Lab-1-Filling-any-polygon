import struct
import pprint

from copy import deepcopy
from obj import Obj

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(c):
    return struct.pack('=h', c)

def dword(c):
    return struct.pack('=l', c)

def color(r, g, b):
    return bytes([b, g, r])

class Render(object):
    def __init__(self, width, height, vpw, vph, vpx, vpy):
        self.width = width
        self.height = height
        self.framebuffer = []
        self.clearColor = color(0,0,0)
        self.glCreateWindow()
        self.glViewport(vpw, vph, vpx, vpy)
        self.drawColor = color(0,0,0)
        self.glClear()

    def glInit(self):
        pass
    
    def glCreateWindow(self):
        #print(self.framebuffer)
        self.framebuffer = [
            [self.clearColor for x in range(self.width)]
             for y in range(self.height)
        ]
        #pprint.pprint(self.framebuffer)
    
    def glViewport(self, width, height, x, y):
        self.ViewportWidth = width
        self.ViewportHeight = height
        self.xNormalized = x
        self.yNormalized = y


    def glClear(self):
        self.framebuffer = [
            [self.clearColor for x in range(self.width)]
             for y in range(self.height)
        ]

    def glClearColor(self, r,g,b):
        self.clearColor = color(int(r*255),int(g*255),int(b*255))

    def glColor(self, r,g,b):
        self.drawColor = color(int(r*255),int(g*255),int(b*255))

    def point(self,x,y):
        self.framebuffer[x][y] = self.drawColor
    
    def line(self, x1, y1, x2, y2):
        dy = abs(y2 - y1)
        #print(y2,y1)
        dx = abs(x2 - x1)
        # print(x2,x1)
        # print(dx)
        steep = dy > dx

        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dy = abs(y2 - y1)
        #print(y2,y1)
        dx = abs(x2 - x1)
        # print(x1,x2,y1,y2)

        offset =  0 * 2 * dx
        threshold = 0.5 * 2 * dx
        y = y1

        points = []
        # print( x1,x2)
        for x in range(x1, x2 + 1):
            # print (x, y)
            if steep:
                points.append((y, x))
            else:
                points.append((x, y))
            
            #print(dy)
            offset += dy * 2
            # print(offset, threshold, y )
            if offset > threshold:
                y += 1 if y1 < y2 else -1
                threshold += 1 * 2 * dx

        for point in points:
            self.point(point[0], point[1])

    def glVertex(self, x,y): 
        xW = int(((x+1)*(self.ViewportWidth/2))+self.xNormalized)
        #print(xW)
        yW = int(((y+1)*(self.ViewportHeight/2))+self.yNormalized)
        xW = (xW - 1) if xW == self.width else xW
        yW = (yW - 1) if yW == self.height else yW
        self.point(xW, yW)

    def glLine(self, x0,y0,x1,y1):
        x0W = ((x0+1)*(self.ViewportWidth/2))+self.xNormalized
        # print(x0W)
        x0W = int(x0W)
        x1W = ((x1+1)*(self.ViewportWidth/2))+self.xNormalized
        # print(x1W)
        x1W = int(x1W)
        y0W = int(((y0+1)*(self.ViewportHeight/2))+self.yNormalized)
        y1W = int(((y1+1)*(self.ViewportHeight/2))+self.yNormalized)
        # print(x0W, x1W, y0W, y1W)
        x0W = (x0W - 1) if x0W == self.width else x0W
        x1W = (x1W - 1) if x1W == self.width else x1W
        y0W = (y0W - 1) if y0W == self.height else y0W
        y1W = (y1W - 1) if y1W == self.height else y1W
        self.line(x0W, y0W, x1W, y1W)

    def glFinish(self, filename):
        f = open(filename, 'bw')

        ## Write file header
        # Header Field
        f.write(char('B'))
        f.write(char('M'))
        # Size in Bytes
        f.write(dword(14 + 40 + (self.width * self.height * 3)))
        #Reserved
        f.write(word(0))
        f.write(word(0))
        #Offset
        f.write(dword(14 + 40))

        # Image header 
        # Bytes in Header
        f.write(dword(40))
        # Width
        f.write(dword(self.width))
        # Height
        f.write(dword(self.height))
        # Color Planes
        f.write(word(1))
        # Bits/Pixel
        f.write(word(24))
        # Pixel array compression
        f.write(dword(0))
        # Size of raw bitmap
        f.write(dword(self.width * self.height * 3))
        #Colors in palette
        f.write(dword(0))
        #Important Colors
        f.write(dword(0))
        # Unused/Reserved
        f.write(dword(0))
        f.write(dword(0))

        # Pixel data
        
        #print(self.framebuffer)
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[y][x])
        f.close()
    
    def point(self,x,y):
        self.framebuffer[x][y] = self.drawColor
    
    def getFrameBufferCopy(self):
        return deepcopy(self.framebuffer)

##Please for the love of God don't use non-4 multiples for your dimensions unless you want to absoultely do you know what to your you know what.

# 
# 
### Las funciones importantes para el LAB1 empiezan aqui
# 
# 

### Mi idea fue revisar a todas las direcciones de un pixel si existia algun pixel distinto al color del fondo, y si para todas se cumple, pintar este pixel.

### Referencias: Ninguna, la idea se me ocurrio platicando con amigos que han hecho proyectos similares y mencionaron el algoritmo "Edge" para esto
###              No quise usarlo asi como me lo dijeron porque tampoco queria usar algo ya hecho, pero la idea de "buscar esquinas de la imagen" me parecio buena
###              y me base en eso. 

def is_encased(pixel, framebuffer,  bg_color, fb_x, fb_y):
    '''
    pixel: pixel en el que estamos
    framebuffer: copia del framebuffer inicial
    bg_color: color que queremos rellenar
    
    Devuelve True si tiene por lo menos un pixel con color distinto a bg_color directamente hacia arriba, uno directamente hacia abajo, y uno directamente a cada lado.
    Devuelve False si por lo menos uno de los cuatro lados no tiene color distinto a bg_color  '''
    pixel_x = pixel[0]
    pixel_y = pixel[1]

    # Para fines practicos asumimos que si el pixel esta en una orilla, tiene un pixel de color distinto hacia el lado de esa orilla (estos son los pixel_x/y ==0 y == fb_x/y)

    ## Verificar a la izquierda y derecha
    if pixel_x == 0:
        left_is_encased = True    
    else:
        left_counter = 0
        for left in range(pixel_x):
            ##Si por lo menos un pixel dio positivo en la prueba, pasar al siguiente paso.
            left_counter += (0 if framebuffer[pixel_y][left] == bg_color else 1)
            if left_counter > 0:
                continue
        left_is_encased = True if left_counter > 0 else False
    
    ##Repetimos lo mismo para todas las direcciones restantes 
    if pixel_x == fb_x:
        right_is_encased = True
    else:
        right_counter = 0
        for right in range(pixel_x+1, fb_x):
            right_counter += (0 if framebuffer[pixel_y][right] == bg_color else 1)
        right_is_encased = True if right_counter > 0 else False
    
    ##Verificamos verticalmente
    if pixel_y == 0:
        up_is_encased = True
    else:
        up_counter = 0
        for up in range(pixel_y):
            up_counter += (0 if framebuffer[up][pixel_x] == bg_color else 1)
        up_is_encased = True if up_counter > 0 else False
    
    if pixel_y == fb_y:
        down_is_encased = True
    else:
        down_counter = 0
        for down in range(pixel_y+1, fb_y):
            down_counter += (0 if framebuffer[down][pixel_x] == bg_color else 1)
        down_is_encased = True if down_counter > 0 else False


    ##Regresamos True si y solo si se cumplen las cuatro condiciones, de lo contrario saltamos al siguiente.
    if (left_is_encased and right_is_encased and down_is_encased and up_is_encased):
        return True
    else:
        return False

## Algoritmo que utiliza el is_encased para determinar si pinta o no un pixel
def fillpolygon(framebuffer, framebuffer_x, framebuffer_y, bg_color, render):
    ## Utilizamos y,x porque asi definimos nuestro framebuffer
    for y in range(len(framebuffer)):
        for x in range(len(framebuffer[y])):
            ## Verificamos para el pixel en el que estamos (y,x) si cumple la condicion de estar "encerrado"
            if is_encased((y,x),framebuffer, bg_color, framebuffer_x, framebuffer_y):
                ## Use render.point en  lugar de render.glVertex porque al no ponerlo dentro de mi clase Render, tendria que hacer unos crazy gymmnastics para poder calcular las posiciones relativas.
                ## Realmente no es tan dificil o loco, solo es realizar el mismo calculo que se hace en las lineas 277 - 280 de DrawPolygon
                render.point(x,y)

## Este algoritmo solo crea el outline, y despues de crearlo corre fillpolygon para poder rellenarlo. 
def drawPolygon(filename, xdim, ydim, vertex_list, polygon=''):
    new_map = Render(xdim, ydim, xdim, ydim,0,0)
    new_map.glColor(0.65, 0.25, 0.75)
    for i in range(len(vertex_list)):
        v1 = vertex_list[i]
        if i != len(vertex_list)-1:
            v2 = vertex_list[i+1]
        else:
            v2 = vertex_list[0]
        print (i, i+1, len(vertex_list))
        x0 = float(v1[0]) / float(xdim)
        y0 = float(v1[1]) / float(ydim)
        x1 = float(v2[0]) / float(xdim)
        y1 = float(v2[1]) / float(ydim)
        ### El calculo de aqui arriba lo hicimos para convertir a las posiciones relativas, ya que el metodo no esta dentro del Render
        # x0 = v1[0]
        # y0 = v1[1]
        # x1 = v2[0]
        # y1 = v2[1]
        ### Estas lineas comentadas fueron debugging para probar con posiciones absolutas, pero las deje para recordarme del problema que me dio.
        # print((x0, y0, x1, y1))
        new_map.glLine(x0, y0, x1, y1)
    fillpolygon(new_map.getFrameBufferCopy(), xdim, ydim, color(0,0,0), new_map)
    new_map.glFinish(filename)

polygon1 = [(165, 380), (185, 360) ,(180, 330) ,(207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]

drawPolygon(r'polygon1.bmp', 600, 600, polygon1)

polygon2 = [(321, 335), (288, 286), (339, 251), (374, 302)]

drawPolygon(r'polygon2.bmp', 400, 400, polygon2)

polygon3 = [(377, 249) ,(411, 197) ,(436, 249)]

drawPolygon(r'polygon3.bmp', 600, 600, polygon3)

rectangle = [(0,0), (599,0), (599,300), (0,300)]

drawPolygon(r'rectangle.bmp', 600, 600, rectangle)

polygon4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52),
(750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230),
(597, 215), (552, 214), (517, 144), (466, 180)]

drawPolygon(r'polygon4.bmp', 800, 800, polygon4)


# def drawModel(filename, output, translate, scale,xdim=800, ydim=800):
#     model = Obj(filename)
#     new_map = Render(xdim, ydim, xdim, ydim,0,0)
#     new_map.glColor(0.25, 0.25, 0.75)

#     for face in model.faces:
#         vcount = len(face)

#         for j in range(vcount):
#             f1 = face[j][0]
#             f2 = face[(j + 1) % vcount][0]

#             v1 = model.vertices[f1 - 1]
#             v2 = model.vertices[f2 - 1]

#             x0 = float(v1[0]) / float(xdim)
#             y0 = float(v1[1]) / float(ydim)
#             x1 = float(v2[0]) / float(xdim)
#             y1 = float(v2[1]) / float(ydim)

#             x0 = ((x0 + translate[0]) * scale[0])
#             y0 = ((y0 + translate[1]) * scale[1])
#             x1 = ((x1 + translate[0]) * scale[0])
#             y1 = ((y1 + translate[1]) * scale[1])

#             # print(x0,y0,x1,y1)
#             new_map.glLine(x0, y0, x1, y1)
#     new_map.glFinish(output)

# sixthcandle = r'C:\Users\Diego\Documents\graphics\gl\6thcandle.obj'
# translate = (0,0)
# scale = (100,100)
# drawModel(sixthcandle, '6thcandle.bmp', translate, scale)

# sixthcandle = r'C:\Users\Diego\Documents\graphics\gl\glasshelm.obj'
# translate = (0,0)
# scale = (50,50)
# drawModel(sixthcandle, 'glasshelm.bmp', translate, scale)

# sixthcandle = r'C:\Users\Diego\Documents\graphics\gl\fern.obj'
# translate = (0,0)
# scale = (4,4)
# drawModel(sixthcandle, 'fern.bmp', translate, scale)

# sixthcandle = r'C:\Users\Diego\Documents\graphics\gl\tree.obj'
# translate = (0,0)
# scale = (3,3)
# drawModel(sixthcandle, 'tree.bmp', translate, scale, 3000, 3000)

# sixthcandle = r'C:\Users\Diego\Documents\graphics\gl\mush.obj'
# translate = (0,0)
# scale = (1,1)
# drawModel(sixthcandle, 'mush.bmp', translate, scale, 3000, 3000)

# sixthcandle = r'C:\Users\Diego\Documents\graphics\gl\akulakhan.obj'
# translate = (0,0)
# scale = (1,1)
# drawModel(sixthcandle, 'akulakhan.bmp', translate, scale, 3000, 3000)

