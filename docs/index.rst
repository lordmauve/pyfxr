pyfxr - a simple synth for games
================================

pyfxr generates tones and noises in fast Cython code, and is intended for use
in simple Python computer games and in education. It can generate:

* Highly configurable noises (the original sfxr_)
* Pure tones with sine, square, saw and triangle waveforms
* Pluck sounds, like harp or guitar, using the `Karplus-Strong algorithm`__

.. __: https://flothesof.github.io/Karplus-Strong-algorithm-Python.html

Sounds can be played with any library that supports the buffer protocol (such
as Pygame), or saved to ``.wav`` files.

.. _sfxr: https://www.drpetter.se/project_sfxr.html

For example, this is a complete program to generate a 1s pluck sound and play
it with Pygame:

.. code-block:: python

    import pygame.mixer
    import time
    import pyfxr

    # pyfxr generates mono 44kHz sounds so we must set
    # Pygame to use this
    pygame.mixer.pre_init(44100, channels=1)
    pygame.mixer.init()

    tone = pyfxr.pluck(duration=1.0, pitch='A4')
    pygame.mixer.Sound(buffer=tone).play()

    # wait for the sound to finish before exiting
    time.sleep(tone.duration)


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   generating
   composing
   soundbuffer


Changes
-------

.. currentmodule:: pyfxr

0.3.0
'''''

* New: :func:`chord` for combining sounds
* New: :func:`simple_chord` for generating harmonic chords from chord names

0.2.0
'''''

* New: :class:`SFX`, which manages parameters for sfx generation
* Change: ``jump()``, ``explosion()`` etc now return ``SFX`` instances.
* New: GUI now prints code for sounds generated
* Deprecation: ``sfx()`` is now deprecated, use :class:`SFX`.
* Fix: bug in handling of ``arp_mod`` parameter

0.1.0
'''''

Initial release.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
