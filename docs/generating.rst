Generating sounds
=================

.. currentmodule:: pyfxr

pyfxr has 3 sound generation algorithms, described below.


sfxr-style sounds
-----------------

sfxr_ is a user interface for generating sounds with a wide array of
parameters. pyfxr provides a full API to generate these sounds in Python
programs.

.. _sfxr: https://www.drpetter.se/project_sfxr.html

.. autofunction:: sfx

You can also randomly generate those parameters:

.. autofunction:: pickup
.. autofunction:: laser
.. autofunction:: explosion
.. autofunction:: powerup
.. autofunction:: hurt
.. autofunction:: jump
.. autofunction:: select


Wavetable sounds
----------------

pyfxr can also generate pure tones using a wavetable. A wavetable gives the
shape of a waveform, such as these:

.. plot::

    from matplotlib import pyplot as plt
    from pyfxr import Wavetable

    figs = plt.figure(figsize=(8, 5)).subplots(2, 2).flat
    waves = [
        ("Sine", Wavetable.sine()),
        ("Square", Wavetable.square()),
        ("Triangle", Wavetable.triangle()),
        ("Saw", Wavetable.saw()),
    ]
    plt.subplots_adjust(hspace=0.5)
    for fig, (name, wavetable) in zip(figs, waves):
        fig.set_title(name)
        fig.plot(range(1024), memoryview(wavetable))


Wavetables can have any shape. To construct a Wavetable with a custom shape,
pass an iterable to the constructor. This should return 1024 float values in
[-1, 1].

.. code-block:: python

    from math import pi, sin
    from pyfxr import Wavetable

    def gen():
        for i in range(1024):
            t = pi / 512 * i
            yield 0.75 * sin(t) + 0.25 * sin(3 * t + 0.5)

    wt = Wavetable(gen())

Or perhaps more simply, use ``Wavetable.from_function()``:

.. code-block:: python

    Wavetable.from_function(
        lambda t: 0.75 * sin(t) + 0.25 * sin(3 * t + 0.5)
    )


.. plot::

    from matplotlib import pyplot as plt
    from pyfxr import Wavetable
    from math import pi, sin

    wt = Wavetable.from_function(
        lambda t: 0.75 * sin(t) + 0.25 * sin(3 * t + 0.5)
    )
    plt.plot(range(1024), memoryview(wt))


.. autoclass:: pyfxr.Wavetable
    :members:

.. autofunction:: pyfxr.tone


ADSR Envelopes
''''''''''''''

Tones are bounded by a 4-phase "ADSR Envelope". The phases are:

* **Attack** - initial increase in volume
* **Decay** - volume decreases to the sustain level
* **Sustain** - the volume stays constant while the note is held
* **Release** - the volume fades to zero

.. plot::

    from pyfxr import Wavetable, tone

    t = tone(wavetable=Wavetable([1] * 1024))
    plt.plot(range(len(t)), [s / (1 << 15) for s in memoryview(t)])


The default ADSR envelope has this shape. Note that durations for any of the
ADSR phases can be set to zero to omit that phase. It is recommended to skip
only decay and sustain phases, as attack and release phases help to avoid
clicks when the sound plays.

This is applied to a waveform by multiplication:

.. plot::

    from pyfxr import Wavetable, tone

    envelope = tone(wavetable=Wavetable([1] * 1024))
    sound = tone(15)
    plt.plot(range(len(envelope)), memoryview(envelope), memoryview(sound))


Pluck sounds
------------

pyfxr can also generate pluck sounds, like a guitar or harp.

.. autofunction:: pyfxr.pluck()
