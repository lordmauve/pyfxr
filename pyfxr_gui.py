from math import sin, pi, copysign, cos
import random
import abc
import sys
from functools import lru_cache
import inspect

try:
    import pygame
except ModuleNotFoundError:
    sys.exit(
        "Pygame was not found. To use the GUI, make sure you install "
        "pyfxr with\n\npip install pyfxr[gui]"
    )
import pygame.draw
import pygame.mixer
from pygame import Rect
import time

import pyfxr


BACKGROUND = pygame.Color((200, 128, 50))
WHITE_KEY = pygame.Color((200, 200, 180))
BLACK_KEY = pygame.Color((50, 50, 50))
screen: pygame.Surface = None


def lighter(color):
    return pygame.Color(
        128 + color.r >> 1,
        128 + color.g >> 1,
        128 + color.b >> 1,
    )

def darker(color):
    return pygame.Color(
        color.r >> 1,
        color.g >> 1,
        color.b >> 1,
    )


def rounded_rect(color, rect, radius=5):
    highlight = darker(color)
    pygame.draw.rect(screen, color, rect, width=0, border_radius=radius)
    pygame.draw.rect(screen, highlight, rect, width=1, border_radius=radius)


def text(text, pos, color='black', align='left'):
    surf = text_surf(text, color)
    x, y = pos
    w, h = surf.get_size()
    if align == 'left':
        pass
    elif align == 'center':
        x -= w // 2
    elif align == 'right':
        x -= w
    else:
        raise ValueError(
            "align must be left, right, or center"
        )
    screen.blit(surf, (x, y))
    return pygame.Rect(x, y, *surf.get_size())


@lru_cache()
def text_surf(text, color='black'):
    """Get a rendered text surface, with caching."""
    if isinstance(color, str):
        color = pygame.Color(color)
    return font.render(text, True, color)


def draw():
    screen.fill(BACKGROUND)

    for w in WIDGETS:
        w.draw()


class Button(abc.ABC):
    def __init__(self, rect, color, radius=5):
        self.rect = rect
        self.color = color
        self.radius = radius
        self.selected = False

    def draw(self):
        color = lighter(self.color) if self.selected else self.color
        rounded_rect(color, self.rect)

    def click(self):
        self.selected = True
        self.on_click()

    def release(self):
        self.selected = False

    @abc.abstractmethod
    def on_click(self):
        """Implement this to define click interactions."""


class Key(Button):
    def __init__(self, note, *args, **kwargs):
        self.note = note
        super().__init__(*args, **kwargs)

    def on_click(self):
        print(
            "tone = pyfxr.tone(",
            f"    {self.note!r}",
            "    attack=0.05,",
            "    sustain=0.0,",
            "    release=0.1,",
            "    wavetable=wavetable,",
            ")",
            sep="\n"
        )
        s = pygame.mixer.Sound(
            buffer=pyfxr.tone(
                self.note,
                attack=0.05,
                sustain=0.0,
                release=0.1,
                wavetable=Waveform.current
            )
        )
        s.set_volume(0.5)
        s.play()


class Label(Button):
    def __init__(self, text, pos, color='black', align='left'):
        self.color = color
        self.align = align
        self.surf = None
        self._text = text
        self.rect = Rect(-1, -1, 0, 0)
        self.pos = pos

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.surf = None
        self.rect = Rect(-1, -1, 0, 0)

    def draw(self):
        self.rect = text(self._text, self.pos, self.color, self.align)

    def on_click(self):
        """Labels are not click-sensitive so this does nothing."""


class Waveform:
    current = None

    def __init__(self, waveform, rect):
        self.waveform_str = inspect.cleandoc(waveform)
        self.waveform = eval(waveform)
        self.rect = rect
        wf = memoryview(self.waveform)
        points = []
        for i in range(0, 1024, 8):
            x = self.rect.left + i / 1024 * self.rect.width
            y = self.rect.centery + wf[i] / (1 << 15) * (self.rect.height / 2.6)
            points.append((x, y))
        self.points = points

        if Waveform.current is None:
            Waveform.current = self.waveform

    def draw(self):
        if self.current is self.waveform:
            rounded_rect(pygame.Color('white'), self.rect)
        else:
            rounded_rect(WHITE_KEY, self.rect)
        pygame.draw.aalines(
            screen,
            'red',
            False,
            self.points
        )

    def click(self):
        print(f"wavetable = {self.waveform_str}")
        Waveform.current = self.waveform

    def release(self):
        pass


WIDGETS = []


def make_keyboard():
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    notes = [f'{note}{octave}' for octave in (3, 4, 5) for note in notes][:25]

    keyboard = Rect(0, 400, 800, 200)
    x = keyboard.left
    white_notes = []
    black_notes = []

    n_white_keys = sum('#' not in note for note in notes)
    key_width = keyboard.width / n_white_keys
    black_width = 2 * (key_width * 2 // 6)

    for note in notes:
        if '#' in note:
            black_notes.append(Key(
                note,
                Rect(x - black_width // 2, keyboard.top - 3, black_width, keyboard.height * 2 // 3),
                BLACK_KEY,
                radius=3
            ))
        else:
            white_notes.append(Key(
                note,
                Rect(int(x), keyboard.top, int(x + key_width) - int(x) + 1, keyboard.height),
                WHITE_KEY,
            ))
            x += key_width
    WIDGETS.extend(white_notes)
    WIDGETS.extend(black_notes)

    waves = [
        "pyfxr.Wavetable.sine()",
        "pyfxr.Wavetable.square()",
        "pyfxr.Wavetable.saw()",
        "pyfxr.Wavetable.triangle()",
        """pyfxr.Wavetable.from_function(
            lambda t: sin(t) * 0.7 + 0.3 * sin(6 * t + 0.5)
        )""",
        """pyfxr.Wavetable.from_function(
            lambda t: sin(t) * 0.5 + 0.5 * sin(2 * t)
        )""",
        """pyfxr.Wavetable.from_function(
            lambda t: sin(t) * 0.4 + 0.3 * sin(2 * t) + 0.3 * sin(10 * t - 1) * sin(t / 2)
        )""",
        """pyfxr.Wavetable.from_function(
            lambda t: 1 - 2 * abs(sin(t / 2 + pi / 2))
        )""",
        """pyfxr.Wavetable.from_function(
            lambda t: sin(10 * t) * sin(t / 2)
        )""",
        "pyfxr.Wavetable.square(0.8)",
        """pyfxr.Wavetable.from_function(
            lambda t: (sin(t) + sin(3 * t) + sin(5 * t)) / 3
        )""",
        """pyfxr.Wavetable.from_function(
            lambda t: sin(t) * 0.9 + 0.1 * copysign(sin(t), sin(3 * t))
        )""",
    ]

    padding = 10
    grid = Rect(30, 60, 800 - 60, 300)
    for i, w in enumerate(waves):
        ycell, xcell = divmod(i, 4)
        width = (grid.width - 3 * padding) / 4
        height = (grid.height - 3 * padding) / 3
        x = grid.left + xcell * (width + padding)
        y = grid.top + ycell * (height + padding)
        WIDGETS.append(Waveform(w, Rect(x, y, width, height)))

    WIDGETS.append(Label("Example Waveforms", (30, 40)))


make_keyboard()


def widget_at(pos):
    for b in reversed(WIDGETS):
        if b.rect.collidepoint(pos):
            return b
    return None


def main():
    global screen, font
    pygame.mixer.pre_init(
        44100,
        channels=1
    )
    pygame.init()
    pygame.display.set_caption("pyfxr")
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont('sans-serif', 24, bold=False)

    while True:
        draw()
        pygame.display.flip()

        ev = pygame.event.wait()
        if ev.type == pygame.QUIT:
            return
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == pygame.BUTTON_LEFT:
                clicked = widget_at(ev.pos)
                if clicked:
                    clicked.click()
        elif ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == pygame.BUTTON_LEFT:
                if clicked:
                    clicked.release()
                    clicked = None


def play():
    sine = pyfxr.Waveform.square()

    start = time.perf_counter_ns()
    tone = pyfxr.pluck(duration=1.0, pitch='A4')
    end = time.perf_counter_ns()

    print("Generated tone in", (end - start) // 1000, "us")

    pygame.mixer.Sound(buffer=tone).play()

    time.sleep(tone.duration)

    tone.save('output.wav')


if __name__ == '__main__':
    main()
