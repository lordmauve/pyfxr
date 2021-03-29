import pygame
import pygame.mixer
import time

import pyfxr

pygame.mixer.pre_init()
pygame.mixer.init()

sine = pyfxr.Waveform.saw()

start = time.perf_counter_ns()
tone = pyfxr.tone(sine)
end = time.perf_counter_ns()

print("Generated tone in", (end - start) // 1000, "us")

pygame.mixer.Sound(buffer=tone).play()

time.sleep(tone.duration)
