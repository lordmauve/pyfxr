import pygame
import pygame.mixer
import time

import pyfxr

pygame.mixer.pre_init(44100, channels=1)
pygame.mixer.init()

sine = pyfxr.Waveform.square()

start = time.perf_counter_ns()
tone = pyfxr.tone(sine)
end = time.perf_counter_ns()

print("Generated tone in", (end - start) // 1000, "us")

pygame.mixer.Sound(buffer=tone).play()

time.sleep(tone.duration)

import wave

with wave.open('output.wav', 'wb') as wav:
    wav.setframerate(44100)
    wav.setnchannels(1)
    wav.setnframes(len(tone))
    wav.setsampwidth(2)
    wav.writeframesraw(tone)
