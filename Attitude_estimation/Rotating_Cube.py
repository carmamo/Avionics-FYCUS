import math
import random
import time
from vedo import Cube
from vedo import *
# Create a simple cone
c = Cube().texture('texture.jpg')

# Setup the scene
plt = Plotter(axes=2, interactive=False)

step = range(0,500,1)

for t in step:
    omega_x = random.randint(-2,2) #angular speed
    omega_z = random.randint(-2,2) #angular speed
    #omega_z = random.randint(-5,5) #angular speed
    #omega_x = 2  # angular speed
    #omega_y = 2 #angular speed
    omega_y = 5

    c.rotate_x(omega_x)
    c.rotate_y(omega_y)
    c.rotate_z(omega_z)
    plt.show(c, viewup="z",camera={'pos':(2,3,4), 'thickness':1000,})
    time.sleep(0.05)

plt.interactive().close()