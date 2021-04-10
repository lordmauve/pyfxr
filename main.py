from math import sin
import abc
import pygame
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
    wt = pyfxr.Wavetable.from_function(
        lambda t: sin(t) * 0.7 + 0.3 * sin(6 * t + 0.5)
    )

    def __init__(self, note, *args, **kwargs):
        self.note = note
        super().__init__(*args, **kwargs)

    def on_click(self):
        pygame.mixer.Sound(
            buffer=pyfxr.tone(
                self.note,
                attack=0.05,
                sustain=0.0,
                release=0.1,
                wavetable=self.wt
            )
        ).play()


WIDGETS = []


def make_keyboard():
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    x = 50
    y = 390
    white_notes = []
    black_notes = []
    for octave in (3, 4):
        for note in notes:
            if '#' in note:
                black_notes.append(Key(
                    f'{note}{octave}',
                    Rect(x - 18, y - 1, 36, 130),
                    BLACK_KEY,
                    radius=3
                ))
            else:
                white_notes.append(Key(
                    f'{note}{octave}',
                    Rect(x, y, 50, 200),
                    WHITE_KEY,
                ))
                x += 50
    WIDGETS.extend(white_notes)
    WIDGETS.extend(black_notes)



make_keyboard()


def widget_at(pos):
    for b in reversed(WIDGETS):
        if b.rect.collidepoint(pos):
            return b
    return None


def main():
    global screen
    pygame.mixer.pre_init(
        44100,
        channels=1
    )
    pygame.init()
    pygame.display.set_caption("pyfxr")
    screen = pygame.display.set_mode((800, 600))

    while True:
        draw()
        pygame.display.flip()

        ev = pygame.event.wait()
        if ev.type == pygame.QUIT:
            return
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == pygame.BUTTON_LEFT:
                w = widget_at(ev.pos)
                w and w.click()
        elif ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == pygame.BUTTON_LEFT:
                w = widget_at(ev.pos)
                w and w.release()


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
