from math import sin, pi, copysign, cos
import random
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


class Button:
    def __init__(self, rect, color=WHITE_KEY, radius=5):
        self.rect = rect
        self.color = color
        self.radius = radius
        self.selected = False

    def draw(self):
        color = lighter(self.color) if self.selected else self.color
        rounded_rect(color, self.rect)

    def on_click(self, pos):
        """Implement this to define click interactions."""
        self.selected = True

    def on_drag(self, pos):
        """Implement this to define click interactions."""

    def on_release(self, pos):
        """Implement this to define click interactions."""
        self.selected = False


class Key(Button):
    def __init__(self, note, *args, **kwargs):
        self.note = note
        super().__init__(*args, **kwargs)

    def on_click(self, pos):
        super().on_click(pos)
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
        super().__init__(Rect(-1, -1, 0, 0), color)
        self.align = align
        self.surf = None
        self._text = text
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

    def on_click(self, pos):
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

    def on_click(self, pos):
        print(f"wavetable = {self.waveform_str}")
        Waveform.current = self.waveform

    def on_release(self, pos):
        pass


WIDGETS = []


class Keyboard:
    def __init__(self, rect=Rect(0, 400, 800, 200)):
        self.widgets = []
        self.rect = rect
        self.build(rect)
        self.clicked = True

    def draw(self):
        for w in self.widgets:
            w.draw()

    def build(self, keyboard: Rect):
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
        self.widgets.extend(white_notes)
        self.widgets.extend(black_notes)

    def key_at(self, pos):
        return widget_at(pos, self.widgets)

    def on_click(self, pos):
        widget = self.key_at(pos)
        if widget:
            widget.on_click(pos)
            self.clicked = widget

    def on_drag(self, pos):
        widget = self.key_at(pos)
        if widget != self.clicked:
            if self.clicked:
                self.clicked.on_release(pos)
            if widget:
                widget.on_click(pos)
            self.clicked = widget

    def on_release(self, pos):
        if self.clicked:
            self.clicked.on_release(pos)
            self.clicked = None


def make_waves():
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


def tones_tab():
    WIDGETS.clear()
    tabs()
    WIDGETS.append(Keyboard())
    make_waves()


sfx = pyfxr.SFX()


class Slider:
    def __init__(self, param, rect):
        self.rect = rect
        self.param_name = param
        self.label = param
        self.param = pyfxr.SFX.__dict__[param]
        self.value = self.param.default

    def draw(self):
        text(
            f"{self.label}: {round(self.value, 2)}",
            (self.rect.left, self.rect.top)
        )
        rounded_rect(
            WHITE_KEY,
            Rect(
                self.rect.left,
                self.rect.top + 25,
                self.rect.width,
                5
            )
        )
        rounded_rect(
            WHITE_KEY,
            self.slider_rect(),
        )

    def slider_rect(self):
        return Rect(
            self.rect.left + self.value * (self.rect.width - 16),
            self.rect.top + 15,
            16,
            24
        )

    def on_click(self, pos):
        slider = self.slider_rect()
        if slider.collidepoint(pos):
            x, y = pos
            self.drag_offset = x - slider.left
        else:
            self.drag_offset = None

    def on_drag(self, pos):
        if self.drag_offset is None:
            return

        x, y = pos
        slider_newx = clamp(
            x - self.drag_offset,
            self.rect.left,
            self.rect.right - 16
        )

        self.value = (slider_newx - self.rect.left) / (self.rect.width - 16)

    def on_release(self, pos):
        self.on_drag(pos)
        setattr(sfx, self.param_name, round(self.value, 2))
        playfx()


def playfx():
    print(f"sfx = {sfx!r}")
    s = pygame.mixer.Sound(
        buffer=sfx.build()
    )
    s.set_volume(0.5)
    s.play()


def clamp(v, min, max):
    if v < min:
        return min
    elif v > max:
        return max
    return v


class TextButton(Button):
    def draw(self):
        super().draw()
        x, y = self.rect.center
        text(self.label, (x, y - 8), align="center")


class Randomiser(TextButton):
    def __init__(self, func, rect):
        super().__init__(rect)
        self.func = self.label = func

    def on_click(self, pos):
        global sfx
        print(f"random_{self.func} = {self.func}()")
        sfx = getattr(pyfxr, self.func)()
        for w in WIDGETS:
            if isinstance(w, Slider):
                w.value = getattr(sfx, w.param_name)
        playfx()


def fxr_tab():
    WIDGETS.clear()
    tabs()

    params = [
        k
        for k, v in vars(pyfxr.SFX).items()
        if isinstance(v, pyfxr.FloatParam)
    ]

    x = 20
    y = 50
    randomisers = [
        "explosion",
        "hurt",
        "jump",
        "pickup",
        "powerup",
        "laser",
        "select",
    ]
    for func in randomisers:
        button = Randomiser(
            func,
            Rect(x, y, 150, 30),
        )
        y += 40
        WIDGETS.append(button)

    x = 190
    y = 50
    for param in params:
        WIDGETS.append(Slider(param, Rect(x, y, 150, 40)))
        y += 60
        if y > 500:
            y = 50
            x += 170

def tabs():
    WIDGETS.append(
        Label("F1 = tones     F2 = sfx", (20, 10))
    )


fxr_tab()

def widget_at(pos, widgets=None):
    for b in reversed(widgets or WIDGETS):
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
                    clicked.on_click(ev.pos)
        elif ev.type == pygame.MOUSEMOTION:
            if pygame.BUTTON_LEFT in ev.buttons:
                if clicked:
                    clicked.on_drag(ev.pos)
        elif ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == pygame.BUTTON_LEFT:
                if clicked:
                    clicked.on_release(ev.pos)
                    clicked = None
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_F1:
                tones_tab()
            elif ev.key == pygame.K_F2:
                fxr_tab()


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
