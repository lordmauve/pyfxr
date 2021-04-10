from math import sin
import pyglet.media
import pyfxr

window = pyglet.window.Window()

wt = pyfxr.Wavetable.from_function(
    lambda t: 0.75 * sin(t) + 0.25 * sin(3 * t + 0.5)
)
tone = pyfxr.tone(pitch='A4')
#tone = pyfxr.pluck(duration=1.0, pitch='A4')
source = pyglet.media.StaticSource(tone)

@window.event
def on_mouse_press(x, y, button, modifiers):
    source.play()

pyglet.app.run()
