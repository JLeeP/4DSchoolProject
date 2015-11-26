
import pyglet
from pyglet.gl import *
from pyglet import clock, window


'''
    http://www.learnersdictionary.com/search/aspect
    a dictionary site

    http://www.opengl.org/sdk/docs/man2/
    opengl api reference

'''

def vector(type, *args):
    '''
        return a ctype array
        GLfloat
        GLuint
        ...
    '''
    return (type*len(args))(*args)


# I added some paraeters to the __init__ function that prompts the user for the following:
# raw_angle = the speed of rotation,
#raw_rotation = the magnitude of the rotation,
# x , y, z which define the coordinates of the pivot point about which the rotation is to take place
# I believe we can add some attributes in order for us to vary the dimension of the displays we have, i will look into that
# Do check this out and suggestions as to what to add or remove are very welcome
# Notice there are two CLASSES so far: model, and world.


class model:
    def __init__(self, vertices, colorMatrix, indice, raw_angle, raw_rotation, x, y, z):
        self.vertices = vertices
        self.colorMatrix = colorMatrix
        self.indice = indice
        self.angle = 0
        self.raw_angle = raw_angle
        self.raw_rotation = raw_rotation
        self.x = x
        self.y = y
        self.z = z
        
    def update(self):
        self.angle += raw_angle
        self.angle %= raw_rotation

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
     
        glRotatef(self.angle, x, y, z)


        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        glColorPointer(3, GL_FLOAT, 0, vector(GLfloat, *self.colorMatrix))
        glVertexPointer(3, GL_FLOAT, 0, vector(GLfloat, *self.vertices))

        glDrawElements(GL_QUADS, len(self.indice), GL_UNSIGNED_INT, vector(GLuint, *self.indice))


        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)



class world:
    def __init__(self):
        self.element = []

    def update(self, dt):
        for obj in self.element:
            obj.update()

    def addModel(self, model):
        self.element.append(model)

    def draw(self):
        for obj in self.element:
            obj.draw()


def setup():
    # look for GL_DEPTH_BUFFER_BIT
    glEnable(GL_DEPTH_TEST)







win = window.Window(fullscreen=False, vsync=True, resizable=True, height=600, width=600)
mWorld = world()

cube1 = (
    1, 1, 1, #0
    -1, 1, 1, #1
    -1, -1, 1, #2
    1, -1, 1, #3
    1, 1, -1, #4
    -1, 1, -1, #5
    -1, -1, -1, #6
    1, -1, -1 #7
)

def modifyer(cube, a):
    array = [i * n for i in cube]
    tup = ()
    for x in array:
        tup += (x,)
        new_cube = tup
    return new_cube
n = int(raw_input('By what factor do you want to change the size of the object: '))
result =  modifyer(cube1, n)


color = (
    1, 0, 0,
    1, 0, 0,
    1, 0, 0,
    1, 0, 0,
    0, 1, 0,
    0, 1, 0,
    0, 0, 1,
    0, 0, 1
)

indice = (
    0, 1, 2, 3, # front face
    0, 4, 5, 1, # top face
    4, 0, 3, 7, # right face
    1, 5, 6, 2, # left face
    3, 2, 6, 7 # bottom face
    #4, 7, 6, 5  #back face
)
raw_angle = int(raw_input('speed of rotation: '))

raw_rotation = int(raw_input('angle of rotation: '))
x = int(raw_input('x-coordinate of pivot point: '))
y = int(raw_input('y-coordinate of pivot point: '))
z = int(raw_input('z-coordinate of pivot point: '))





obj = model(result, color, indice, raw_angle, raw_rotation, x, y, z)
mWorld.addModel(obj)


@win.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-10, 10, -10, 10, -10, 10)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED

@win.event
def on_draw():
    glClearColor(0.2, 0.2, 0.2, 0.8)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    mWorld.draw()


pyglet.clock.schedule(mWorld.update)
clock.set_fps_limit(0)
setup()
pyglet.app.run()
