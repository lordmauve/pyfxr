# pyfxr

Sound effects generation for Python, compatible with Pygame and Pyglet.


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
