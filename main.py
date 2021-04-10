import pygame
import pygame.mixer
import time

import pyfxr

pygame.mixer.pre_init(
    44100,
    channels=1
)
pygame.mixer.init()

sine = pyfxr.Waveform.square()

start = time.perf_counter_ns()
tone = pyfxr.pluck(duration=1.0, pitch='A4')
end = time.perf_counter_ns()

print("Generated tone in", (end - start) // 1000, "us")

pygame.mixer.Sound(buffer=tone).play()

time.sleep(tone.duration)

tone.save('output.wav')
