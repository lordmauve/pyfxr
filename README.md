# pyfxr

Sound effects generation for Python, compatible with Pygame and Pyglet.


## Installation

`pyfxr` is on PyPI and pre-compiled for Mac, Windows and Linux. You can install
the library with

```
pip install pyfxr
```

To also install the Pygame-based GUI, use

```
pip install pyfxr[gui]
```

## Pygame Usage

```
# Set mixer to 44kHz mono
pygame.mixer.pre_init(44100, channels=1)

# Generate a sound
tone = pygame.mixer.Sound(
    buffer=pyfxr.pluck(duration=1.0, pitch='A4')
)

# Play it
tone.play()
```

## Pyglet Usage

```
# Generate a sound
explosion = pyglet.media.StaticSource(pyfxr.explosion())

# Play it
explosion.play()
```

## GUI

A Pygame GUI is in development, to explore the feature set and create music!

This can be run with `python main.py`.

![Screenshot](docs/_static/keyboard.png)
