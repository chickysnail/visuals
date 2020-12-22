import matplotlib; matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from perlin_noise import PerlinNoise
import numpy as np
import winsound
import os

noise = PerlinNoise()

fig = plt.figure()
ax = fig.add_subplot(111, projection='polar')  # with polar projection its easier to draw such shapes
ax.axis('off')  # makes the output picture clean without background grid and axis
line, = ax.plot([], [], linestyle='-')

n = 1000  # amount of points on a circle to make it more detailed
theta = np.linspace(0, 2 * np.pi, n - 1, endpoint=False)  # angle for drawing the end shape
theta = np.append(theta, 0.0)  # from angle 0 to 0 to make the shape closed. I dont know how to automatically close a shape in MPL
angles = np.linspace(0, 2 * np.pi, n)  # angle for choosing offset values on perlin noise
radius = 0.5

total_frames = 360  # amount of frames in a GIF
loop_radius = 1.3  # to make the GIF seamlessly repeating the first circle (where we take offset from) and the last must
# be next to each other. This circle will be moving with its center on another circle with this radius
alpha = np.linspace(0, 2 * np.pi, total_frames)  # how fast the center of outer circle will be moving on the inner circle
xshift = np.cos(alpha) * loop_radius
yshift = np.sin(alpha) * loop_radius

ax.set_ylim(0, 1 + radius)


def gen_offset(noise, n, radius, shift):
    offset = []
    xoff = np.cos(1 * angles) * radius + shift[0]  # you can change factors of angles to make different symmetry shapes
    yoff = np.sin(1 * angles) * radius + shift[1]
    for i in range(n):
        value = noise([xoff[i], yoff[i]])
        offset.append(value)
    return np.array(offset)


def init():
    line.set_data([], [])
    return line


def transition(t):
    offset = gen_offset(noise, n, radius, (xshift[t], yshift[t]))
    r = np.ones(n) + offset
    line.set_data(theta, r)
    return line


anim = FuncAnimation(fig, transition, interval=2, frames=total_frames)

path = lambda i: rf'..\perlin_circle{"%03d" % (i,)}.gif'
i = 0
while os.path.exists(path(i)):
    i += 1

anim.save(path(i), 'imagemagick', fps=30)
winsound.Beep(500, 500)  # it takes a bit of time to render the GIF so you can hear when it's ready.
print(path(i))
