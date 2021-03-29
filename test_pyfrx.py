from math import sin, pi, floor

from pytest import approx

from pyfxr import Waveform


tau = 2 * pi

AMPLITUDE = (1 << 15) - 1


def test_sine_wave():
    """We can generate a sine wave."""
    w = Waveform.sine()
    assert memoryview(w)[357] == floor(sin(357 / 1023 * tau) * AMPLITUDE)

