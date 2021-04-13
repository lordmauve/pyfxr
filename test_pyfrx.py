from math import sin, pi, floor

from pytest import approx

from pyfxr import Wavetable, tone


tau = 2 * pi

AMPLITUDE = (1 << 15) - 1


def test_sine_wave():
    """We can generate a sine wave."""
    w = Wavetable.sine()
    assert memoryview(w)[357] == floor(sin(357 / 1023 * tau) * AMPLITUDE)


def test_wavetable_generator():
    """We can constrct a wavetable from a generator."""
    def samples():
        for i in range(1024):
            yield i / 1023 * 2 - 1

    w = memoryview(Wavetable(samples()))
    for i in range(1023):
        assert w[i] < w[i + 1]


def test_adsr_envelope():
    """Tones are modulated by an ADSR envelope."""
    w = Wavetable.from_function(lambda t: 1)
    sound = tone(
        attack=0.1,
        decay=0.1,
        sustain=0.75,
        release=0.25,
        wavetable=w
    )

    def sample_at(t: float) -> float:
        """Get the (float) value of the waveform at time t."""
        return sound[min(int(t * 44100), len(sound) - 1)] / (1 << 15)

    samples = list(map(
        sample_at,
        [0, 0.05, 0.1, 0.2, 0.5, 0.95, 1.2],
    ))

    assert samples == approx(
        [0, 0.5, 1.0, 0.7, 0.7, 0.7, 0],
        abs=1e-3
    )


def test_sine_tone():
    """The wavetable is repeated through the tone."""
    # Calculate the envelope so we can divide it out of the generated sample
    envelope = tone(
        wavetable=Wavetable.from_function(lambda t: 1)
    )
    pitch = 50.0
    sound = tone(pitch=pitch)

    samples = []
    expected = []

    for i in range(1000, 44100, 1000):
        t = i / 44100.0
        phase = (t * pitch) % 1.0 * tau
        sample = sound[i]
        env = envelope[i]
        samples.append(sample / env)
        expected.append(sin(phase))

    assert samples == approx(expected, abs=0.05)

