import pyglet.media
import pyfxr

window = pyglet.window.Window()

source = pyglet.media.StaticSource(
    pyfxr.pluck(duration=1.0, pitch='A4')
)

@window.event
def on_mouse_press(x, y, button, modifiers):
    source.play()

pyglet.app.run()
