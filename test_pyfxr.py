import math
import pytest
from pyfxr import note_to_hertz, simple_chord, tone, jump, SoundBuffer


def test_note_to_hertz_a4():
    """note_to_hertz converts note names to frequencies."""
    assert math.isclose(note_to_hertz("A4"), 440.0)


def test_note_to_hertz_c5():
    """Another note conversion check."""
    expected = 440.0 * math.pow(2 ** (1/12), 3)  # C5 is 3 semitones above A4
    assert math.isclose(note_to_hertz("C5"), expected)


def test_simple_chord_invalid():
    """Invalid chord names raise ValueError."""
    with pytest.raises(ValueError):
        simple_chord("H7")


def test_jump_builds_sound():
    """jump returns an SFX object that can build a SoundBuffer."""
    fx = jump()
    sound = fx.build()
    assert isinstance(sound, SoundBuffer)
    assert len(sound) > 0


def test_tone_string_pitch():
    """tone accepts a note string for pitch."""
    snd = tone(pitch="A4")
    assert isinstance(snd, SoundBuffer)
    assert snd.duration > 0


def test_buffer_protocol():
    """SFX and SoundBuffer expose the buffer protocol."""
    fx = jump()
    sb = fx.build()

    mv_fx = memoryview(fx)
    mv_sb = memoryview(sb)

    assert mv_fx.format == "h"
    assert mv_sb.format == "h"
    assert mv_fx.itemsize == 2
    assert mv_fx.ndim == 1
    assert mv_sb.ndim == 1
    assert mv_fx.shape == mv_sb.shape
    assert len(mv_fx) == len(mv_sb) > 0
